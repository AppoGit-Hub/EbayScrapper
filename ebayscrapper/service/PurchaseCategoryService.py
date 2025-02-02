#STD
from typing import Optional

#EXTERN
import psycopg2._psycopg as psycopg

#INTERN
from ebayscrapper.core import EXIST_PURCHASECATEGORY, INSERT_PURCHASECATEGORY
from ebayscrapper.model import PurchaseCategory

def get(cursor: psycopg.cursor, pc: PurchaseCategory) -> Optional[PurchaseCategory]:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(pc, PurchaseCategory)

    cursor.execute(EXIST_PURCHASECATEGORY, (
        pc.name, 
    ))

    pc_db: Optional[tuple] = cursor.fetchone()
    return PurchaseCategory(*pc_db) if isinstance(pc_db, tuple) else None

def exists(cursor: psycopg.cursor, pc: PurchaseCategory) -> bool:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(pc, PurchaseCategory)

    cursor.execute(EXIST_PURCHASECATEGORY, (
        pc.name, 
    ))

    return isinstance(cursor.fetchone(), tuple)

def insert(cursor: psycopg.cursor, pc: PurchaseCategory):
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(pc, PurchaseCategory)

    cursor.execute(INSERT_PURCHASECATEGORY, (
        pc.name, 
    ))

def ensure(cursor: psycopg.cursor, pc: PurchaseCategory) -> PurchaseCategory:
    assert isinstance(cursor, psycopg.cursor)
    assert isinstance(pc, PurchaseCategory)

    pc_new: Optional[PurchaseCategory] = get(cursor, pc)
    if not pc_new:
        insert(cursor, pc)
        pc_new: Optional[PurchaseCategory] = get(cursor, pc)
    return pc_new