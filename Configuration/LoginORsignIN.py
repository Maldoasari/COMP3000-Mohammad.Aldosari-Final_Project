import hashlib
import os
import subprocess
import sys
import time
import tkinter as tk
from tkinter import messagebox, font
import json
from EmailService.CodeGeneration import generate_random_5_digit_number
from EmailService.EmailAccessability import Code_extractor
from EmailService.EmailSender import send_email
from Security.Resttful_API import Post_record, Get_record_by_email
from Voice_Assistant.Speak import Speak
from Voice_Assistant.Read_Email_Voice_Inputs import POST, Get
from Security.Cryptography import create_database_directory, hash_password, verify_password
def LoginOrSign():
 count_Attempts = [4]
 x = []
 x.append(False)
 create_database_directory()
 data = Get("Database/Data.json")
 print(len(data["User_email"]))
 print(data["Time_Bi_Login"] <= 3)
 if (len(data["User_email"]) > 0) and (data["Time_Bi_Login"] < 3):
     atempt = data["Time_Bi_Login"] + 1
     POST("Database/Data.json", "Time_Bi_Login", 'post', atempt)
     x.clear()
     x.append(True)
     return x
 
 
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



# Function to attempt login
 def attempt_login(email, input, status):
    user_data = Get_record_by_email(email)
    if user_data == None:
        return False
    
    if status == "check password":
       password_verified = verify_password(user_data["password_login"], input)
       return password_verified
    elif status == "check pincode":
       pin_verified = verify_password(user_data["pincode_login"], input)
       return pin_verified
    else:
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
        "pincode_login": "",
        "password_login": hashed_password,
        "email_service_login_email": "",
        "email_service_login_pass": "",
        "netflix_username": "",
        "netflix_pass": "",
        "primeVideo_username": "",
        "primeVideo_pass": "",
        "spotify_Client_ID": "",
        "spotify_Client_Secret": ""
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
    if attempt_login(email, password, "check password"):
        count_Attempts[0] = 4
        open_login_pin_window(email)
    if count_Attempts[0] == 0:
        x.clear()
        x.append(False)
        root.destroy()
    else: 
     counts = count_Attempts[0] - 1
     count_Attempts.clear()
     count_Attempts.append(counts)
     messagebox.showerror("Invalid", f"Email and password invalid you have {counts} attempts left")
     return 

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
        x.clear()
        x.append(False)
        return False
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
        POST("Database/Data.json", "User_email", 'post', user_data["email_login"])
        x.clear()
        x.append(True)
        return True

    tk.Button(pin_window, text="Submit Pin", command=on_pin_submit, font=custom_font).pack(pady=10)

# Open Pin Window for login
 def open_login_pin_window(email):
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
        x.clear()
        x.append(False)
        return False

    login_pin_window.protocol("WM_DELETE_WINDOW", on_login_pin_window_close)
    def on_pin_submit():
        getstatus = None
        pin = pin_entry.get()
        if attempt_login(email, pin, "check pincode"):
            codeIS = generate_random_5_digit_number()
            send_email("Success", f"Please provide this email to the software to varify your email: \n {codeIS}", email, "User", "system email")
            count = 0
            while True:
             count = count + 1
             Speak("What is the code:\n", 0, 1.0)
             get_code = Code_extractor()
             if(codeIS == get_code):
              POST("Database/Data.json", "User_email", 'post', email) 
              POST("Database/Data.json", "Time_Bi_Login", 'post', 0)
              messagebox.showinfo("Login Successful", "You are now logged in.")
              getstatus = True
              break
             elif count == 4:
                 getstatus = False
                 break
             else:
                Speak("Incorrect\n", 0, 1.0)
                continue
        if getstatus == True:
            login_pin_window.destroy()
            root.destroy()
            x.clear()
            x.append(True)
            return getstatus  
        if getstatus == False:
            messagebox.showerror("Login Failed", "Invalid code.")
            x.clear()
            x.append(False)
            return getstatus
        if count_Attempts[0] == 0:
            x.clear()
            x.append(False)
            root.destroy()
        else:
            counts = count_Attempts[0] - 1
            count_Attempts.clear()
            count_Attempts.append(counts)
            messagebox.showerror("Invalid", f"Invalid pincode. you have {count_Attempts} left")
            #login_pin_window.destroy()
            return
        #login_pin_window.destroy()
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
 return x

 
 

