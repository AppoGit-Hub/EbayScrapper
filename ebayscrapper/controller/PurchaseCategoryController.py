#STD

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.service import PurchaseCategoryService
from ebayscrapper.model import PurchaseCategory

def ensure(cursor: psycopg.cursor, pc: PurchaseCategory) -> PurchaseCategory:
    return PurchaseCategoryService.ensure(cursor, pc)