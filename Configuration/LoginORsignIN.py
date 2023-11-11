import hashlib
import os
import tkinter as tk
from tkinter import messagebox, font
import json

##Creating a login and or sign in window for new and current users:

# Fade affect 
def fade_in(widget, step=0.05):
    
    alpha = widget.attributes("-alpha")
    if alpha < 1:
        alpha += step
        widget.attributes("-alpha", alpha)
        widget.after(50, lambda: fade_in(widget, step))

# Function to clear the placeholder text when the user clicks
def on_entry_click(event, default_text):
    if event.widget.get() == default_text:
        event.widget.delete(0, "end")
        event.widget.config(fg='black')

# Function to add placeholder text if the field is empty
def on_focusout(event, default_text):
    if not event.widget.get():
        event.widget.insert(0, default_text)
        event.widget.config(fg='grey')
def forget_action():
     pass

def hash_password(password):
    """ Hash a password for storing. """
    salt = os.urandom(32)  # A new salt for this user
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    # Return a hex string
    return salt.hex() + pwdhash.hex()

def verify_password(stored_password, provided_password):
    """ Verify a stored password against one provided by user """
    salt = bytes.fromhex(stored_password[:64])  # 32 bytes salt in hex is 64 characters
    stored_password = bytes.fromhex(stored_password[64:])
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_password


# Function to handle submit action
def submit_action():
    email = email_entry.get() if email_entry.get() != "Enter Email" else ""
    password = password_entry.get() if password_entry.get() != "Enter Password" else ""
    
    if len(email) == 0 or len(password) == 0:
         messagebox.showerror("Invalid", "the givin password or email must not be empty")
         return
    hashed_password = hash_password(password)
    user_data = {
        "Email address": email,
        "password": hashed_password,
        "pincode": ""
    }
    # Hide the main window
    root.withdraw()
    # Open the pincode window
    pin_window = tk.Toplevel(root)
    pin_window.title("Pin Code")
    pin_window.configure(bg='#333333')
    pin_window.geometry("300x200")

    tk.Label(pin_window, text="Enter Pincode:", font=custom_font, bg='#333333', fg='white').pack(pady=10)
    pin_entry = tk.Entry(pin_window, show="*", font=custom_font)
    pin_entry.pack(pady=10)
    def submit_pin():
        x = pin_entry.get()
        if (len(x) == 0) or (len(x) <= 5) or (len(x) >= 7):
         messagebox.showerror("Invalid", "the givin pincode must be 6 digits and not empty")
         return
        elif not x.isdigit():
         messagebox.showerror("Invalid", "the givin pincode must contain only digits (numbers)")
         return  
        hashed_pin = hash_password(x)
        user_data["pincode"] = hashed_pin
        # Show the data in JSON format as an example (not secure)
        messagebox.showinfo("User Data", json.dumps(user_data, indent=4))
        pin_window.destroy()
        root.destroy()

    tk.Button(pin_window, text="Submit Pin", command=submit_pin, font=custom_font).pack(pady=10)

    # When the pin window is closed, show the main window again
    pin_window.protocol("WM_DELETE_WINDOW", lambda: [pin_window.destroy(), root.deiconify()])

# Main window setup
root = tk.Tk()
root.title("Sign In / Login")
root.geometry("300x200")
root.configure(bg='#333333')
root.attributes("-alpha", 0)  # Start with a transparent window
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
sign_in_button = tk.Button(root, text="Sign In", command=submit_action, font=custom_font, width=13, height=1, bg='grey', borderwidth=5)
login_button = tk.Button(root, text="Login", command=submit_action, font=custom_font, width=13, height=1, bg='grey', borderwidth=5)
sign_in_button.pack(pady=1)
login_button.pack(pady=2)

Forget_button = tk.Button(root, text="Forget My Info", command=forget_action, bg='grey', borderwidth=3)
Forget_button.pack(pady=5)


# Fade in the main window
fade_in(root)

root.mainloop()
