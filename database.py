import sqlite3
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    connection = sqlite3.connect('hotel.db')
    connection.row_factory = sqlite3.Row
    try:
        yield connection
    finally:
        connection.close()