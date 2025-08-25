import sqlite3
import pandas as pd

DB_PATH = "db/restaurant.db"

def get_menu():
    conn = pd.read_sql("SELECT * FROM menu", conn)
    conn.close()
    return df

def save_order(items, quantities, total):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
                   INSERT INTO order(items, quantities, total)
                   VALUES (?, ?, ?)
    """, (str(items), str(quantities), total))
    conn.commit()
    conn.close()
