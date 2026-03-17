# ==========================================
# CONFIGURATION SETTINGS
# Store all global constants and settings here
# ==========================================
import os

# Dynamic Path Resolution
# This finds the absolute path to the directory containing this config.py file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define specific folders
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
DATA_DIR = os.path.join(BASE_DIR, 'data')

# Ensure the data directory exists before the database tries to save there
os.makedirs(DATA_DIR, exist_ok=True)

# File Paths
DB_NAME = os.path.join(DATA_DIR, 'passwords.db')
LOCK_IMG_PATH = os.path.join(ASSETS_DIR, 'lock.png')

# Common constants for UI styling
BLACK = "#040514"
TURQUOISE = "#0ce3c7"
DARK_CHARCOAL = "#333031"
FONT = ("consolas", 10, "normal")
ENTRY_PAD = 7