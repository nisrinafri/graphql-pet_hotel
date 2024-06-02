import os

import dotenv
import psycopg2

dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn
