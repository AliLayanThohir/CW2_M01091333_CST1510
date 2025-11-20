#Import needed to make this module work
import pandas as pd
from app.data.db import connect_database
from datetime import datetime

#Function to create a ticket
def insert_ticket(ticket_id, priority, status, category, subject, description, assigned_to=None):
    conn = connect_database()
    cursor = conn.cursor()
    new_id = None
    created_date = datetime.now().strftime("%Y-%m-%d")
    
    # If creating a ticket that is already resolved, set the resolved date immediately
    resolved_date = None
    if status in ['Resolved', 'Closed']:
        resolved_date = created_date
        
    cursor.execute("""
        INSERT INTO it_tickets 
        (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticket_id, priority, status, category, subject, description, created_date, resolved_date, assigned_to))
    
    conn.commit()
    new_id = cursor.lastrowid
    print(f"✅ Inserted ticket '{ticket_id}' with ID: {new_id}")
    conn.close()
    return new_id

#Read ticket
def get_all_tickets():
    conn = connect_database()
    df = pd.read_sql_query("SELECT * FROM it_tickets ORDER BY id DESC", conn)
    conn.close()
    return df

#Update ticket
def update_ticket_status(ticket_id, new_status, is_resolved=False):
    conn = connect_database()
    cursor = conn.cursor()
    rows_affected = 0
    
    # 1. Get Current Status and Date to make a decision
    cursor.execute("SELECT status, resolved_date FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    row = cursor.fetchone()
    
    if row:
        current_status, current_date = row
        new_resolved_date = current_date # Default to keeping existing date
        
        # LOGIC: If moving TO Resolved/Closed
        if new_status in ['Resolved', 'Closed']:
            # Only update the date if it wasn't ALREADY Resolved/Closed
            # OR if for some reason it was missing a date
            if current_status not in ['Resolved', 'Closed'] or not current_date:
                new_resolved_date = datetime.now().strftime("%Y-%m-%d")
            # If it was already Resolved/Closed, we keep 'current_date' (do nothing to it)
            
        # LOGIC: If moving BACK TO Open/In Progress
        elif new_status in ['Open', 'In Progress', 'Investigating']:
            # Clear the resolved date
            new_resolved_date = None
            
        # Execute the update
        sql = "UPDATE it_tickets SET status = ?, resolved_date = ? WHERE ticket_id = ?"
        params = (new_status, new_resolved_date, ticket_id)
        
        cursor.execute(sql, params)
        conn.commit()
        rows_affected = cursor.rowcount
        
        if rows_affected > 0:
            print(f"✅ Updated status for ticket: {ticket_id} to {new_status} (Date: {new_resolved_date})")
            
    conn.close()
    return rows_affected

#Function to delete ticket
def delete_ticket(ticket_id):
    conn = connect_database()
    cursor = conn.cursor()
    rows_affected = 0
    cursor.execute("DELETE FROM it_tickets WHERE ticket_id = ?", (ticket_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    if rows_affected > 0:
        print(f"✅ Deleted ticket with ID: {ticket_id}")
    conn.close()
    return rows_affected