#STD

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.service import AuthorService, CountryService
from ebayscrapper.model import Author

def ensure(cursor: psycopg.cursor, author: Author) -> Author:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(author, Author)

    if author.country.name:
        CountryService.ensure(cursor, author.country)
    return AuthorService.ensure(cursor, author)