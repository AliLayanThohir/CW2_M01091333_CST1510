#Importing libraries / needed items to show IT Operations interface
import streamlit as st
from app.data.tickets import (
    get_all_tickets, insert_ticket, delete_ticket, update_ticket_status
)
from app.utils.navigation import make_sidebar

##Page configuration, Icon, Title and it's layout
st.set_page_config(page_title="IT Ops", page_icon="⚙️", layout="wide") # Page setup

#Display sidebar
make_sidebar()

#Page title
st.title("⚙️ IT Operations & Ticketing")

#Sidebar filters
with st.sidebar:
    st.header("Filters")
    status_filter = st.multiselect("Status", ["Open", "Closed", "Resolved"], default=["Open"]) #Filter by status

df = get_all_tickets()
#Filters data based on selection
if not df.empty and status_filter:
    df = df[df['status'].isin(status_filter)]

#Allows for viewage of Tickets, shows table with all data
st.metric("Visible Tickets", len(df))
st.dataframe(df, use_container_width=True)

#Seperator for page format
st.divider()

#Creates tabs for each action
tab_new, tab_update = st.tabs(["Create Ticket", "Update/Delete"])

#Tab to create tickets
with tab_new:
    with st.form("ticket_form"):
        #Splits into two different columns
        c1, c2 = st.columns(2)
        with c1:
            t_id = st.text_input("Ticket ID") #ID of the ticket
            t_subject = st.text_input("Subject") #Subject of the ticket
            t_cat = st.selectbox("Category", ["Hardware", "Software", "Network"]) #Category of the ticket
        with c2:
            t_pri = st.selectbox("Priority", ["Low", "Medium", "High"]) #Priority of the ticket
            t_stat = st.selectbox("Status", ["Open", "In Progress", "Closed"]) #Status of the ticket
            t_assign = st.text_input("Assigned To") #Who the ticket is assigned to
        t_desc = st.text_area("Description") #Description of the ticket
        
#Button so the ticket is created
        if st.form_submit_button("Submit"):
            success = False #Flag to track if insertion was successful
            try:
                #Inserts ticket data
                insert_ticket(t_id, t_pri, t_stat, t_cat, t_subject, t_desc, t_assign)
                st.success("Created.") #Print message to show that it has been created
                success = True #Mark as successful
            except Exception as e:
                st.error(f"Error creating ticket: {e}") #Print specific error message
            #Check if success is true
            if success:
                st.rerun() #Refreshes automatically so table is updated (Must be outside try block)

#Tab to manage tickets
with tab_update:
    df_all = get_all_tickets()
    #Only shows up if data exists
    if not df_all.empty:
        #Selection of which ticket by it's ID number
        tid = st.selectbox("Select Ticket ID", df_all['ticket_id'].tolist())
        #Splits to two sections, update or delete
        col_u, col_d = st.columns(2)
        with col_u:
            #For updating status of the ticket
            new_st = st.selectbox("New Status", ["Open", "In Progress", "Resolved", "Closed"], key="ns")
            is_res = new_st in ['Resolved', 'Closed']
            if st.button("Update Status"):
                update_ticket_status(tid, new_st, is_resolved=is_res)
                st.success("Updated.") #Print message to show that it has been updated
                st.rerun() #Refreshes automatically so table is updated
        with col_d:
            if st.button("Delete Ticket", type="primary"):
                delete_ticket(tid)
                st.rerun() #Refreshes automatically so table is updated