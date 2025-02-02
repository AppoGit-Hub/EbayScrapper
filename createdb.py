#STD
import json

#EXTERN
import psycopg2

#INTERN
from ebayscrapper.core import (
    POSTGRESS_CREDENTIAL_FILENAME
)

if __name__ == "__main__":
    import psycopg2

    with open(POSTGRESS_CREDENTIAL_FILENAME, "r") as file:
        creds: dict = json.load(file)

    connection = psycopg2.connect(**creds)
    cursor = connection.cursor()
    
    resp: str = str(input("Do really want to override the db ? (y/n)"))
    if resp == "y":
        with open("db.sql", "r") as file:
            cursor.execute(file.read())
        
        connection.commit()