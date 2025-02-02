import streamlit as st
import mysql.connector
import pandas as pd
from PIL import Image
import io

# Database Configuration
DB_CONFIG = {
    "host": "82.180.143.66",
    "user": "u263681140_students1",
    "password": "testStudents@123",
    "database": "u263681140_students1"
}

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="82.180.143.66",
        user="u263681140_students1",
        password="testStudents@123",
        database="u263681140_students1"
    )
    return connection
def insert_product(name, amount, img_binary, group):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO products (name, amount, img, `group`) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, amount, img_binary, group))
    connection.commit()
    cursor.close()
    connection.close()

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

def RegisterProduct():
    st.title("Product Registration")
    
    # Input fields
    product_name = st.text_input("Product Name")
    product_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    product_image = st.file_uploader("Upload Product Image", type=["jpg", "jpeg", "png"])
    product_group = st.selectbox("Select Group", ["VegStarter","NonVegStarter", "VegMainCource", "NonVegMainCource", "Roti", "Rice", "Beverage"])
    
    if st.button("Register Product"):
        if not product_name:
            st.error("Please enter the product name.")
        elif product_amount <= 0:
            st.error("Please enter a valid amount.")
        elif not product_image:
            st.error("Please upload a product image.")
        elif not product_group:
            st.error("Please select a group.")
        else:
            # Convert uploaded image to binary
            img_binary = product_image.read()
            try:
                # Insert into database
                insert_product(product_name, product_amount, img_binary, product_group)
                st.success("Product registered successfully!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
    

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
        cursor1 = conn1.cursor()
        query1 = "UPDATE HotelOrder SET status = %s WHERE tableNo = %s"
        cursor1.execute(query1, (status, table_no))
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
        elif(username == "admin" and password == "admin"):
            st.session_state.authenticated = True
            st.session_state.user_group = "admin"
            st.rerun()  # Clear the login page and load RegisterProduct()
            RegisterProduct()

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
        status_options = ["Received Order", "Processing", "Preparing Order", "Order Prepared", "Dispatched", "Served"]
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
