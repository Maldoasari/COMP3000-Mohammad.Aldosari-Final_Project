import atexit
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
import webbrowser
from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)

CLIENT_SECRETS_FILE = 'EmailService/cre.json'  
REDIRECT_URI = 'https://localhost:5000/callback'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CERTIFICATE_PATH = 'EmailService/cert.pem'
PRIVATE_KEY_PATH = 'EmailService/key.pem'
CREDENTIALS_FILE = 'Database/credentials.json'

def store_credentials(credentials):
    # Store credentials in a file
    with open(CREDENTIALS_FILE, 'w') as credentials_file:
        credentials_file.write(credentials.to_json())
def POST(Jsonfile, tragetData, status, input):
    with open(Jsonfile, 'r') as file:
        data = json.load(file)
    if status == "post":
      data[f"{tragetData}"] =  input
      with open(Jsonfile, 'w') as file:
         json.dump(data, file, indent=4)
    else:
        return 501

@app.route('/')
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )

    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials

    # Store credentials for later use
    store_credentials(credentials)
    POST("Database/data.json", "email_ststus", "post", True)
    return "Linked with success.."

def send_email(credentials):
    """Send an email using Gmail API."""
    # Build Gmail API service
    service = build('gmail', 'v1', credentials=credentials)

    # Construct the email message
    email_message = create_email_message(
        sender='jax.wood.m@gmail.com',
        to='jax.wood.m@example.com',
        subject='Your Subject',
        body='Your email body content'
    )

    # Send the email
    send_message(service, 'me', email_message)

def create_email_message(sender, to, subject, body):
    """Create a MIMEText email message."""
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg_body = MIMEText(body)
    message.attach(msg_body)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    return {'raw': raw_message}

def load_credentials():
    """Load OAuth 2.0 credentials from a file."""
    if os.path.exists(CREDENTIALS_FILE):
        try:
            with open(CREDENTIALS_FILE, 'r') as credentials_file:
                credentials_data = json.load(credentials_file)
                flow = InstalledAppFlow.from_client_config(credentials_data, SCOPES)
                credentials = flow.run_local_server(port=0)
                return credentials
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    return None

def send_message(service, user_id, message):
    """Send an email message using the Gmail API."""
    try:
        sent_message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f"Message sent! Message Id: {sent_message['id']}")
        return sent_message
    except Exception as e:
        print(f"Error sending email: {e}")
        return None

        
if __name__ == '__main__':
    # Run the Flask app without the reloader
    webbrowser.open('https://127.0.0.1:5000')
    app.run(debug=False, ssl_context=(CERTIFICATE_PATH, PRIVATE_KEY_PATH))
    
