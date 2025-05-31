# error_handling.py

import logging
import streamlit as st

# Setup logging
logging.basicConfig(
    filename="app.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_exception(e, context=""):
    """Log error ke file log."""
    logging.error(f"{context}: {str(e)}", exc_info=True)

def show_user_error(message):
    """Tampilkan error ke pengguna dengan cara yang ramah."""
    st.error(message)
