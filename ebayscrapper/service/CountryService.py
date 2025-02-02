#STD
from typing import Optional

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.core import INSERT_COUNTRY, EXIST_COUNTRY
from ebayscrapper.model import Country

def get(cursor: psycopg.cursor, country: Country) -> Optional[Country]:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(country, Country)

    cursor.execute(EXIST_COUNTRY, (
        country.name, 
    ))

    country_db: Optional[tuple] = cursor.fetchone()
    return Country(*country_db) if isinstance(country_db, tuple) else None

def exists(cursor: psycopg.cursor, country: Country) -> bool:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(country, Country)

    cursor.execute(EXIST_COUNTRY, (
        country.name, 
    ))

    return isinstance(cursor.fetchone(), tuple)

def insert(cursor: psycopg.cursor, country: Country):
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(country, Country)

    cursor.execute(INSERT_COUNTRY, (
        country.name, 
    ))

def ensure(cursor: psycopg.cursor, country: Country) -> Country:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(country, Country)

    country_new: Optional[Country] = get(cursor, country)
    if not country_new: #doesnt exists
        insert(cursor, country)
        country_new: Optional[Country] = get(cursor, country)
    return country_new