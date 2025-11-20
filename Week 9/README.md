# Week 9: Streamlit Web Interface & GUI
Student Name: Ali Layan Thohir
Student ID: M01091333
Course: CST1510 - CW2 - Multi-Domain Intelligence Platform
## Project Description
This project migrates the functionality from Week 8's command-line interface to a web-based Graphical User Interface (GUI) using Streamlit. This system maintains full CRUD (Create, Read, Update and Delete) operations across the three domain types of Cybersecurity, Data Science and IT, accessible through role-based pages.
## Features
- Transformation from CLI to an interactive GUI
- Secure Authentication interface (Login/Register)
- Role-Based Navigation (Sidebar)
- Web forms for data entry and management
## Technical Implementation
- Interface: Streamlit.
- Database: SQLite (intelligence_platform.db).
- Password Security: bcrypt (Hashing and verification).
- Modules: pandas (Data handling), streamlit (UI components and charts).
- Application Structure (Pages):
    - Home: Entry - handling secure user Login and Registration.
    - Dashboard: Displays executive overview,showing overview of all data of 3 tables.
    - Cybersecurity: Interface for reporting, viewing and managing security incidents.
    - Data Science: Interface for viewing, adding and updating dataset metadata.
    - IT Operations: Interface for viewing, creating and managing IT support tickets.