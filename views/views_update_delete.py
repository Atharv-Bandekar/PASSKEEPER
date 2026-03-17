from tkinter import *
from tkinter import messagebox, ttk
import config
import database

# ---------------------------- Update / Delete Page ------------------------------- #
def update_delete_password_page(window, navigate):
    window.title("update/delete passwords")

    # Canvas and Logo Image
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH) 
        canvas = Canvas(window, width=250, height=200, highlightthickness=0, bg=config.BLACK)
        canvas.create_image(175, 100, image=window.image_refs['lock_img'])
        canvas.grid(row=0, column=1)
    except Exception as e: 
        print(f"Image load error: {e}")

    # Search Bar for Website
    Label(window, text="Website:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0)
    website_entry = Entry(window, width=60, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    website_entry.grid(row=2, column=1, columnspan=2, pady=config.ENTRY_PAD, sticky=W)
    website_entry.focus()

    # --- Core Processing Logic ---
    # This handles checking the DB and routing to the right function based on how many accounts exist
    def process_action(action_type):
        website = website_entry.get().upper()
        if len(website) == 0:
            messagebox.showinfo(title="Error", message=f"Please enter a website name to {action_type}.")
            return

        results = database.get_passwords(website)
        
        if not results:
            messagebox.showinfo(title="Error", message=f"No password found for {website}.")
            return
            
        if len(results) == 1:
            # Only one account found, proceed normally
            if action_type == "update":
                open_update_form(website, results[0])
            else:
                confirm_and_delete(website, results[0])
        else:
            # MULTIPLE ACCOUNTS FOUND: Open a selector popup
            select_win = Toplevel(window)
            select_win.title("Multiple Accounts Found")
            select_win.config(padx=20, pady=20, bg=config.BLACK)
            
            Label(select_win, text=f"Select account to {action_type}:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).pack()
            
            # Format the options for the dropdown
            account_var = StringVar()
            options = [f"Email: {r[0]} | User: {r[1]}" for r in results]
            
            # Use ttk Combobox for selection
            style = ttk.Style()
            style.theme_use("clam")
            dropdown = ttk.Combobox(select_win, textvariable=account_var, values=options, state="readonly", width=40)
            dropdown.pack(pady=10)
            dropdown.current(0) # Select first item by default
            
            def proceed():
                # Get the index of the selected item to map it back to our results list
                idx = dropdown.current()
                selected_account = results[idx]
                select_win.destroy()
                
                # Route to the correct action
                if action_type == "update":
                    open_update_form(website, selected_account)
                else:
                    confirm_and_delete(website, selected_account)
                    
            Button(select_win, text="Proceed", command=proceed, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).pack()

    # ---------------------------- Update Form Logic ------------------------------- #
    def open_update_form(website, account_data):
        old_email, old_username, old_password = account_data
        
        update_window = Toplevel(window)
        update_window.title("Update Password")
        update_window.config(padx=20, pady=20, bg=config.BLACK)

        Label(update_window, text="Email:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=0, column=0)
        Label(update_window, text="Username:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=1, column=0)
        Label(update_window, text="Password:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0)

        email_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
        email_entry.grid(row=0, column=1, pady=config.ENTRY_PAD)
        email_entry.insert(0, old_email if old_email else "") 

        username_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
        username_entry.grid(row=1, column=1, pady=config.ENTRY_PAD)
        username_entry.insert(0, old_username if old_username else "") 

        password_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
        password_entry.grid(row=2, column=1, pady=config.ENTRY_PAD)
        password_entry.insert(0, old_password) 

        def update_in_db():
            new_email = email_entry.get()
            new_username = username_entry.get()
            new_password = password_entry.get()

            if len(new_password) == 0:
                messagebox.showinfo(title="Error", message="Password cannot be empty.")
            else:
                # Passes old_email and old_username to precisely target the correct database row
                database.update_password(website, old_email, old_username, new_email, new_username, new_password)
                messagebox.showinfo(title="Success", message="Password updated successfully!")
                update_window.destroy()

        Button(update_window, text="Update", command=update_in_db, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=0, columnspan=2, pady=config.ENTRY_PAD)

    # ---------------------------- Delete Action Logic ------------------------------- #
    def confirm_and_delete(website, account_data):
        old_email, old_username, _ = account_data
        
        display_id = old_email if old_email else old_username
        if messagebox.askokcancel(title="Delete Confirmation", message=f"Are you sure you want to delete the record for {website} ({display_id})?"):
            database.delete_password(website, old_email, old_username)
            messagebox.showinfo(title="Success", message="Record deleted successfully!")

    # ---------------------------- UI Buttons ------------------------------- #
    # Lambda functions are used here to pass the "action_type" to our central processor
    Button(window, text="Update", width=20, command=lambda: process_action("update"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=1, pady=config.ENTRY_PAD, sticky=W)
    Button(window, text="Delete", width=20, command=lambda: process_action("delete"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=2, pady=config.ENTRY_PAD, sticky=E)
    
    Label(window, text="    ", bg=config.BLACK).grid(row=4, column=1)
    Button(window, text="<-Back", width=22, command=lambda: navigate("dashboard"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=5, column=1, columnspan=2, pady=config.ENTRY_PAD)