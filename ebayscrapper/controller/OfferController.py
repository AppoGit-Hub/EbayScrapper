#STD

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.model import Offer
from ebayscrapper.controller import (
    AuthorController,
    StarController,
    PurchaseCategoryController
)
from ebayscrapper.service import (
    OfferService,
)

def ensure(cursor: psycopg.cursor, offer: Offer) -> Offer:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(offer, Offer)

    if offer.purchase.exist():
        PurchaseCategoryController.ensure(cursor, offer.purchase)
    if offer.star.exist():
        StarController.ensure(cursor, offer.star)
    if not offer.author.exist():
        offer.author = AuthorController.ensure(cursor, offer.author)

    return OfferService.ensure(cursor, offer)