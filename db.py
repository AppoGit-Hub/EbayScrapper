import psycopg2, json, os

from common import POSTGRESS_CREDENTIAL_FILENAME

def create_db():
    postgress_path: str = os.path.abspath(POSTGRESS_CREDENTIAL_FILENAME)
    with open(postgress_path, 'r') as key_file:
        postgress_data: dict = json.loads(key_file.read())

    connection = psycopg2.connect(**postgress_data)
    cursor = connection.cursor()
    
    with open("db.sql", "r") as file:
        cursor.execute(file.read())
    
    connection.commit()

create_db()