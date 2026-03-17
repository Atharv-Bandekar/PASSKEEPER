from tkinter import *
from tkinter import messagebox
import config
import database

# ------------------- Sign-Up Page -------------------
def sign_up_page(window, navigate):
    window.title("Sign Up")

    # Canvas and Image
    canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=config.BLACK)
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH) 
        canvas.create_image(130, 100, image=window.image_refs['lock_img'])
    except Exception as e:
        print(f"Image load error: {e}")
    canvas.grid(row=0, column=1)

    # Label and Entry
    pin_label = Label(window, text="Set the pin:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    pin_label.grid(row=4, column=0)

    pin_valid_label = Label(window, text="*Enter 4 or 6-digits pin", bg=config.BLACK, fg=config.TURQUOISE,
                            font=("consolas", 9, "normal"), pady=config.ENTRY_PAD)
    pin_valid_label.grid(row=5, column=1, sticky=W)

    pin_entry = Entry(window, width=60, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT)
    pin_entry.grid(row=4, column=1, columnspan=3, sticky=EW)

    # Function for sign-up button
    def sign_up():
        pin = pin_entry.get()

        # Field validations
        if len(pin) == 0:
            messagebox.showinfo(title="Error", message="Make sure you have not left any empty fields")
            return

        if not pin.isdigit():
            messagebox.showinfo(title="Error", message="Please enter a valid pin without characters")
            return

        if len(pin) not in (4, 6):
            messagebox.showinfo(title="Error", message="Please enter a valid 4 or 6-digit pin")
            return

        database.save_user_pin(pin)

        messagebox.showinfo(title="Success", message="Sign-up successful!")
        # Go to log-in page
        navigate("log_in")

    # Sign-up Button
    sign_up_button = Button(window, text="Sign up", width=59, command=sign_up, bg=config.DARK_CHARCOAL, 
                            fg=config.TURQUOISE, font=config.FONT)
    sign_up_button.grid(row=7, column=1, columnspan=3, pady=config.ENTRY_PAD)


# ------------------- Log-In Page -------------------
def log_in_page(window, navigate):
    window.title("Log In")

    # Canvas and Image
    canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=config.BLACK)
    try:
        window.image_refs['lock_img'] = PhotoImage(file=config.LOCK_IMG_PATH) 
        canvas.create_image(130, 100, image=window.image_refs['lock_img'])
    except Exception as e:
        print(f"Image load error: {e}")
    canvas.grid(row=0, column=1)

    # Label and Entry
    pin_label = Label(window, text="Enter the pin:", bg=config.BLACK, fg=config.TURQUOISE, font=config.FONT)
    pin_label.grid(row=2, column=0)

    pin_entry = Entry(window, width=60, bg=config.DARK_CHARCOAL, fg=config.TURQUOISE, font=config.FONT, show='*')
    pin_entry.grid(row=2, column=1, columnspan=3, pady=config.ENTRY_PAD, sticky=EW)
    pin_entry.focus()

    # Function for log-in button
    def log_in():
        pin = pin_entry.get()

        if len(pin) == 0:
            messagebox.showerror(title="Error!", message="Fill the pin field; it can't be empty!")
            return

        if database.verify_pin(pin):
            messagebox.showinfo(title="Success", message="Login successful!")
            # Proceed to add password page
            navigate("dashboard")
        else:
            messagebox.showerror(title="Error", message="Entered pin is wrong!")
            return

    # Log-in Button
    sign_in_button = Button(window, text="Log in", width=59, command=log_in, bg=config.DARK_CHARCOAL, 
                            fg=config.TURQUOISE, font=config.FONT)
    sign_in_button.grid(row=3, column=1, columnspan=3, pady=config.ENTRY_PAD)