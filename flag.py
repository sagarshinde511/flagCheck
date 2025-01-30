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

# Function to fetch orders
def fetch_orders(user_group):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
        SELECT tableNo AS 'Table No.', 
               Product AS 'Product', 
               quantity AS 'Quantity',
               status AS 'Status'

        FROM HotelOrder 
        WHERE `group` = %s
        """
        cursor.execute(query, (user_group,))
        orders = cursor.fetchall()

        cursor.close()
        conn.close()

        if orders:
            return pd.DataFrame(orders, columns=['Table No.', 'Product', 'Quantity', 'Status'])
        else:
            return None
    except mysql.connector.Error as err:
        st.error(f"Database error: {err}")
        return None

# Function to update order status
def update_order_status(table_no, status):
    try:

        conn1 = mysql.connector.connect(**DB_CONFIG)
        cursor1 = conn.cursor()
        query1 = "UPDATE HotelOrder SET status = %s WHERE tableNo = %s"
        cursor1.execute(query, (status, table_no))
        conn1.commit()
        cursor1.close()
        conn1.close()

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()        
        query = "UPDATE FinalOrder SET Status = %s WHERE orderNo = %s"
        cursor.execute(query, (status, table_no))
        conn.commit()
        cursor.close()
        conn.close()
        
        st.success("Order status updated successfully!")
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
            st.rerun()
        else:
            st.error("Invalid username or password.")

# Dashboard
def dashboard():
    st.title("📊 Dashboard")
    st.write(f"Welcome! Your group: **{st.session_state.user_group}**")

    # Fetch and display orders
    orders_df = fetch_orders(st.session_state.user_group)
    if orders_df is not None:
        st.table(orders_df)

        # Order status update section
        table_numbers = orders_df['Table No.'].unique().tolist()
        selected_table = st.selectbox("Select Table Number", table_numbers)
        status_options = ["Received Order", "Processing", "Preparing Order", "Order Prepared", "Dispatched"]
        selected_status = st.selectbox("Update Order Status", status_options)

        if st.button("Update Status"):
            update_order_status(selected_table, selected_status)
            st.rerun()
    else:
        st.write("No orders found for your group.")

# Main Application Logic
if st.session_state.authenticated:
    dashboard()
else:
    login()
