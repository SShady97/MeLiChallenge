import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def conexion():
    try:
        params = {
            "host": os.getenv('DB_HOST'),
            "database": os.getenv('DB_NAME'),
            "user": os.getenv('DB_USER'),
            "password": os.getenv('DB_PASSWORD'),
            "port": os.getenv('DB_PORT')
        }
        return psycopg2.connect(**params)
    except psycopg2.Error as e:
        print("Ocurrió un error al conectar a PostgreSQL: ", e)