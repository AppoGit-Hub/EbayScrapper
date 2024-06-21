

def something():
    import json
    import requests
    from bs4 import BeautifulSoup, Tag

    with open(".\\config\\gameboy.json", 'r') as config_file:
        config_data: dict = json.loads(config_file.read())

    def get_soup(url: str):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
        except Exception:
            raise Exception()

    def extract_page_count(url: str):
        try:
            soup: BeautifulSoup = get_soup(url)
            page: Tag = soup.find("ol", class_="pagination__items")
            return len(page.find_all("li"))
        except Exception:
            raise Exception()

def send_mail():
    from notify import Notify


def db_test():
    import psycopg2, os, json

    try:
        pg_keys_path: str = os.path.abspath("pg_keys.json")
        with open(pg_keys_path, 'r') as key_file:
            pg_keys_data: dict = json.loads(key_file.read())

        connection = psycopg2.connect(
            dbname=pg_keys_data["dbname"], 
            user=pg_keys_data["user"], 
            password=pg_keys_data["password"], 
            host=pg_keys_data["host"], 
            port=pg_keys_data["port"]
        )
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM rtx;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        print(len(rows))
    except Exception as error:
        pass
    finally:
        cursor.close()
        connection.close()

def read_test():
    with open("./asset/rtxs.csv", 'r', encoding="UTF-8") as file:
        print(file.read())

def class_test():
    class SuperObject:
        @property
        def test(self):
            return self._test
        
        @test.setter
        def test(self, value):
            self._test = value

    super = SuperObject()
    super.test = "haha"

    print(super.__dict__)

def format_test():
    print("https://www.ebay.fr/sch/i.html?&_nkw=RTX&_ipg=240&_pgn={page}".format(page=1))

def reset_db_test():
    import psycopg2, json, os

    pg_keys_path: str = os.path.abspath("pg_keys.json")
    with open(pg_keys_path, 'r') as key_file:
        pg_keys_data: dict = json.loads(key_file.read())

    connection = psycopg2.connect(
        dbname=pg_keys_data["dbname"], 
        user=pg_keys_data["user"], 
        password=pg_keys_data["password"], 
        host=pg_keys_data["host"], 
        port=pg_keys_data["port"]
    )

    cursor = connection.cursor()
    with open("db.sql", "r") as file:
        sql_command = file.read()
        cursor.execute(sql_command)
    connection.commit()

def select_db_test():
    import psycopg2

    connection = psycopg2.connect(
        dbname='postgres', 
        user='myuser', 
        password='mypassword', 
        host='localhost', 
        port='5432'
    )
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM rtx WHERE id = '405bc449e8';")
    rows = cursor.fetchone()
    for row in rows:
        print(row)

def logging_test():
    import logging

    logging.basicConfig(
        filename="log.txt", 
        level=logging.DEBUG, 
        format='%(asctime)s [%(levelname)s] - %(message)s'
    )

    logger = logging.getLogger("logger")

    logger.critical("critical")
    logger.error("error")
    logger.warning("warning")
    logger.info("info")
    logger.debug("debug")

def dict_look_test():
    from dataclasses import dataclass, fields

    @dataclass
    class User:
        user: str
        password: str

    print([field.name for field in fields(User)])

    data = {
        "user" : "myuser",
        "password" : "mypassword"
    }

    other = {
        "user" : "otheruser",
        "password": "mypassword",
        "link": "linkedin"
    }

    print(set(data.keys()) < set(other.keys()))
    print(set([field.name for field in fields(User)]) < set(other.keys()))