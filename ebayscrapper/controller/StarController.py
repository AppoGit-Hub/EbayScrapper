#STD

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.service import StarService
from ebayscrapper.model import Star

def ensure(cursor: psycopg.cursor, star: Star) -> Star:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(star, Star)

    return StarService.ensure(cursor, star)