# database/connection.py

import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables from the project root .env
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_dotenv(env_path)

# Meta-DB (users & chat history)
META_PARAMS = {
    "host": os.getenv("META_DB_HOST"),
    "port": os.getenv("META_DB_PORT"),
    "dbname": os.getenv("META_DB_NAME"),
    "user": os.getenv("META_DB_USER"),
    "password": os.getenv("META_DB_PASS"),
}

# Data-DB (business queries)
DATA_PARAMS = {
    "host": os.getenv("DATA_DB_HOST"),
    "port": os.getenv("DATA_DB_PORT"),
    "dbname": os.getenv("DATA_DB_NAME"),
    "user": os.getenv("DATA_DB_USER"),
    "password": os.getenv("DATA_DB_PASS"),
}

# SQLAlchemy URI for LangChain’s SQLDatabase
DATA_URI = (
    f"postgresql+psycopg2://"
    f"{DATA_PARAMS['user']}:{DATA_PARAMS['password']}@"
    f"{DATA_PARAMS['host']}:{DATA_PARAMS['port']}/"
    f"{DATA_PARAMS['dbname']}"
)

_meta_conn = None
_data_conn = None

def get_meta_connection():
    """
    Return a psycopg2 connection to the meta-database (users & history).
    """
    global _meta_conn
    if _meta_conn is None or _meta_conn.closed:
        _meta_conn = psycopg2.connect(**META_PARAMS)
    return _meta_conn

def get_data_connection():
    """
    Return a psycopg2 connection to the data-database (business queries).
    """
    global _data_conn
    if _data_conn is None or _data_conn.closed:
        _data_conn = psycopg2.connect(**DATA_PARAMS)
    return _data_conn

if __name__ == "__main__":
    print("META_PARAMS:", META_PARAMS)
    print("DATA_PARAMS:", DATA_PARAMS)
    print("DATA_URI:", DATA_URI)
    api_key = os.getenv("OPENAI_API_KEY", "")
    print("OPENAI_API_KEY repr:", repr(api_key))
    # Optionally: try a dry‐run connection
    # conn = psycopg2.connect(**DATA_PARAMS)
    # print("Connected!", conn)
