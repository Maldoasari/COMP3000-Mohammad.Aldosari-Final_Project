from tkinter import messagebox
import imaplib, smtplib, json
from email.mime.text import MIMEText
from Security.Resttful_API import Update_record_by_email
import base64
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

def delete_all_emails(user_email, app_password):
    
    # Connect to Gmail's IMAP server
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(user_email, app_password)
    
    # Select All Mail label (it includes inbox, sent, drafts, etc.)
    mail.select('"[Gmail]/Sent Mail"')
    
    # Search for all emails
    result, data = mail.search(None, "ALL")
    if result == 'OK':
        for num in data[0].split():
            # Mark email for deletion
            mail.store(num, '+FLAGS', '\\Deleted')
        # Expunge (permanently remove) emails marked for deletion
        mail.expunge()
        print("All emails have been deleted!")
    else:
        print("Error searching for emails.")

    # Logout and close connection
    mail.logout()
    
def send_email(subject, message_body, to_email, nameOfRec, type):
     # Send email
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    
    try:
      if type == "system email":   
       with open("System.json", "r") as file:
          data = json.load(file)
          if(data["System"]["EmailAddress"] == "") or (data["System"]["Ekey"] == ""):
              return 500
          else:
              SMTP_email = data['System']['EmailAddress']
              SMTP_pass = data['System']['Ekey']
      elif type == "user email":
         User_Email(subject, message_body, to_email, nameOfRec)
         return
    except (FileNotFoundError, json.JSONDecodeError):
        pass
        
    email_body = f"""
Hello From Taylor,
This Message is on behalf of MR.Aldosari Mohammad Saying:
Dear {nameOfRec}, 
    
    
{message_body}

    
I hope this email finds you well.

Regards,
TYM
note: don't replay to this email as it will not be seen.
Try this: jax.wood.m@gmail.com
"""
    
    try:
        # Create message and GET email config
        msg = MIMEText(email_body)
        msg['From'] = SMTP_email
        msg['To'] = to_email
        msg['Subject'] = subject
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_email, SMTP_pass)  # Use the app password here.
        server.sendmail(SMTP_email, to_email, msg.as_string())
        server.close()
        #delete_all_emails(data['Login']['L_email'], data['Login']['L_password'])
        return 1
    except Exception as e:
        print(f'Error sending email: {e}')
        return 0
def User_Email(subject, message_body, to_email, nameOfRec):
    with open("Database/Data.json", "r") as file:
          GetEmail = json.load(file)
          GetEmail = GetEmail["User_email"]
    with open('Database/credentials.json', 'r') as file:
          credentials_data = json.load(file)
    # Create a Credentials object
    credentials = Credentials.from_authorized_user_info(credentials_data)
    
    # Check if the token is expired and refresh if necessary
    if credentials.expired:
        credentials.refresh(Request())

    # Set up the Gmail API
    service = build('gmail', 'v1', credentials=credentials)

    # Create a simple email message
    message = f"From: {GetEmail}\nTo: {to_email}\nSubject: {subject}\n\n {nameOfRec},\n {message_body}"

    # Encode the raw content in base64url
    raw_message_bytes = base64.urlsafe_b64encode(message.encode('utf-8'))
    raw_message_str = raw_message_bytes.decode('utf-8')

    # Send the email
    service.users().messages().send(userId='me', body={'raw': raw_message_str}).execute()

def checkAccess(SMTP_SERVER, SMTP_PORT, SMTP_email, SMTP_pass):
    try:
    # Create an SMTP server connection
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()  # Can be omitted
        server.starttls()
        server.ehlo()  # Can be omitted
        server.login(SMTP_email, SMTP_pass)  # Use the app password here.
        server.close()

    # If the login is successful, it means the credentials are correct
        return 1
    except Exception as e:
        messagebox.showerror("Error", "The Given email or and password is incorrect")
            #data = {"Login": {"L_email": "", "L_password": ""}}
        with open("Database/Data.json", "r") as file:
          GetEmail = json.load(file)
          GetEmail = GetEmail["User_email"]
        update_data = {
            "email_service_login_email": " ",
            "email_service_login_pass": " "}
        Update_record_by_email(GetEmail, update_data)
    # Handle exceptions (e.g., authentication failure, connection errors)
        print(f"An error occurred: {e}")
        return 0


