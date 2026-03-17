from tkinter import *
from tkinter import messagebox
import config
import utils
import database

# ---------------------------- save_default_emails ------------------------------- #
def save_default_emails_page(window, navigate):
    # ----------------------------- UI SETUP ----------------------------- #
    window.title("Save default emails")
    
    # Canvas and Image
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH) 
        canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=config.BLACK)
        canvas.create_image(120, 100, image=window.image_refs['lock_img'])
        canvas.grid(row=0, column=1)
    except Exception as e: 
        print(f"Image load error: {e}")

    # Labels
    Label(window, text="Enter Email:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=1, column=0)
    
    # Entry
    email_entry = Entry(window, width=59, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    email_entry.grid(row=1, column=1, pady=config.ENTRY_PAD, columnspan=2)

    def save_default_email():
        email = email_entry.get()

        # Email validation
        if len(email) == 0:
            messagebox.showinfo(title="Oops!", message="Please make sure you haven't left the email field empty.")
        elif not utils.is_valid_email(email):
            messagebox.showinfo(title="Invalid Email", message="Please enter a valid email address.")
        else:
            # Displaying a pop-up box to confirm saving
            is_ok = messagebox.askokcancel(title="Confirm Email", message=f"Is it okay to save this email?\n\nEmail: {email}")

            if is_ok:
                # Insert the email into the default_emails table
                database.add_default_email(email)
                
                # Clear the email field
                email_entry.delete(first=0, last=END)
                messagebox.showinfo(title="Success", message="Email has been saved successfully!")

    # Add Button
    Button(window, text="Add", width=59, command=save_default_email, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=1, columnspan=2, pady=config.ENTRY_PAD)
    
    blank_label = Label(window, text="    ", bg=config.BLACK)
    blank_label.grid(row=3, column=1)
    
    # back Button
    Button(window, text="<-Back", width=22, command=lambda: navigate("dashboard"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=4, column=1, columnspan=2, pady=config.ENTRY_PAD)