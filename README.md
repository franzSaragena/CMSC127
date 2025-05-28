# Student Organization Management System

A simple and efficient command-line-based Student Organization Management System for CMSC 127 at the University of the Philippines Los Baños. This system helps manage memberships, roles, fees, and payments across multiple student organizations.

## Project Summary

This project implements a relational database-driven application for tracking student organization data such as:

- Student information
- Membership status and academic details
- Membership fees, dues and payments
- Fee and payment insights
- Org statistics

The system uses **MariaDB** for the backend database and **Python** for the CLI-based frontend.

---

## Setup Instructions

### Prerequisites
- MariaDB installed and running
- Python 3 installed
- `tabulate` Python package (install with `pip install tabulate`)

### Setup Steps

1. **Login to MariaDB as root:**
   ```bash
   sudo mysql -u root -p
   ```
2. **Run the SQL script to create and populate the database**
    ```sql
    source sql_setup.sql
    ```
3. **Run the main program.**
    ```bash
    python main.py
    ```

## Authors
- **Phea Jamolod** 
- **Bea Patricia Mercado** 
- **Franz Saragena**

> CMSC 127 – File Processing and Database Systems  
> 2nd Semester, AY 2024–2025  
> University of the Philippines Los Baños


