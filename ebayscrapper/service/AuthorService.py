#STD
from typing import Optional

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.core import INSERT_AUTHOR, EXIST_AUTHOR
from ebayscrapper.model import Author

def get(cursor: psycopg.cursor, author: Author) -> Optional[Author]:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(author, Author)

    cursor.execute(EXIST_AUTHOR, (
        author.pseudo, 
    ))

    author_db: Optional[tuple] = cursor.fetchone()
    return Author(*author_db) if isinstance(author_db, tuple) else None

def exists(cursor: psycopg.cursor, author: Author) -> bool:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(author, Author)

    cursor.execute(EXIST_AUTHOR, (
        author.pseudo, 
    ))

    return isinstance(cursor.fetchone(), tuple)

def insert(cursor: psycopg.cursor, author: Author):
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(author, Author)

    cursor.execute(INSERT_AUTHOR, (
        author.pseudo, 
        author.country.name, 
    ))

def ensure(cursor: psycopg.cursor, author: Author) -> Author:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(author, Author)

    author_new: Optional[Author] = get(cursor, author)
    if not author_new:
        insert(cursor, author)
        author_new: Optional[Author] = get(cursor, author)
    return author_new