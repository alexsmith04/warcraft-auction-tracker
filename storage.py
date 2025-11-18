import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ah_data.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():

    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

def insert_median_price(item_id, timestamp, median_price):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO item_prices (item_id, timestamp, median_price)
        VALUES (?, ?, ?)
        """,
        (item_id, timestamp, median_price)
    )

    conn.commit()
    conn.close()

def get_prices_for_item(item_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, median_price
        FROM item_prices
        WHERE item_id = ?
        ORDER BY timestamp ASC
        """,
        (item_id,))

    results = cursor.fetchall()
    conn.close()
    return results