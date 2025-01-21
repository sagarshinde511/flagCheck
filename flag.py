import streamlit as st
import mysql.connector
from mysql.connector import Error

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
st.title("Database Reader")

st.subheader("Fetching data from the database...")
data = get_data()

if data is not None:
    st.success(f"Value of F1: {data}")
else:
    st.warning("No data found or an error occurred.")
