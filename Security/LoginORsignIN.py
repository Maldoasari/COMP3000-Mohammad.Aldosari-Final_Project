import hashlib
import os
import subprocess
import time
import tkinter as tk
from tkinter import messagebox, font
import json
from Resttful_API import Post_record, Get_record_by_email
def LoginOrSign():
# Fade effect
 def fade_in(widget, step=0.05):
    alpha = widget.attributes("-alpha")
    if alpha < 1:
        alpha += step
        widget.attributes("-alpha", alpha)
        widget.after(50, lambda: fade_in(widget, step))

# Functions for placeholder text handling
 def on_entry_click(event, default_text):
    if event.widget.get() == default_text:
        event.widget.delete(0, "end")
        event.widget.config(fg='black')

 def on_focusout(event, default_text):
    if not event.widget.get():
        event.widget.insert(0, default_text)
        event.widget.config(fg='grey')

# Hashing functions
 def hash_password(password):
    salt = os.urandom(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwdhash.hex()

 def verify_password(stored_password, provided_password):
    salt = bytes.fromhex(stored_password[:64])
    stored_password = bytes.fromhex(stored_password[64:])
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_password

# Function to save user data
 def save_user_data(user_data):
    filename = './Database/User.json'
    try:
        with open(filename, 'r') as file:
            data_to_save = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data_to_save = {}

    email = user_data["Email address"]
    data_to_save[email] = user_data

    with open(filename, 'w') as file:
        json.dump(data_to_save, file, indent=4)

# Function to attempt login
 def attempt_login(email, password, pin):
    filename = './Database/User.json'
    try:
        with open(filename, 'r') as file:
            users = json.load(file)
            if email in users:
                stored_data = users[email]
                password_verified = verify_password(stored_data["password"], password)
                pin_verified = verify_password(stored_data["pincode"], pin)
                return password_verified and pin_verified
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return False

# Sign In Action
 def sign_in_action():
    email = email_entry.get() if email_entry.get() != "Enter Email" else ""
    password = password_entry.get() if password_entry.get() != "Enter Password" else ""

    if len(email) == 0 or len(password) == 0:
        messagebox.showerror("Invalid", "Email and password must not be empty")
        return

    hashed_password = hash_password(password)
    user_data = {
        "email_login": email,
        "pincode_login": "string",
        "password_login": hashed_password,
        "email_service_login_email": "string",
        "email_service_login_pass": "string",
        "netflix_username": "string",
        "netflix_pass": "string",
        "primeVideo_username": "string",
        "primeVideo_pass": "string",
        "spotify_Client_ID": "string",
        "spotify_Client_Secret": "string"
    }

    # Open the pincode window
    open_pin_window(user_data)

# Login Action
 def login_action():
    email = email_entry.get() if email_entry.get() != "Enter Email" else ""
    password = password_entry.get() if password_entry.get() != "Enter Password" else ""

    if len(email) == 0 or len(password) == 0:
        messagebox.showerror("Invalid", "Email and password must not be empty")
        return

    # Open the pincode window for login
    open_login_pin_window(email, password)

# Open Pin Window for sign in
 def open_pin_window(user_data):
    root.withdraw()
    pin_window = tk.Toplevel(root)
    pin_window.title("Enter Pincode")
    pin_window.configure(bg='#333333')
    pin_window.geometry("300x200")

    tk.Label(pin_window, text="Enter Pincode:", font=custom_font, bg='#333333', fg='white').pack(pady=10)
    pin_entry = tk.Entry(pin_window, show="*", font=custom_font)
    pin_entry.pack(pady=10)
    def on_pin_window_close():
        root.deiconify()  
        pin_window.destroy()

    pin_window.protocol("WM_DELETE_WINDOW", on_pin_window_close)

    def on_pin_submit():
        command = ["python", "./Security/Loader.py"]
        pin = pin_entry.get()
        if len(pin) == 0 or not pin.isdigit() or len(pin) != 6:
            messagebox.showerror("Invalid", "Pincode must be 6 digits and not empty")
            return
        pin_window.destroy()
        root.destroy()
        process = subprocess.Popen(command)
        hashed_pin = hash_password(pin)
        user_data["pincode_login"] = hashed_pin
        Post_record(user_data)
        process.wait()
        messagebox.showinfo("Sign In Successful", "You are now signed in.")

    tk.Button(pin_window, text="Submit Pin", command=on_pin_submit, font=custom_font).pack(pady=10)

# Open Pin Window for login
 def open_login_pin_window(email, password):
    root.withdraw()
    login_pin_window = tk.Toplevel(root)
    login_pin_window.title("Enter Pincode")
    login_pin_window.configure(bg='#333333')
    login_pin_window.geometry("300x200")

    tk.Label(login_pin_window, text="Enter Pincode:", font=custom_font, bg='#333333', fg='white').pack(pady=10)
    pin_entry = tk.Entry(login_pin_window, show="*", font=custom_font)
    pin_entry.pack(pady=10)
    def on_login_pin_window_close():
        root.deiconify()  
        login_pin_window.destroy()

    login_pin_window.protocol("WM_DELETE_WINDOW", on_login_pin_window_close)
    def on_pin_submit():
        pin = pin_entry.get()
        if attempt_login(email, password, pin):
            messagebox.showinfo("Login Successful", "You are now logged in.")
            login_pin_window.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid email, password, or pincode.")
            login_pin_window.destroy()
        root.destroy()

    tk.Button(login_pin_window, text="Submit Pin", command=on_pin_submit, font=custom_font).pack(pady=10)

# Main window setup
 root = tk.Tk()
 root.title("Sign In / Login")
 root.geometry("300x200")
 root.configure(bg='#333333')
 root.attributes("-alpha", 0)
 root.attributes('-topmost', True)

# Custom font
 custom_font = font.Font(family="Helvetica", size=12)

# Email Entry
 email_entry = tk.Entry(root, font=custom_font, fg='grey')
 email_entry.insert(0, "Enter Email")
 email_entry.bind('<FocusIn>', lambda event: on_entry_click(event, "Enter Email"))
 email_entry.bind('<FocusOut>', lambda event: on_focusout(event, "Enter Email"))
 email_entry.pack(pady=10)

# Password Entry
 password_entry = tk.Entry(root, show="*", font=custom_font, fg='grey')
 password_entry.insert(0, "Enter Password")
 password_entry.bind('<FocusIn>', lambda event: on_entry_click(event, "Enter Password"))
 password_entry.bind('<FocusOut>', lambda event: on_focusout(event, "Enter Password"))
 password_entry.pack(pady=10)

# Sign In and Login Buttons
 sign_in_button = tk.Button(root, text="Sign In", command=sign_in_action, font=custom_font, width=13, height=1, bg='grey', borderwidth=5)
 login_button = tk.Button(root, text="Login", command=login_action, font=custom_font, width=13, height=1, bg='grey', borderwidth=5)
 sign_in_button.pack(pady=1)
 login_button.pack(pady=2)

# Fade in the main window
 fade_in(root)

 root.mainloop()

LoginOrSign()