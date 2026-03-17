# ==========================================
# MAIN ROUTER
# Initializes Tkinter and manages page navigation
# ==========================================

from tkinter import Tk
import config
import database

# Import all your separated views from the views folder
from views.views_auth import sign_up_page, log_in_page
from views.views_dashboard import add_password_page
from views.views_emails import save_default_emails_page
from views.views_update_delete import update_delete_password_page
from views.views_view_all import view_saved_websites_page

# Initialize the database
database.init_db()

# Main window setup
window = Tk()
window.title("Password Manager")
window.config(bg=config.BLACK)

# Keep a reference to images to prevent garbage collection
window.image_refs = {}

def clear_window():
    # Clear the window (Destroys all current widgets)
    for widget in window.winfo_children():
        widget.destroy()

# Router logic to switch between pages cleanly
def navigate(page_name):
    clear_window()
    
    # Reset default padding (since view_saved_websites changes it)
    window.config(padx=50, pady=50)

    if page_name == "sign_up":
        sign_up_page(window, navigate)
    elif page_name == "log_in":
        log_in_page(window, navigate)
    elif page_name == "dashboard":
        add_password_page(window, navigate)
    elif page_name == "save_emails":
        save_default_emails_page(window, navigate)
    elif page_name == "update_delete":
        update_delete_password_page(window, navigate)
    elif page_name == "view_all":
        view_saved_websites_page(window, navigate)

# Function to check if user exists and Start the application
def start_app():
    if database.user_exists():
        # User exists, show log-in page
        navigate("log_in")
    else:
        # No user, show sign-up page
        navigate("sign_up")

# Calling the app's start logic
start_app()

# Main window loop
window.mainloop()