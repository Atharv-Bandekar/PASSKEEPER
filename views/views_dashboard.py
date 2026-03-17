from tkinter import *
from tkinter import messagebox, ttk
import pyperclip
import config
import utils
import database

# ------------------- Main Dashboard Page -------------------
def add_password_page(window, navigate):
    window.title("PASSKEEPER")

    # Canvas and Logo Image
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH)
        canvas = Canvas(window, width=270, height=200, highlightthickness=0, bg=config.BLACK)
        canvas.create_image(68, 100, image=window.image_refs['lock_img'])
        canvas.grid(row=0, column=1, columnspan=3)
    except Exception as e:
        print(f"Image load error: {e}")

    # --- ROW 2: Website Input ---
    Label(window, text="Website:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=0)
    website_entry = Entry(window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    website_entry.grid(row=2, column=1, columnspan=2, pady=config.ENTRY_PAD, sticky=EW)
    website_entry.focus() # Auto-focus the cursor here when the page loads

    # --- ROW 3: Dynamic Field Checkboxes ---
    Label(window, text="Include:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=0)
    
    # BooleanVars track the state of the checkboxes (True/False)
    show_email_var = BooleanVar(value=True)  # Default to showing email
    show_username_var = BooleanVar(value=False)

    # Checkbuttons trigger the toggle_fields() function whenever clicked
    Checkbutton(window, text="Email", variable=show_email_var, command=lambda: toggle_fields(), bg=config.BLACK, fg=config.TURQUOISE, selectcolor=config.DARK_CHARCOAL, font=config.FONT).grid(row=3, column=1, sticky=W)
    Checkbutton(window, text="Username", variable=show_username_var, command=lambda: toggle_fields(), bg=config.BLACK, fg=config.TURQUOISE, selectcolor=config.DARK_CHARCOAL, font=config.FONT).grid(row=3, column=2, sticky=W)

    # --- ROW 4 & 5: Dynamic Email & Username Inputs ---
    # We define the widgets here, but we don't 'grid' them yet. 
    # toggle_fields() will handle placing or hiding them based on the checkboxes.
    
    email_label = Label(window, text="Email:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    email_var = StringVar()
    
    # Styling for the ttk Combobox (Dropdown)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TCombobox", fieldbackground=config.DARK_CHARCOAL, background=config.DARK_CHARCOAL, foreground=config.TURQUOISE, selectbackground=config.DARK_CHARCOAL, selectforeground=config.TURQUOISE)
    
    dropdown = ttk.Combobox(window, width=59, height=15, textvariable=email_var)
    dropdown['values'] = database.get_default_emails()

    username_label = Label(window, text="Username:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    username_entry = Entry(window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)

    # Function to dynamically show/hide input fields
    def toggle_fields():
        if show_email_var.get():
            email_label.grid(row=4, column=0)
            dropdown.grid(row=4, column=1, columnspan=3, pady=config.ENTRY_PAD, sticky=EW)
        else:
            # grid_remove temporarily hides the widget without destroying it
            email_label.grid_remove()
            dropdown.grid_remove()
            dropdown.set('') # Clear the data if hidden

        if show_username_var.get():
            username_label.grid(row=5, column=0)
            username_entry.grid(row=5, column=1, columnspan=3, pady=config.ENTRY_PAD, sticky=EW)
        else:
            username_label.grid_remove()
            username_entry.grid_remove()
            username_entry.delete(0, END) # Clear the data if hidden

    # Call it once on startup to set the initial UI state
    toggle_fields() 

    # --- ROW 7: Password Input ---
    Label(window, text="Password:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=7, column=0)
    password_entry = Entry(window, width=40, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    password_entry.grid(row=7, column=1, columnspan=2, pady=config.ENTRY_PAD, sticky=EW)

    # ------------------- Action Functions -------------------
    
    # Inserts a generated password into the UI and copies it
    def generate_password_ui(nr_letters=10, nr_symbols=4, nr_numbers=4):
        password_entry.delete(first=0, last=END)
        password = utils.generate_random_password(nr_letters, nr_symbols, nr_numbers)
        pyperclip.copy(password) 
        password_entry.insert(index=0, string=password)

    # Decides whether to generate default length or ask for manual length
    def generate_password_handler():
        if password_length_choice.get() == "manual":
            manual_length_popup()
        else:
            generate_password_ui()

    # Popup window for custom password parameters
    def manual_length_popup():
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
                popup.destroy() 
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers.")

        Button(popup, text="Generate", command=get_manual_values, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=3, column=1)

    # Save logic with validation for dynamic fields
    def save():
        website = website_entry.get().upper()
        email = dropdown.get()
        username = username_entry.get()
        password = password_entry.get()

        # 1. Base validation
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops!", message="Please make sure Website and Password are not empty.")
            return
            
        # 2. Checkbox state validation
        if not show_email_var.get() and not show_username_var.get():
            messagebox.showinfo(title="Oops!", message="Please select at least Email or Username to save.")
            return

        # 3. Content validation for active fields
        if show_email_var.get() and len(email) == 0:
            messagebox.showinfo(title="Oops!", message="Email field is checked but empty.")
            return

        if show_username_var.get() and len(username) == 0:
            messagebox.showinfo(title="Oops!", message="Username field is checked but empty.")
            return

        if show_email_var.get() and not utils.is_valid_email(email):
            messagebox.showinfo(title="Invalid Email", message="Please enter a valid email address.")
            return

        # 4. Build confirmation message dynamically
        msg = f"Details entered:\n"
        if show_email_var.get(): msg += f"Email: {email}\n"
        if show_username_var.get(): msg += f"Username: {username}\n"
        msg += f"Password: {password}\nIs it ok to save?"

        # 5. Save to database
        if messagebox.askokcancel(title=website, message=msg):
            database.add_password(website, email, username, password)
            # Clear fields after saving
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            dropdown.set('')
            username_entry.delete(0, END)

    # Search for an existing password
    def search_password():
        website = website_entry.get().upper()
        
        # Returns a list of all accounts for this website
        results = database.get_passwords(website)
        
        if results:
            msg = f"Accounts found for {website}:\n\n"
            
            # Loop through the list and format each account
            for index, (email, username, password) in enumerate(results, start=1):
                msg += f"--- Account {index} ---\n"
                if email: msg += f"Email: {email}\n"
                if username: msg += f"Username: {username}\n"
                msg += f"Password: {password}\n\n"
                
            # .strip() removes any trailing blank lines
            messagebox.showinfo(title=website, message=msg.strip())
        else:
            messagebox.showinfo(title="Error", message=f"No password found for {website}.")


    # Wipe database function
    def delete_account():
        if messagebox.askyesno(title="Delete Account", message="Are you sure you want to delete your account? All data will be lost."):
            database.delete_all_user_data()
            messagebox.showinfo(title="Account Deleted", message="Your account has been deleted.")
            navigate("sign_up")

    # ---------------------------- UI Layout Continued ------------------------------- #
    
    # Radio Buttons for password length
    password_length_choice = StringVar(value="default")
    Radiobutton(window, text="Default Length", variable=password_length_choice, value="default", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=6, column=1, sticky="w", padx=10, pady=config.ENTRY_PAD)
    Radiobutton(window, text="Manual Length", variable=password_length_choice, value="manual", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT).grid(row=6, column=2, sticky="w", padx=10, pady=config.ENTRY_PAD)

    # Main Action Buttons
    Button(window, text="Search", width=17, command=search_password, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=2, column=3, sticky=EW)
    Button(window, text="Generate Password", command=generate_password_handler, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=7, column=3, sticky=EW)
    Button(window, text="Add", width=59, command=save, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=8, column=1, columnspan=3, pady=config.ENTRY_PAD, sticky=EW)
    
    # Navigation Buttons (using lambda to pass the page name to the router)
    Button(window, text="View saved websites", command=lambda: navigate("view_all"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=10, column=0, pady=20)
    Button(window, text="Save default emails", command=lambda: navigate("save_emails"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=10, column=1, columnspan=2, pady=20)
    Button(window, text="Update/Delete passwords", command=lambda: navigate("update_delete"), bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=10, column=3, pady=20, columnspan=4, sticky=E)
    Button(window, text="Delete account", command=delete_account, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT).grid(row=11, column=1, columnspan=2, pady=20, sticky=EW)