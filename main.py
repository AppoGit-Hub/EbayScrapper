#STD
import datetime as dt

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.business import SearchStrategy
from ebayscrapper.core import ConnectionSingleton
from ebayscrapper.model import (
    Offer, 
    PurchaseCategory,
    Author,
    Star,
    Country
)
import ebayscrapper.controller.OfferController as OfferController

def scrap_search(url: str):
    assert isinstance(url, str)

    now = dt.datetime.now()
    current_date: str = now.strftime("%Y-%m-%d")

    try:
        connection = ConnectionSingleton.get_instance()
        cursor: psycopg.cursor = connection.cursor()

        for scrap_data in SearchStrategy.scrap(url):
            id: str = scrap_data["id"]
            title: str = scrap_data["title"]

            if not title or not id:
                continue

            print(scrap_data)

            OfferController.ensure(
                cursor, 
                Offer(
                    id,
                    current_date,
                    title,
                    scrap_data["subtitle"],
                    scrap_data["price"],
                    scrap_data["shipping"],
                    PurchaseCategory(
                        scrap_data["purchase"]
                    ),
                    Star(
                        scrap_data["star"]
                    ),
                    Author(
                        None,
                        scrap_data["pseudo"], 
                        Country(
                            scrap_data["country"]
                        )
                    )
                )
            )

        connection.commit()

    except Exception as error:
        print(error)

if __name__ == "__main__":
    scrap_search("RTX")