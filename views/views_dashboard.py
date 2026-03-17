from tkinter import *
from tkinter import messagebox, ttk
import pyperclip
import config
import utils
import database

# ------------------- Add Password Page -------------------
def add_password_page(window, navigate):
    window.title("PASSKEEPER")

    # Canvas and Image
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH)
        canvas = Canvas(window, width=240, height=200, highlightthickness=0, bg=config.BLACK)
        canvas.create_image(170, 100, image=window.image_refs['lock_img'])
        canvas.grid(row=0, column=1)
    except Exception as e:
        print(f"Image load error: {e}")

    # Labels
    website_label = Label(window, text="Website:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    website_label.grid(row=2, column=0)

    email_username_label = Label(window, text="Email/Username:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    email_username_label.grid(row=3, column=0)

    blank_label = Label(window, text="    ", bg=config.BLACK)
    blank_label.grid(row=4, column=1)

    password_label = Label(window, text="Password:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    password_label.grid(row=6, column=0)

    # Entries
    website_entry = Entry(window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    website_entry.grid(row=2, column=1, columnspan=2, pady=config.ENTRY_PAD, sticky=EW)
    website_entry.focus()

    email_var = StringVar()
    # Create a style object for the Combobox
    style = ttk.Style()
    # Set the theme to 'clam' or another that supports styling changes
    style.theme_use("clam")
    # Configure the style for the Combobox
    style.configure("TCombobox", fieldbackground=config.DARK_CHARCOAL, background=config.DARK_CHARCOAL, 
                    foreground=config.TURQUOISE, selectbackground=config.DARK_CHARCOAL, selectforeground=config.TURQUOISE)

    dropdown = ttk.Combobox(window, width=59, height=15, textvariable=email_var)
    dropdown.grid(row=3, column=1, columnspan=3, pady=config.ENTRY_PAD, sticky=EW)
    dropdown['values'] = database.get_default_emails()

    password_entry = Entry(window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    password_entry.grid(row=6, column=1, columnspan=2, pady=config.ENTRY_PAD, sticky=EW)

    # Functions for buttons
    def generate_password_ui(nr_letters=10, nr_symbols=4, nr_numbers=4):
        password_entry.delete(first=0, last=END) # Clear previous password
        password = utils.generate_random_password(nr_letters, nr_symbols, nr_numbers)
        pyperclip.copy(password) # Copy to clipboard
        password_entry.insert(index=0, string=password)

    def generate_password_handler():
        # If "manual" is selected, open a popup to get custom lengths
        if password_length_choice.get() == "manual":
            manual_length_popup() # Open popup window to get manual lengths
        else:
            # Default length generation
            generate_password_ui()

    def manual_length_popup():
        # Popup window to get manual lengths
        popup = Toplevel(window)
        popup.title("Enter Manual Lengths")
        popup.config(padx=50, pady=50, bg=config.BLACK)

        Label(popup, text="Number of Letters:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=0, column=0, padx=10, pady=10)
        Label(popup, text="Number of Symbols:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=1, column=0, padx=10, pady=10)
        Label(popup, text="Number of Numbers:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0, padx=10, pady=10)

        letters_entry = Entry(popup, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
        symbols_entry = Entry(popup, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
        numbers_entry = Entry(popup, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)

        letters_entry.grid(row=0, column=1, padx=10, pady=10)
        symbols_entry.grid(row=1, column=1, padx=10, pady=10)
        numbers_entry.grid(row=2, column=1, padx=10, pady=10)

        def get_manual_values():
            try:
                generate_password_ui(int(letters_entry.get()), int(symbols_entry.get()), int(numbers_entry.get()))
                popup.destroy() # Close popup after collecting data
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers.")

        Button(popup, text="Generate", command=get_manual_values, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=1)

    def save():
        website = website_entry.get().upper()
        email = dropdown.get()
        password = password_entry.get()

        if len(website) == 0 or len(email) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty.")
        elif not utils.is_valid_email(email):
            messagebox.showinfo(title="Invalid Email", message="Please enter a valid email address.")
        else:
            is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\n Email: {email}\nPassword: {password}\nIs it ok to save?")
            if is_ok:
                database.add_password(website, email, password)
                website_entry.delete(first=0, last=END)
                password_entry.delete(first=0, last=END)
                dropdown.set('')

    def search_password():
        website = website_entry.get().upper()
        result = database.get_password(website)
        if result:
            messagebox.showinfo(title=website, message=f"Email: {result[0]}\nPassword: {result[1]}")
        else:
            messagebox.showinfo(title="Error", message=f"No password found for {website}.")

    def delete_account():
        confirm = messagebox.askyesno(title="Delete Account",
                                      message="Are you sure you want to delete your account? All data will be lost.")
        if confirm:
            database.delete_all_user_data()
            messagebox.showinfo(title="Account Deleted", message="Your account has been deleted.")
            # Return to sign-up page
            navigate("sign_up")

    # ---------------------------- Radio Buttons ------------------------------- #
    password_length_choice = StringVar(value="default") # Default option

    # Create radio buttons for password length options
    Radiobutton(window, text="Default Length", variable=password_length_choice, value="default", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=5, column=1, sticky="w", padx=10, pady=config.ENTRY_PAD)
    Radiobutton(window, text="Manual Length", variable=password_length_choice, value="manual", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=5, column=2, sticky="w", padx=10, pady=config.ENTRY_PAD)

    # Buttons
    Button(window, text="Generate Password", command=generate_password_handler, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=6, column=3, sticky=EW)
    Button(window, text="Add", width=59, command=save, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=7, column=1, columnspan=3, pady=config.ENTRY_PAD, sticky=EW)
    Button(window, text="Search", width=17, command=search_password, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=3, sticky=EW)
    
    # Navigation Buttons
    Button(window, text="view saved websites", command=lambda: navigate("view_all"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=9, column=0, pady=20)
    Button(window, text="save_default_emails", command=lambda: navigate("save_emails"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=9, column=1, columnspan=2, pady=20)
    Button(window, text="update_passwords", command=lambda: navigate("update_delete"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=9, column=3, pady=20, columnspan=4, sticky=E)
    Button(window, text="delete_account", command=delete_account, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=10, column=1, columnspan=2, pady=20, sticky=EW)