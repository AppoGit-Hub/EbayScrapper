import time
import sys
import json
import logging
import logging.handlers
from logging import Logger
import os
import datetime as dt
from typing import Optional

import bs4
import requests
import psycopg2
import psycopg2._psycopg as psycopg

import offer
from models import Offer, ScrapStats, RunStats
from queries import EXIST_QUERY, INSERT_QUERY
from common import LOG_DIRECTORY, LOGNAME_PATTERN

def get_logger(subject: str):
    now = dt.datetime.now()
    current_date: str = now.strftime("%Y-%m-%d")

    log_filename = LOGNAME_PATTERN.format(subject=subject, date=current_date) 

    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=os.path.join(LOG_DIRECTORY, log_filename)
    )

    return logging.getLogger(subject)

def get_connection(postgress: dict):
    connection = psycopg2.connect(**postgress)
    return connection, connection.cursor()

def nullable(parameter):
    return f"'{parameter}'" if parameter else "NULL"

def notnull(parameter):
    assert(parameter)
    return f"'{parameter}'"

def display_timeleft(subject: str, seconds: int):
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    
    sys.stdout.flush()
    print(f"{subject} time left: {days}d, {hours % 24}h, {minutes % 60}m, {seconds % 60}s")

def exist_offer(cursor: psycopg.cursor, offer: Offer):
    cursor.execute(EXIST_QUERY.format(
        id = notnull(offer.id),
        date = notnull(offer.date),
        title = notnull(offer.title),
        type = notnull(offer.type)
    ))
    return isinstance(cursor.fetchone(), tuple)

def insert_offer(cursor: psycopg.cursor, offer: Offer):
    cursor.execute(INSERT_QUERY.format(
        id = notnull(offer.id),
        current_date = notnull(offer.date),
        title = notnull(offer.title),
        type = notnull(offer.type),
        is_new = nullable(offer.is_new),
        star = nullable(offer.star),
        subtitle = nullable(offer.subtitle),
        price = nullable(offer.price),
        pseudo = nullable(offer.pseudo),
        sales_count = nullable(offer.sales_count),
        satisfaction = nullable(offer.satisfaction),
        bid_count = nullable(offer.bid_count),
        purchase = nullable(offer.purchase),
        shipping = nullable(offer.shipping),
        country = nullable(offer.country)
    ))

def scrap(subject: str, url: str) -> tuple[ScrapStats, list[Offer]]:
    offers: list[Offer] = []

    logger: Logger = get_logger(subject)
    stats = ScrapStats()

    response = requests.get(url.format(page=1))
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    page: bs4.Tag = soup.find("ol", class_="pagination__items")
    nb_pages: int = 1
    if page:
        nb_pages: int = len(page.find_all("li"))

    for page_index in range(1, nb_pages + 1):
        time.sleep(0.1)

        page_url: str = url.format(page=page_index)
        print(f"Scrapping: {page_url}")
        logger.info(f"Scrapping: {page_url}")

        response = requests.get(page_url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        root: bs4.Tag = soup.find("ul", class_="srp-results srp-list clearfix")
        next(root.children)

        for element in root.children:
            id_tag: str = element.get("id")
            is_new_tag: bs4.Tag = element.find("span", class_="LIGHT_HIGHLIGHT")
            title_tag: bs4.Tag = element.find("div", class_="s-item__title")
            star_tag: bs4.Tag = element.find("div", class_="x-star-rating")
            subtitle_tag: bs4.Tag = element.find("div", class_="s-item__subtitle")
            price_tag: bs4.Tag = element.find("span", class_="s-item__price")
            pseudo_tag: bs4.Tag = element.find("span", class_="s-item__seller-info-text")
            sales_count_tag: bs4.Tag = element.find("span", class_="s-item__seller-info-text")
            satisfaction_tag: bs4.Tag = element.find("span", class_="s-item__seller-info-text")
            bid_count_tag: bs4.Tag = element.find("span", class_="s-item__bids s-item__bidCount")
            purchase_tag: bs4.Tag = element.find("span", class_="s-item__dynamic s-item__purchaseOptionsWithIcon")
            shipping_tag: bs4.Tag = element.find("span", class_="s-item__shipping s-item__logisticsCost")
            country_tag: bs4.Tag = element.find("span", class_="s-item__location s-item__itemLocation")

            if not id_tag or not title_tag:
                stats.skipped += 1
                continue

            now = dt.datetime.now()
            current_date: str = now.strftime("%Y-%m-%d")

            id: Optional[str] = offer.extract_id(id_tag)
            title: Optional[str] = offer.extract_title(title_tag)
            subtitle: Optional[str] = offer.extract_subtitle(subtitle_tag)
            is_new: Optional[str] = offer.extract_is_new(is_new_tag)
            star: Optional[float] = offer.extract_star(star_tag)
            price: Optional[float] = offer.extract_price(price_tag)
            pseudo: Optional[str] = offer.extract_pseudo(pseudo_tag)
            sales_count: Optional[int] = offer.extract_sales_count(sales_count_tag)
            satisfaction: Optional[float] = offer.extract_satisfaction(satisfaction_tag)
            bid_count: Optional[int] = offer.extract_bid_count(bid_count_tag)
            purchase: Optional[str] = offer.extract_purchase(purchase_tag)
            shipping: Optional[str] = offer.extract_shipping(shipping_tag)
            country: Optional[str] = offer.extract_country(country_tag)

            title = title.replace('\'', "_")
            subtitle = subtitle.replace("\'", "_")

            offers.append(Offer(
                id,
                current_date,
                title, 
                subject,
                is_new, 
                star, 
                subtitle, 
                price, 
                pseudo, 
                sales_count, 
                satisfaction, 
                bid_count, 
                purchase, 
                shipping, 
                country
            ))

    return stats, offers

def run(subject: str, url: str, cursor: psycopg.cursor) -> tuple[RunStats, ScrapStats]:
    run_stats = RunStats()   

    scrap_stats, offers = scrap(subject, url)
    for offer in offers:
        run_stats.total += 1
        if exist_offer(cursor, offer):
            run_stats.exist += 1
        else:
            run_stats.added += 1
            insert_offer(cursor, offer)

    return run_stats, scrap_stats