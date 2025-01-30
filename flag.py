import streamlit as st
import mysql.connector
import pandas as pd

# Database Configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1"
}

# Function to authenticate user and fetch their group
def authenticate_user(username, password):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Fix: Use backticks for `group` column
        query = "SELECT `group` FROM HotelStaff WHERE loginID = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            return user[0]  # Return group
        else:
            return None
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None
def fetch_orders(user_group):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT tableNo AS 'Table No.', 
               Product AS 'Product', 
               quantity AS 'Quantity'
        FROM HotelOrder 
        WHERE `group` = %s
        """
        cursor.execute(query, (user_group,))
        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        # Convert the orders into a Pandas DataFrame
        if orders:
            df = pd.DataFrame(orders, columns=['Table No.', 'Product', 'Quantity',])

            # Display the DataFrame as a table
            st.table(df)  # Display data as a table
        else:
            st.write("No orders found for the selected group.")

    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")

# Streamlit Page Config
st.set_page_config(page_title="Login Page", page_icon="🔒", layout="centered")

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_group" not in st.session_state:
    st.session_state.user_group = ""

# Login Form
def login():
    st.title("🔒 Login Page")
    st.write("Please log in to access the dashboard.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_group = authenticate_user(username, password)
        if user_group:
            st.session_state.authenticated = True
            st.session_state.user_group = user_group  # Store user's group
            st.rerun()  # Reload app to show dashboard
        else:
            st.error("Invalid username or password.")

# Dashboard
def dashboard():
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.user_group = ""
        st.rerun()  # Refresh to go back to login page

    st.title("📊 Dashboard")
    st.write(f"Welcome! Your group: **{st.session_state.user_group}**")

    # Fetch and display orders for this user's group
    orders = fetch_orders(st.session_state.user_group)
    if orders:
        st.write("### Orders for Your Group:")
        for order in orders:
            st.write(order)  # Display each order
    #else:
    #    st.write("No orders found for your group.")


# Main Application Logic
if st.session_state.authenticated:
    dashboard()
else:
    login()
