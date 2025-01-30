import streamlit as st
import mysql.connector

# Database Configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1"
}

# Function to verify credentials
def authenticate_user(username, password):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Query to check if user exists
        query = "SELECT * FROM HotelStaff WHERE loginID = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        return user is not None  # Returns True if user exists, else False
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return False

# Streamlit Page Config
st.set_page_config(page_title="Login Page", page_icon="🔒", layout="centered")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login Form
def login():
    st.title("🔒 Login Page")
    st.write("Please log in to access the dashboard.")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if authenticate_user(username, password):
            st.session_state.authenticated = True
            st.session_state.login_username = ""  # Clear username input
            st.session_state.login_password = ""  # Clear password input
            st.rerun()  # Reload app to show dashboard
        else:
            st.error("Invalid username or password.")

# Dashboard
def dashboard():
    st.title("📊 Dashboard")
    st.write("Welcome to your dashboard!")

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()  # Refresh to go back to login page

# Main Application Logic
if st.session_state.authenticated:
    dashboard()
else:
    login()
