import os
import json
import time
from dataclasses import fields
from typing import Callable

from models import GenericDataclass, MailCredential, PostgressCredential

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

if __name__ == "__main__":
    print(get_json_as("pg_keys.json", PostgressCredential))
    print(get_json_as("mail_keys.json", MailCredential))