#Imports needed to make sure this module works
import streamlit as st
from time import sleep

#Function to create sidebar
def make_sidebar():
    with st.sidebar: #In the sidebar
        #Title of the sidebar
        st.title("🧭 Navigation")
        
        #Page switch to go back to homepage, with the name as 'Home' and icon for it
        st.page_link("Home.py", label="Home", icon="🏠")
        
        #Link that'll show for logged in users
        if st.session_state.get("logged_in", False):
            
            #Subheader for sidebar
            st.subheader("Modules")
            #Page link to go to Dashboard which is available for all users
            st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="📊")
            
            #Variable needed to check what role the logged in user current is
            role = st.session_state.get("role", "")
            
            #Shows the Cybersecurity page - Only to Cybersecurity Analysts
            if role == "Cybersecurity Analyst":
                st.page_link("pages/2_Cybersecurity.py", label="Cybersecurity", icon="🔒")
            
            #Shows the Data Science page - Only to Data Scientists
            if role == "Data Scientist":
                st.page_link("pages/3_Data_Science.py", label="Data Science", icon="📈")
                
            #Shows the IT Operations page - Only to IT Administrators
            if role == "IT Administrator":
                st.page_link("pages/4_IT_Operations.py", label="IT Operations", icon="⚙️")
            
            #Button to Logout and reset states back to default
            st.divider()
            if st.button("Log Out", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.role = ""
                st.success("Logged out successfully!")
                #Pauses execution of any code for specified time, in this case used to show logout message
                sleep(1)
                #Switches back to homepage
                st.switch_page("Home.py")
        
        #If the user isn't logged in, displays message and only "Home" on the sidebar
        elif st.session_state.get("logged_in") is False:
            st.info("Please log in to access modules.")