from tkinter import *
import config
import database

# ---------------------------- View All Saved Websites Page ------------------------------- #
def view_saved_websites_page(window, navigate):
    window.title("Saved Websites")
    # Remove standard padding for this specific view to maximize vertical space for lists
    window.config(padx=0) 
    
    # Fetch all records from the database. Returns a list of tuples: [(web, email, user), ...]
    websites = database.get_all_saved_websites() 

    # Navigation Back Button
    Button(window, text="<-Back", width=22, command=lambda: navigate("dashboard"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=0, column=0, pady=config.ENTRY_PAD)
    
    # Decorative line separator
    line_label = Label(window, text="_______________________________________________________________________________________________", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    line_label.grid(row=1, column=0, columnspan=4, pady=5)

    # Empty state check
    if not websites:
        Label(window, text="No website has been saved yet.", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0, columnspan=4, pady=5)
    else:
        # Enumerate gives us an index (0, 1, 2) to help dynamically place rows in the grid
        for index, (website, email, username) in enumerate(websites):
            
            # Column 0: Website Name
            Label(window, text=website, bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=index + 2, column=0, pady=5)
            
            # Format the output string cleanly based on what data actually exists in the DB
            display_text = ""
            if email and username:
                display_text = f"- Email: {email} | User: {username}"
            elif email:
                display_text = f"- Email: {email}"
            elif username:
                display_text = f"- User: {username}"
                
            # Column 1: Associated Email/Username Info
            Label(window, text=display_text, bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=index + 2, column=1, pady=5, sticky=W)