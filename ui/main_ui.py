import streamlit as st
import sqlite3
import pandas as pd
import json
from datetime import datetime
from utils.calculator import calculate_total

DB_PATH = "db/restaurant.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS menu(
                id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, category TEXT, price REAL, gst REAL
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS orders(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                items TEXT, total REAL, gst REAL, discount REAL, payment_method TEXT, date_time TEXT
                )""")
    
    conn.commit()
    conn.close()

def load_menu():
    return pd.read_csv("data/menu.csv")

def save_order(items, subtotal, gst, discount, total, payment):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO orders(items, total, gst, discount, payment_method, date_time) VALUES (?,?,?,?,?,?)
                """,
    (
        json.dumps(items),
        total, 
        gst, 
        discount, 
        payment, 
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

    conn.commit()
    conn.close()

def run_ui():
    init_db()
    menu_df = load_menu()
    st.subheader("Place an order")

    mode = st.radio("Mode:", ["Takeaway"])
    
    order_items = []
    for i, row in menu_df.iterrows():
        qty = st.number_input(f"{row['item_name']}(₹{row['price']})", min_value=0, step=1, key=row["item_name"])

        if qty > 0:
            order_items.append({
                "name": row['item_name'],
                "price": row['price'],
                "qty": qty,
                "gst": row['gst']
            })

    discount = st.slider("Discount (%)", 0, 50, 0)
    payment = st.radio("Payment Method", ["Cash", "UPI", "Card"])

    if st.button("Generate Bill"):
        if not order_items:
            st.error("⚠️ No items selected.")
        else:
            subtotal, gst_amount, discount_amount, total = calculate_total(order_items, gst=True, discount=discount)

            st.success("✅ Bill Generated")
            st.write("**Subtotal:** ₹", subtotal)
            st.write("**GST:** ₹", gst_amount)
            st.write("**Discount:** ₹", discount_amount)
            st.write("**Total:** ₹", total)

            # Save order
            save_order(order_items, subtotal, gst_amount, discount_amount, total, payment)

            # Export CSV
            bill_df = pd.DataFrame(order_items)
            bill_df.to_csv("data/sales_report.csv", index=False)

            # Export JSON
            with open("data/sample_bills.json", "w") as f:
                json.dump(order_items, f, indent=4)

            