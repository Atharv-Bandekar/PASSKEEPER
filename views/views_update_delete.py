from tkinter import *
from tkinter import messagebox
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

    # ---------------------------- Update Logic ------------------------------- #
    def update_password():
        website = website_entry.get().upper()
        if len(website) == 0:
            messagebox.showinfo(title="Error", message="Please enter a website name to update.")
            return

        # Fetch the existing data to pre-fill the update form
        result = database.get_password(website)
        
        if result:
            # Create a popup window (Toplevel) over the main window
            update_window = Toplevel(window)
            update_window.title("Update Password")
            update_window.config(padx=20, pady=20, bg=config.BLACK)

            # Labels for the 3 data fields
            Label(update_window, text="Email:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=0, column=0)
            Label(update_window, text="Username:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=1, column=0)
            Label(update_window, text="Password:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0)

            # Pre-populate Email field (Check if it exists first to avoid NoneType errors)
            email_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
            email_entry.grid(row=0, column=1, pady=config.ENTRY_PAD)
            email_entry.insert(0, result[0] if result[0] else "") 

            # Pre-populate Username field
            username_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
            username_entry.grid(row=1, column=1, pady=config.ENTRY_PAD)
            username_entry.insert(0, result[1] if result[1] else "") 

            # Pre-populate Password field
            password_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
            password_entry.grid(row=2, column=1, pady=config.ENTRY_PAD)
            password_entry.insert(0, result[2]) 

            # Nested function to handle the actual database update when clicked
            def update_in_db():
                new_email = email_entry.get()
                new_username = username_entry.get()
                new_password = password_entry.get()

                if len(new_password) == 0:
                    messagebox.showinfo(title="Error", message="Password cannot be empty.")
                else:
                    database.update_password(website, new_email, new_username, new_password)
                    messagebox.showinfo(title="Success", message="Password updated successfully!")
                    update_window.destroy()

            # Execute Update Button
            Button(update_window, text="Update", command=update_in_db, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=0, columnspan=2, pady=config.ENTRY_PAD)
        else:
            messagebox.showinfo(title="Error", message="No password found for the given website.")

    # ---------------------------- Delete Logic ------------------------------- #
    def delete_password():
        website = website_entry.get().upper()
        if len(website) == 0:
            messagebox.showinfo(title="Error", message="Please enter a website name to delete.")
            return

        # Always ask for confirmation before executing a DELETE query
        if messagebox.askokcancel(title="Delete Confirmation", message=f"Are you sure you want to delete the record for {website}?"):
            database.delete_password(website)
            messagebox.showinfo(title="Success", message="Record deleted successfully!")

    # UI Buttons for Update and Delete
    Button(window, text="Update", width=20, command=update_password, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=1, pady=config.ENTRY_PAD, sticky=W)
    Button(window, text="Delete", width=20, command=delete_password, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=2, pady=config.ENTRY_PAD, sticky=E)
    
    # Spacer
    Label(window, text="    ", bg=config.BLACK).grid(row=4, column=1)
    
    # Navigation Back Button
    Button(window, text="<-Back", width=22, command=lambda: navigate("dashboard"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=5, column=1, columnspan=2, pady=config.ENTRY_PAD)