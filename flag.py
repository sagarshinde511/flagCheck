import streamlit as st
import mysql.connector
from mysql.connector import Error
import time

# Database connection details
HOST = "82.180.143.66"
USER = "u263681140_students"
PASSWORD = "testStudents@123"
DATABASE = "u263681140_students"

def get_data():
    """Fetches the value of F1 from the UpdateFlag table where id=1."""
    try:
        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT F1 FROM UpdateFlag WHERE id = 1"
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result["F1"] if result else None
    except Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Streamlit app
st.title("Real-time Database Update")

# Placeholder for dynamic update
data_placeholder = st.empty()

# Auto-refresh every 5 seconds (change as needed)
while True:
    # Fetch the data
    data = get_data()

    # Update the placeholder with the latest data
    if data is not None:
        data_placeholder.success(f"Value of F1: {data}")
    else:
        data_placeholder.warning("No data found or an error occurred.")

    # Wait before refreshing the data
    time.sleep(2)  # Updates every 5 seconds
    st.experimental_rerun()  # Forces the page to re-render
