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

def get_item_name_from_db(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM items WHERE item_id = ?", (item_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def upsert_item_name(item_id, name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO items (item_id, name, last_updated)
        VALUES (?, ?, datetime('now'))
        ON CONFLICT(item_id) DO UPDATE SET
            name = excluded.name,
            last_updated = excluded.last_updated
        """,
        (item_id, name))
    conn.commit()
    conn.close()

def insert_median_price(item_id, timestamp, median_price, quantity):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO item_prices (item_id, timestamp, median_price, quantity)
        VALUES (?, ?, ?, ?)
        """,
        (item_id, timestamp, median_price, quantity)
    )

    conn.commit()
    conn.close()

def get_prices_for_item(item_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT timestamp, median_price, quantity
        FROM item_prices
        WHERE item_id = ?
        ORDER BY timestamp ASC
        """,
        (item_id,))

    results = cursor.fetchall()
    conn.close()
    return results

def get_item_id_from_name(name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT item_id
        FROM items
        WHERE name = ?
        COLLATE NOCASE
        """,
        (name,))
    
    results = cursor.fetchall()
    conn.close()
    results = results[0][0]
    return results