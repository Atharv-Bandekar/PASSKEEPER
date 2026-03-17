import sqlite3
import os
import config

# Connect to the SQLite database
def get_connection():
    return sqlite3.connect(config.DB_NAME)

# Initialize database tables on startup
def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS USER_INFO (pin TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        website TEXT NOT NULL, 
                        email TEXT NOT NULL, 
                        password TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS default_emails (
                        email TEXT NOT NULL)''')
        conn.commit()
    
    # Set the file as read-write for admin only (User-only access)
    try:
        os.chmod(config.DB_NAME, 0o600) 
    except FileNotFoundError:
        pass 

# Function to check if user exists
def user_exists():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER_INFO'")
        if c.fetchone():
            # Table exists, check if there's a user
            c.execute("SELECT * FROM USER_INFO")
            if c.fetchone():
                return True
    return False

# Save a new user PIN
def save_user_pin(pin):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO USER_INFO (pin) VALUES (?)", (pin,))
        conn.commit()

# Verify the entered PIN matches the database
def verify_pin(pin):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT pin FROM USER_INFO")
        result = c.fetchone()
        return result and pin == result[0]

# Wipe all data if user deletes account
def delete_all_user_data():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS USER_INFO")
        c.execute("DROP TABLE IF EXISTS passwords")
        c.execute("DROP TABLE IF EXISTS default_emails")
        conn.commit()

# ------------------- CRUD Operations for Passwords -------------------

def add_password(website, email, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
                  (website, email, password))
        conn.commit()

def get_password(website):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT email, password FROM passwords WHERE website = ?", (website,))
        return c.fetchone()

def update_password(website, new_email, new_password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("UPDATE passwords SET email = ?, password = ? WHERE website = ?",
                  (new_email, new_password, website))
        conn.commit()

def delete_password(website):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM passwords WHERE website = ?", (website,))
        conn.commit()

def get_all_saved_websites():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT website, email FROM passwords")
        return c.fetchall()

# ------------------- Default Emails Operations -------------------

def add_default_email(email):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO default_emails (email) VALUES (?)", (email,))
        conn.commit()

def get_default_emails():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT email FROM default_emails")
        return [row[0] for row in c.fetchall()]