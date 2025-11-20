#Importing libraries / needed items to show data science interface
import streamlit as st
from datetime import date
from app.data.datasets import (
    get_all_datasets, insert_dataset, delete_dataset, 
    update_dataset_record_count
)
from app.utils.navigation import make_sidebar

##Page configuration, Icon, Title and it's layout
st.set_page_config(page_title="Data Science", page_icon="📈", layout="wide") # Page setup

#Display sidebar
make_sidebar()

#Page title
st.title("📈 Data Science Hub")

#Splits into two different columns
col1, col2 = st.columns([2, 1])

#Allows for viewage of Datasets, shows table with all data
with col1:
    st.subheader("Available Datasets")
    df = get_all_datasets()
    st.dataframe(df, use_container_width=True)

#Section to add new datasets
with col2:
    #Subheader for adding
    st.subheader("Add New Dataset")
    with st.form("dataset_form"):
        ds_name = st.text_input("Dataset Name") #Name of the dataset
        ds_cat = st.selectbox("Category", ["Financial", "Operational", "Customer", "Security"]) #Category of the dataset
        ds_source = st.text_input("Source") #Source where data came from
        ds_date = st.date_input("Last Updated", value=date.today()) #Automatically puts current date
        ds_count = st.number_input("Record Count", min_value=0) #Count of records
        ds_size = st.number_input("Size (MB)", min_value=0.0, format="%.2f") #Size of the file
        
        #Button so the dataset is added
        if st.form_submit_button("Add Dataset"):
            #Inserts dataset data
            insert_dataset(ds_name, ds_cat, ds_source, str(ds_date), ds_count, ds_size)
            st.success("Dataset added.") #Print message to show that it has been added
            st.rerun() #Refreshes automatically so table is updated

#Seperator for page format
st.divider()

#Section to manage datasets
st.subheader("Manage Datasets")

#Only shows up if data exists
if not df.empty:
    #Selection of which dataset by it's ID number
    selected_id = st.selectbox("Select Dataset ID", df['id'].tolist())
    current_ds = df[df['id'] == selected_id].iloc[0]
    
    #Splits to two sections, update or delete
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        with st.form("upd_form"):
            #For updating count of the records
            new_count = st.number_input("New Record Count", value=int(current_ds['record_count']))
            if st.form_submit_button("Update Count"):
                update_dataset_record_count(selected_id, new_count)
                st.success("Updated.") #Print message to show it updated
                st.rerun() #Refreshes automatically so table is updated
    with col_m2:
        st.write("Delete")
        if st.button("Delete Dataset", type="primary"):
            delete_dataset(selected_id)
            st.rerun() #Refreshes automatically so table is updated