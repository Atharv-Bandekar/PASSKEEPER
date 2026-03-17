from tkinter import *
from tkinter import messagebox
import config
import database

# ---------------------------- update_delete_password ------------------------------- #
def update_delete_password_page(window, navigate):
    # ---------------------------- UI SETUP ------------------------------- #
    window.title("update/delete passwords")

    # Canvas and Image
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH) 
        canvas = Canvas(window, width=250, height=200, highlightthickness=0, bg=config.BLACK)
        canvas.create_image(175, 100, image=window.image_refs['lock_img'])
        canvas.grid(row=0, column=1)
    except Exception as e: 
        print(f"Image load error: {e}")

    # Labels
    Label(window, text="Website:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0)
    
    # Entries
    website_entry = Entry(window, width=60, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    website_entry.grid(row=2, column=1, columnspan=2, pady=config.ENTRY_PAD, sticky=W)
    website_entry.focus()

    # ---------------------------- UPDATE PASSWORD ------------------------------- #
    def update_password():
        website = website_entry.get().upper()

        # Check if the website field is not empty
        if len(website) == 0:
            messagebox.showinfo(title="Error", message="Please enter a website name to update.")
            return

        # Fetch the existing data for the website
        result = database.get_password(website)
        if result:
            # Display the current email and password in a popup for updating
            update_window = Toplevel(window)
            update_window.title("Update Password")
            update_window.config(padx=20, pady=20, bg=config.BLACK)

            # Labels and entries for email and password
            Label(update_window, text="Email/Username:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=0, column=0)
            Label(update_window, text="Password:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=1, column=0)

            email_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
            email_entry.grid(row=0, column=1, pady=config.ENTRY_PAD)
            email_entry.insert(0, result[0]) # Populate the existing email

            password_entry = Entry(update_window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
            password_entry.grid(row=1, column=1, pady=config.ENTRY_PAD)
            password_entry.insert(0, result[1]) # Populate the existing password

            # Function to update the database
            def update_in_db():
                new_email = email_entry.get()
                new_password = password_entry.get()

                if len(new_email) == 0 or len(new_password) == 0:
                    messagebox.showinfo(title="Error", message="Please fill in all fields.")
                else:
                    database.update_password(website, new_email, new_password)
                    messagebox.showinfo(title="Success", message="Password updated successfully!")
                    update_window.destroy()

            # Update button
            Button(update_window, text="Update", command=update_in_db, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0, columnspan=2, pady=config.ENTRY_PAD)
        else:
            messagebox.showinfo(title="Error", message="No password found for the given website.")

    # ---------------------------- DELETE PASSWORD ------------------------------- #
    def delete_password():
        website = website_entry.get().upper()

        if len(website) == 0:
            messagebox.showinfo(title="Error", message="Please enter a website name to delete.")
            return

        # Confirmation popup
        is_ok = messagebox.askokcancel(title="Delete Confirmation", message=f"Are you sure you want to delete the record for {website}?")
        if is_ok:
            database.delete_password(website)
            messagebox.showinfo(title="Success", message="Record deleted successfully!")

    # Buttons
    Button(window, text="Update", width=20, command=update_password, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=1, pady=config.ENTRY_PAD, sticky=W)
    Button(window, text="Delete", width=20, command=delete_password, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=2, pady=config.ENTRY_PAD, sticky=E)
    Label(window, text="    ", bg=config.BLACK).grid(row=4, column=1)
    
    # back Button
    Button(window, text="<-Back", width=22, command=lambda: navigate("dashboard"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=5, column=1, columnspan=2, pady=config.ENTRY_PAD)