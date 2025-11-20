#CST1510 - Programming for Data Communication and Networks
#Coursework 2 - Multi-Domain Intelligence Platform
#Ali Layan Thohir - M01091333 - Week 9 - Streamlit Interfact

#Importing libraries / needed items to run homepage
import streamlit as st
from app.services.user_service import (
    login_user, 
    register_user, 
    validate_user, 
    validate_pass, 
    check_password_strength
)
from app.data.db import connect_database, DATA_DIR
from app.data.schema import create_all_tables
from app.services.user_service import migrate_users_from_file
from app.utils.navigation import make_sidebar
from app.data.users import get_user_by_username

#Page configuration, Icon, Title and it's layout
st.set_page_config(page_title="Intelligence Platform", page_icon="🔐", layout="centered")

#Function to setup database
@st.cache_resource
def system_startup():
    print("--- Initializing Database Setup ---")
    conn = connect_database()
    create_all_tables(conn)
    users_txt_path = DATA_DIR / "users.txt"
    migrate_users_from_file(users_txt_path)
    print("--- Database Setup Complete ---")

#Run the setup once when the script starts
system_startup()

#Initializing session state variables if they don't exist yet
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""

#Render Sidebar
make_sidebar()

#Title and Introduction for the main page
st.title("🔐 Multi-Domain Intelligence Platform")

#If user is logged in
if st.session_state.logged_in:
    st.success(f"You are currently logged in as **{st.session_state.username}** ({st.session_state.role}).")
    st.info("Use the sidebar 🧭 to navigate to your modules.")
#If user is not logged in
else:
    st.write("Welcome! Please login or register to access the dashboard.")
    #Menu/Start-up display for registration/login
    tab1, tab2 = st.tabs(["Login", "Register"])

    #If user wants to login to an existing account
    with tab1:
        st.header("Login")
        #Username - input
        login_user_input = st.text_input("Username", key="login_user")
        #Password - input
        login_pass_input = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", type="primary"):
            #Check if inputs are provided
            if login_user_input and login_pass_input:
                #Login user function called and checked using the inputs given above
                success, msg = login_user(login_user_input, login_pass_input)
                #If login successful, updates session state and redirects
                if success:
                    # Fetch User Role to store in session
                    user_details = get_user_by_username(login_user_input)
                    # user_details structure: (id, username, password_hash, role, created_at)
                    user_role = user_details[3] if user_details else "User"
                    
                    st.session_state.logged_in = True
                    st.session_state.username = login_user_input
                    st.session_state.role = user_role
                    
                    st.success(msg)
                    st.switch_page("pages/1_Dashboard.py")
                #If unsuccessful displays error message
                else:
                    st.error(msg)
            #If fields are empty
            else:
                st.warning("Please enter both username and password.")

    #If user wants to register a new account
    with tab2:
        #Display of function
        st.header("Register")
        
        #Username - input
        reg_user_input = st.text_input("Choose Username", key="reg_user")
        #Password - input
        reg_pass_input = st.text_input("Choose Password", type="password", key="reg_pass")
        reg_confirm_input = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        #Group to be assigned to
        group_choice = st.selectbox(
            "Select Department",
            ("Cybersecurity Analyst", "Data Scientist", "IT Administrator")
        )
        group_map = {
            "Cybersecurity Analyst": 1,
            "Data Scientist": 2,
            "IT Administrator": 3
        }
        
        if st.button("Create Account"):
            #Check for empty fields
            if not reg_user_input or not reg_pass_input:
                st.warning("Please fill in all fields.")
            
            #Check for password mismatch
            elif reg_pass_input != reg_confirm_input:
                st.error("Passwords do not match.")
            
            else:
                #Validation check for username using predefined function
                valid_user, user_msg = validate_user(reg_user_input)
                #If username is invalid
                if not valid_user:
                    st.error(user_msg)
                else:
                    #Validation check for password using predefined function
                    valid_pass, pass_msg = validate_pass(reg_pass_input)
                    #If password is invalid
                    if not valid_pass:
                        st.error(pass_msg)
                    else:
                        #Password strength check using predefined function
                        strength = check_password_strength(reg_pass_input)
                        #If password strength is not strong
                        if strength != "Strong":
                            st.warning(f"Password Strength: {strength}")
                            st.info("Password must be Strong (Min 12 chars, Upper, Lower, Digit, Special).")
                        else:
                            #If all validations are passed, registers user and prints confirmation
                            success, msg = register_user(reg_user_input, reg_pass_input, group_map[group_choice])
                            
                            if success:
                                st.success(msg + " Please switch to the Login tab.")
                            else:
                                st.error(msg)