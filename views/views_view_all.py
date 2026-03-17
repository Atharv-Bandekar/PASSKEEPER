from tkinter import *
import config
import database

# ---------------------------- view_saved_websites ------------------------------- #
def view_saved_websites_page(window, navigate):
    window.title("Saved Websites")
    window.config(padx=0)  # Remove padding for this specific view to maximize space
    
    # Fetching all saved websites from the database
    websites = database.get_all_saved_websites() # This returns a list of tuples

    # back Button
    Button(window, text="<-Back", width=22, command=lambda: navigate("dashboard"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=0, column=0, pady=config.ENTRY_PAD)
    
    line_label = Label(window, text="_______________________________________________________________________________________________", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    line_label.grid(row=1, column=0, columnspan=4, pady=5)

    # If there are no saved websites
    if not websites:
        Label(window, text="No website has been saved yet.", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0, columnspan=4, pady=5)
    else:
        # Display websites using Labels
        for index, (website, email) in enumerate(websites):
            Label(window, text=website, bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=index + 2, column=0, pady=5)
            Label(window, text=f"- {email}", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=index + 2, column=1, pady=5)