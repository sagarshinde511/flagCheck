import streamlit as st

# Set default login credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "admin"

# Page configuration
st.set_page_config(page_title="Login Page", page_icon="🔒", layout="centered")

# Create a session state for user authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login form
def login():
    st.title("🔒 Login Page")
    st.write("Please log in to access the dashboard.")

    # Create input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        # Check credentials
        if username == DEFAULT_USERNAME and password == DEFAULT_PASSWORD:
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

# Dashboard
def dashboard():
    st.title("📊 Dashboard")
    st.write("Welcome to your dashboard!")
    st.button("Logout", on_click=logout)

# Logout functionality
def logout():
    st.session_state.authenticated = False

# Main application flow
if st.session_state.authenticated:
    dashboard()
else:
    login()
