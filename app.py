import streamlit as st
from ui.main_ui import run_ui

def main():
    st.set_page_config(page_title="Restaurant Billing Software", layout="centered")
    st.title("Restaurant Billing Software")

    run_ui()

if __name__ == "__main__":
    main()