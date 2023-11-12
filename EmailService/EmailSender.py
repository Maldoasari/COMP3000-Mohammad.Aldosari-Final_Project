from tkinter import messagebox
from Libraries import imaplib, smtplib, MIMEText, json
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
           data = json.load(file)
           if(data["Login"]["L_email"] == "") or (data["Login"]["E_APIKEY"] == ""):
              return 404
           else:
              SMTP_email = data['Login']['L_email']
              SMTP_pass = data['Login']['E_APIKEY']
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
        with open("Database/Data.json", 'r') as file:
         data = json.load(file)
         data["Login"]["L_email"] = ""
         data["Login"]["E_APIKEY"] = ""
         # Write the updated data back to the JSON file
        with open("Database/Data.json", 'w') as file:
         json.dump(data, file, indent=4)
    # Handle exceptions (e.g., authentication failure, connection errors)
        print(f"An error occurred: {e}")
        return 0


