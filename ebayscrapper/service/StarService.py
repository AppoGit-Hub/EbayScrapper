#STD
from typing import Optional

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.core import INSERT_STAR, EXIST_STAR
from ebayscrapper.model import Star

def get(cursor: psycopg.cursor, star: Star) -> Optional[Star]:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(star, Star)

    cursor.execute(EXIST_STAR, (
        star.value, 
    ))

    star_db: Optional[tuple] = cursor.fetchone()
    return Star(*star_db) if isinstance(star_db, tuple) else None

def exists(cursor: psycopg.cursor, star: Star) -> bool:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(star, Star)

    cursor.execute(EXIST_STAR, (
        star.value, 
    ))

    return isinstance(cursor.fetchone(), tuple)

def insert(cursor: psycopg.cursor, star: Star):
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(star, Star)

    cursor.execute(INSERT_STAR, (
        star.value, 
    ))

def ensure(cursor: psycopg.cursor, star: Star) -> Star:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(star, Star)

    star_new: Optional[Star] = get(cursor, star)
    if not star_new:
        insert(cursor, star)
        star_new: Optional[Star] = get(cursor, star)
    return star_new