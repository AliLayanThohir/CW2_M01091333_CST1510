# Week 8: Data Pipeline & CRUD (SQL)
Student Name: Ali Layan Thohir
Student ID: M01091333
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform
## Project Description
This project migrates the functions from Week 7's file-based sytem to a persistent SQLite database. It contains a database with multi-table schema, data migration from week 7 and a pipeline to load CSV's into the database. This system also has full CRUD(Create,Read,Update and Delete) operations for the three domain types of Cybersecurity, Data Science and IT.
## Features
- Migration from textfile to the new SQLite table
- Database authentication
- Multi-Domain Schema
- Data pipeline functionality to read and load CSV
- Fully operational CRUD functionality
- Queries
- Security & Sessions 
## Technical Implementation
- Database: SQLite (intelligence_platform.db).
- Password Security: bcrypt (Hashing and verification).
- Modules: pandas (Used for data loading and queries).
- Database Schema (Tables): 
    - users: Stores user credentials, hashed password and roles for authentification
    - cyber_incidents: Tracks security incidents, it's severity and the status.
    - datasets_metadata: Stores metadata for data science datasets.
    - it_tickets: Logs and stores IT support tickets, their priority and it's status.
    - sessions: Stores active user login tokens 
    - lockout: Tracks failed login attempts in order to lock accounts.

Picture of output of main.py:
<img width="1508" height="1285" alt="image" src="https://github.com/user-attachments/assets/c6de666a-13a3-412c-a081-6ef2de31e781" />
<img width="1712" height="1217" alt="image" src="https://github.com/user-attachments/assets/313acafe-03ee-4eae-a697-f365ac161b35" />
<img width="1672" height="424" alt="image" src="https://github.com/user-attachments/assets/bb1736d1-681b-40d7-9573-5509adcdf096" />


