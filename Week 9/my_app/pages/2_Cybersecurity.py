#Importing libraries / needed items to show cybersecurity interface
import streamlit as st 
from datetime import date 
from app.data.incidents import (
    get_all_incidents, insert_incident, delete_incident,
    update_incident_status, get_incidents_by_type_count,
    get_high_severity_by_status
)
from app.utils.navigation import make_sidebar 

##Page configuration, Icon, Title and it's layout
st.set_page_config(page_title="Cybersecurity", page_icon="🔒", layout="wide") # Page setup

#Display sidebar
make_sidebar() 

#Page title
st.title("🔒 Cybersecurity Operations") 

#Creates tabs for each action
tab_view, tab_analytics, tab_add, tab_manage = st.tabs(["View Log", "Analytics", "Report Incident", "Manage Records"]) 

#Allows for viewage of Log data, shows table with all data
with tab_view:
    st.subheader("Incident Log") 
    df = get_all_incidents() 
    st.dataframe(df, use_container_width=True) 

#Shows analytical data of all the incidents
with tab_analytics: 
    st.subheader("Incident Analytics") 
    #Splits into two different columns
    col1, col2 = st.columns(2) 
    with col1:
        #Bar chart with type of incidents
        st.markdown("**Incidents by Type**") 
        df_type = get_incidents_by_type_count() 
        if not df_type.empty:
             st.bar_chart(df_type.set_index("incident_type")) 
    with col2:
        #Shows data table of incidents by their 
        st.markdown("**High Severity by Status**") 
        df_high = get_high_severity_by_status() 
        st.dataframe(df_high, use_container_width=True) 

#Tab to add incidents
with tab_add: 
    #Subheader for adding
    st.subheader("Report New Incident") 
    with st.form("incident_form"): 
        inc_date = st.date_input("Date", value=date.today()) #Automatically puts current date for incident
        inc_type = st.selectbox("Type", ["Phishing", "Malware", "DDoS", "Intrusion", "Other"]) #What type of incident
        inc_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"]) #Severity of the incident
        inc_status = st.selectbox("Status", ["Open", "Investigating", "Resolved"]) #Status of the incident
        inc_desc = st.text_area("Description") #Description of the incident
        
        #Button so the incident is logged
        if st.form_submit_button("Submit Report"):
            #Inserts incident data along with current logged in users name as the user who logged it
            insert_incident(str(inc_date), inc_type, inc_severity, inc_status, inc_desc, st.session_state.username) 
            st.success("Incident reported successfully!") #Print message to show that it has been logged
            st.rerun() #Refreshes automatically so table is updated

#Tab to manage incidents
with tab_manage: 
    st.subheader("Manage Incidents") 
    df = get_all_incidents() 
    #Only shows up if data exists
    if not df.empty: 
        #Selection of which incident by it's ID number
        incident_id = st.selectbox("Select Incident ID", df['id'].tolist()) 
        #Splits to two sections, update or delete
        col_up, col_del = st.columns(2) 
        with col_up:
            #For updating status of the incident
            new_status = st.selectbox("New Status", ["Open", "Investigating", "Resolved"], key="stat") 
            if st.button("Update Status"):
                update_incident_status(incident_id, new_status) 
                st.success("Status updated.") 
                st.rerun() #Refreshes automatically so table is updated
        with col_del:
            if st.button("Delete Incident", type="primary"): 
                delete_incident(incident_id) 
                st.rerun() #Refreshes automatically so table is updated