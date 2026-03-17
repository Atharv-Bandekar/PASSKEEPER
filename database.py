import sqlite3
import os
import config

# Connect to the SQLite database using the dynamic path from config
def get_connection():
    return sqlite3.connect(config.DB_NAME)

# Initialize database tables on startup and handle schema migrations
def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        
        # Table for storing the master PIN
        c.execute('''CREATE TABLE IF NOT EXISTS USER_INFO (pin TEXT NOT NULL)''')
        
        # Main table for storing credentials. 
        c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        website TEXT NOT NULL, 
                        email TEXT, 
                        username TEXT,
                        password TEXT NOT NULL)''')
        
        # MIGRATION LOGIC: Adds username column if it doesn't exist
        c.execute("PRAGMA table_info(passwords)")
        columns = [column[1] for column in c.fetchall()]
        if 'username' not in columns:
            c.execute("ALTER TABLE passwords ADD COLUMN username TEXT DEFAULT ''")
            
        # Table for storing reusable default emails for the dropdown menu
        c.execute('''CREATE TABLE IF NOT EXISTS default_emails (
                        email TEXT NOT NULL)''')
        conn.commit()
    
    # Security feature: Set the database file as read-write for the owner only
    try:
        os.chmod(config.DB_NAME, 0o600) 
    except FileNotFoundError:
        pass 

# Check if a master PIN has already been set up by the user
def user_exists():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER_INFO'")
        if c.fetchone():
            c.execute("SELECT * FROM USER_INFO")
            if c.fetchone():
                return True
    return False

# Save a new master PIN during sign-up
def save_user_pin(pin):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO USER_INFO (pin) VALUES (?)", (pin,))
        conn.commit()

# Verify the entered PIN matches the database during log-in
def verify_pin(pin):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT pin FROM USER_INFO")
        result = c.fetchone()
        return result and pin == result[0]

# Wipe all tables if the user completely deletes their account
def delete_all_user_data():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS USER_INFO")
        c.execute("DROP TABLE IF EXISTS passwords")
        c.execute("DROP TABLE IF EXISTS default_emails")
        conn.commit()

# ------------------- CRUD Operations for Passwords -------------------

# Create a new password entry
def add_password(website, email, username, password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO passwords (website, email, username, password) VALUES (?, ?, ?, ?)",
                  (website, email, username, password))
        conn.commit()

# Read/Search ALL password entries for a given website name
def get_passwords(website):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT email, username, password FROM passwords WHERE website = ?", (website,))
        return c.fetchall() # FETCHALL returns a list of tuples for multiple accounts

# Update a specific password entry using the old email/username to target it precisely
def update_password(website, old_email, old_username, new_email, new_username, new_password):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute('''UPDATE passwords 
                     SET email = ?, username = ?, password = ? 
                     WHERE website = ? AND email = ? AND username = ?''',
                  (new_email, new_username, new_password, website, old_email, old_username))
        conn.commit()

# Delete a specific password entry
def delete_password(website, email, username):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM passwords WHERE website = ? AND email = ? AND username = ?", 
                  (website, email, username))
        conn.commit()

# Fetch all saved records for the 'View All' page
def get_all_saved_websites():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT website, email, username FROM passwords")
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