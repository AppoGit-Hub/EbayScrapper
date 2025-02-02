#STD
import os
import sys
import json
import time
import logging
import logging.handlers
import datetime as dt
from dataclasses import fields, asdict
from typing import Callable

#EXTERN
import psycopg2

#INTERN
from ebayscrapper.model import GenericDataclass, PostgressCredential

#IMPORTS
from .Queries import *
from .Notify import *

LOG_DIRECTORY: str = "./log"
LOGNAME_PATTERN: str = "ebay-{subject}-{date}.log"

MAIL_CREDENTIAL_FILENAME = "mail_keys.json"
POSTGRESS_CREDENTIAL_FILENAME = "pg_keys.json"
LINKS_FILENAME = "links.json"
CONFIG_DATA = "config.json"

def get_json_as(filepath: str, type: GenericDataclass) -> GenericDataclass:
    fullpath: str = os.path.abspath(filepath)
    if not os.path.exists(fullpath):
        raise Exception(f"file {fullpath} doesnt exists")

    if not os.path.isfile(fullpath):
        raise Exception(f"file {fullpath} not a file")
    
    with open(fullpath, 'r') as file:
        data: dict = json.loads(file.read())
    
    type_fields: list = [field.name for field in fields(GenericDataclass)]
    if not set(type_fields) < set(data.keys()):
        raise Exception(f"file must contain {type_fields} fields")

    return type(**data)

def wait(current_time: int, interval: int, wait_time: int) -> tuple[int, bool]:
    time.sleep(interval)
    current_time -= interval
    is_done = current_time <= 0
    return wait_time if is_done else current_time, is_done

def wait_step(wait_time: int, interval: int, on_interval: Callable[..., int]):
    seconds_left: int = 0
    is_done = False
    while not is_done:
        seconds_left, is_done = wait(seconds_left, interval, wait_time)
        if not is_done:
            on_interval(seconds_left)
            continue

def get_logger(subject: str):
    now = dt.datetime.now()
    current_date: str = now.strftime("%Y-%m-%d")

    log_filename = LOGNAME_PATTERN.format(subject=subject, date=current_date) 

    if not os.path.exists(LOG_DIRECTORY):
        os.mkdir(LOG_DIRECTORY)

    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=os.path.join(LOG_DIRECTORY, log_filename)
    )

    return logging.getLogger(subject)

def get_connection(postgress: dict):
    connection = psycopg2.connect(**postgress)
    return connection, connection.cursor()

def nullable(parameter):
    return f"'{parameter}'" if parameter else "NULL"

def notnull(parameter):
    assert(parameter)
    return f"'{parameter}'"

def display_timeleft(subject: str, seconds: int):
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24
    
    sys.stdout.flush()
    print(f"{subject} time left: {days}d, {hours % 24}h, {minutes % 60}m, {seconds % 60}s")


class ConnectionSingleton:
    _connection = None
    def get_instance():
        if ConnectionSingleton._connection == None:
            postgress = get_json_as(POSTGRESS_CREDENTIAL_FILENAME, PostgressCredential)
            ConnectionSingleton._connection = psycopg2.connect(**asdict(postgress))
            ConnectionSingleton._connection.autocommit = False
        return ConnectionSingleton._connection
