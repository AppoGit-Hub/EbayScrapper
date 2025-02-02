#STD
import time
from logging import Logger

#EXTERN
import bs4
import requests

#INTERN
from ebayscrapper.core import get_logger
from ebayscrapper.urlbuilder import SearchUrlBuilder
from ebayscrapper.extractor import (
    pseudo, 
    purchase, 
    bid_count, 
    sales_count, 
    price, 
    title, 
    satisfaction, 
    shipping, 
    star, 
    subtitle,
    country,
    id
)

def scrap(url: str) -> dict[str]:
    assert isinstance(url, str)

    offers: list[dict[str]] = []

    logger: Logger = get_logger("log")

    response = requests.get(SearchUrlBuilder.build(url, page=1))
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    page: bs4.Tag = soup.find("ol", class_="pagination__items")
    nb_pages: int = len(page.find_all("li")) if page else 1

    for page_index in range(1, nb_pages + 1):
        time.sleep(0.1)

        page_url: str = SearchUrlBuilder.build(url, page=page_index)
        print(f"Scrapping: {page_url}")
        logger.info(f"Scrapping: {page_url}")

        response = requests.get(page_url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        """
        with open("index.html", "w") as file:
            file.write(str(response.content))
        """

        root: bs4.Tag = soup.find("ul", class_="srp-results srp-list clearfix")
        next(root.children)

        for element in root.children:
            if not isinstance(element, bs4.Tag):
                continue

            id_tag: str = element.get("id")
            #is_new_tag: bs4.Tag = element.find("span", class_="LIGHT_HIGHLIGHT")
            title_tag: bs4.Tag = element.find("div", class_="s-item__title")
            star_tag: bs4.Tag = element.find("div", class_="x-star-rating")
            subtitle_tag: bs4.Tag = element.find("div", class_="s-item__subtitle")
            price_tag: bs4.Tag = element.find("span", class_="s-item__price")
            bid_count_tag: bs4.Tag = element.find("span", class_="s-item__bids s-item__bidCount")
            shipping_tag: bs4.Tag = element.find("span", class_="s-item__shipping s-item__logisticsCost")
            country_tag: bs4.Tag = element.find("span", class_="s-item__location s-item__itemLocation")
            pseudo_tag: bs4.Tag = element.find("span", class_="s-item__seller-info-text")
            purchase_tag: bs4.Tag = element.find("span", class_="s-item__dynamic s-item__purchaseOptionsWithIcon")
            sales_count_tag: bs4.Tag = element.find("span", class_="s-item__seller-info-text")
            satisfaction_tag: bs4.Tag = element.find("span", class_="s-item__seller-info-text")

            offers.append({
                "id": id(id_tag),
                "title": title(title_tag),
                "star": star(star_tag),
                "subtitle": subtitle(subtitle_tag),
                "price": price(price_tag),
                "bid_count": bid_count(bid_count_tag),
                "shipping": shipping(shipping_tag),
                "country": country(country_tag),
                "pseudo": pseudo(pseudo_tag),
                "purchase": purchase(purchase_tag),
                "sales_count": sales_count(sales_count_tag),
                "satisfaction": satisfaction(satisfaction_tag),
            })
            
    return offers