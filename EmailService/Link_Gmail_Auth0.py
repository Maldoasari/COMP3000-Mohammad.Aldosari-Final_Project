import os
import json
import webbrowser
from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

app = Flask(__name__)

CLIENT_SECRETS_FILE = 'cre.json'  # Replace with the path to your client secrets file
REDIRECT_URI = 'https://localhost:5000/callback'
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CERTIFICATE_PATH = 'cert.pem'
PRIVATE_KEY_PATH = 'key.pem'
CREDENTIALS_FILE = 'credentials.json'

def store_credentials(credentials):
    # Store credentials in a file
    with open(CREDENTIALS_FILE, 'w') as credentials_file:
        credentials_file.write(credentials.to_json())

def load_credentials():
    # Load credentials from a file
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as credentials_file:
            credentials_data = json.load(credentials_file)
            return Flow.from_client_config(credentials_data, SCOPES).credentials
    return None

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

    # Example: Send an email using Gmail API
    send_email(credentials)

    return 'Gmail account linked successfully.'

def send_email(credentials):
    # Build Gmail API service
    service = build('gmail', 'v1', credentials=credentials)

if __name__ == '__main__':
    # Load credentials if available
    existing_credentials = load_credentials()

    if existing_credentials:
        print("Using existing credentials.")
        quit()
    else:
        print("Credentials not found. Please run the app and authenticate.")
    # Run the Flask app without the reloader
    webbrowser.open('https://127.0.0.1:5000')
    app.run(debug=False, ssl_context=(CERTIFICATE_PATH, PRIVATE_KEY_PATH))
