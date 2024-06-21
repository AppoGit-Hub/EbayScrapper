import os
import sys
import time
import json
import logging
from logging import Logger
import datetime as dt
from dataclasses import asdict

import psycopg2
from prometheus_client import start_http_server, Counter

import notify
from scrap import run
from utils import get_json_as
from models import (
    PostgressCredential, 
    MailCredential, 
)
from common import (
    POSTGRESS_CREDENTIAL_FILENAME, 
    MAIL_CREDENTIAL_FILENAME, 
    LOG_DIRECTORY, 
    LINKS_FILENAME,
    LOGNAME_PATTERN
)

def get_logger():
    now = dt.datetime.now()
    current_date: str = now.strftime("%Y-%m-%d")

    log_filename = LOGNAME_PATTERN.format(subject="log", date=current_date) 

    logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=os.path.join(LOG_DIRECTORY, log_filename)
    )

    return logging.getLogger("log")

if __name__ == "__main__":
    skipped = Counter('ebayscrap_skipped', 'skip offer')
    total = Counter('ebayscrap_total', 'total offer')
    exist = Counter('ebayscrap_exist', 'exist offer')
    added = Counter('ebayscrap_added', 'added offer')

    start_http_server(8000)

    if (len(sys.argv)) > 1:
        links_file = sys.argv[1]
        if os.path.exists(links_file) and os.path.isfile(links_file):
            if not os.path.exists(LOG_DIRECTORY):
                os.mkdir(LOG_DIRECTORY)

            postgress = get_json_as(POSTGRESS_CREDENTIAL_FILENAME, PostgressCredential)
            mail = get_json_as(MAIL_CREDENTIAL_FILENAME, MailCredential)
            
            with open(LINKS_FILENAME, "r") as file:
                links: dict = json.loads(file.read())

            wait_time: int = 3
            while True:
                for index in range(wait_time):
                    print(f"Time left: {wait_time - index}s")
                    time.sleep(1)

                logger: Logger = get_logger()

                try:
                    logger.info("Connection to database...")

                    connection = psycopg2.connect(**asdict(postgress))
                    cursor = connection.cursor()

                    logger.info("Connected to database!")
                    logger.info("Scrapping begings...")

                    for subject, link in links.items():
                        scrap_stats, run_stats = run(subject, link, cursor)

                        skipped.inc(run_stats.skipped)
                        
                        total.inc(scrap_stats.total)
                        exist.inc(scrap_stats.exist)
                        added.inc(scrap_stats.added)

                    logger.info(f"Scrapping ended with {json.dumps(asdict(run_stats))}")
                    logger.info("Commit to databse...")
                    
                    connection.commit()
                    
                    logger.info("Scrapping succes !")
                    
                except Exception as error:
                    logger.exception(error)

                    notify.send_message(
                        mail.sender, 
                        mail.password, 
                        mail.receiver, 
                        f"Error ebayscrap with {subject}", 
                        f"Error with {error} with {json.dumps(asdict(run_stats))}"
                    )
                finally:
                    logger.info("Closing database connecion...")

                    if "connection" in locals():
                        connection.close()
                    if "cursor" in locals():
                        cursor.close()

                    logger.info("Database connecion closed !")