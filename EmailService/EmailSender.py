import os
from tkinter import messagebox
from Libraries import imaplib, smtplib, MIMEText, json
from Security.Cryptography import decrypt_text
from Security.Resttful_API import Get_record_by_email, Update_record_by_email
from google_auth_oauthlib.flow import Flow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CREDENTIALS_FILE = 'Database/credentials.json'

def load_credentials():
    # Load credentials from a file
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as credentials_file:
            credentials_data = json.load(credentials_file)
            return Flow.from_client_config(credentials_data, SCOPES).credentials
    return None

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
        with open("Database/Data.json", "r") as file:
          GetEmail = json.load(file)
          GetEmail = GetEmail["User_email"]
          data = Get_record_by_email(GetEmail)
          decryptKey = decrypt_text(data["email_service_login_pass"])
        if(len(data["email_service_login_email"]) == 0) or (len(decryptKey) == 0):
              return 400
        else:
              SMTP_email = data["email_service_login_email"]
              SMTP_pass = decryptKey
              status = checkAccess(SMTP_SERVER, SMTP_PORT, SMTP_email, SMTP_pass)
              if status == 1:
                  pass
              else:
                  return 0
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


