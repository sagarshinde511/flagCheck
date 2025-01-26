import streamlit as st

# Set default login credentials
DEFAULT_USERNAME = "admin"
DEFAULT_PASSWORD = "123"

# Page configuration
st.set_page_config(page_title="Login Page", page_icon="🔒", layout="centered")

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Function to display the login form
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
            #st.experimental_rerun()  # Immediately refresh the app to show the dashboard
        else:
            st.error("Invalid username or password.")

# Function to display the dashboard
def dashboard():
    st.title("📊 Dashboard")
    st.write("Welcome to your dashboard!")
    if st.button("Logout"):
        st.session_state.authenticated = False
        #st.experimental_rerun()  # Immediately refresh the app to return to the login page

# Main application flow
if st.session_state.authenticated:
    dashboard()
else:
    login()
