# db_config.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",    # Use your MySQL root password
        database="profgps"  # Make sure this DB exists
    )