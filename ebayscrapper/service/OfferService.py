#STD
from typing import Optional

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.model import Offer
from ebayscrapper.core import INSERT_OFFER, EXIST_OFFER

def get(cursor: psycopg.cursor, offer: Offer) -> Optional[Offer]:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(offer, Offer)

    cursor.execute(EXIST_OFFER, (
        offer.id,
    ))

    offer_db: Optional[tuple] = cursor.fetchone()
    return Offer(*offer_db) if isinstance(offer_db, tuple) else None

def exists(cursor: psycopg.cursor, offer: Offer) -> bool:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(offer, Offer)

    cursor.execute(EXIST_OFFER, (
        offer.id,
    ))

    return isinstance(cursor.fetchone(), tuple)

def insert(cursor: psycopg.cursor, offer: Offer):
    assert(isinstance(cursor, psycopg.cursor))
    assert(isinstance(offer, Offer))

    cursor.execute(INSERT_OFFER, (
        offer.id,
        offer.date,
        offer.title,
        offer.subtitle,
        offer.price,
        offer.shipping,
        offer.purchase.name,
        offer.star.value,
        offer.author.id
    ))

def ensure(cursor: psycopg.cursor, offer: Offer) -> Offer:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(offer, Offer)

    offer_new: Optional[Offer] = get(cursor, offer)
    if not offer_new:
        insert(cursor, offer)
        offer_new: Optional[Offer] = get(cursor, offer)
    return offer_new