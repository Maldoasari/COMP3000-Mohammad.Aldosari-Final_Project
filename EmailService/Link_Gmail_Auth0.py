import json
from google_auth_oauthlib.flow import InstalledAppFlow
import webbrowser
from flask import Flask, redirect, request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import AuthorizedSession

app = Flask(__name__)

CLIENT_SECRETS_FILE = 'EmailService/cre.json'  
REDIRECT_URI = 'https://localhost:5000/callback'
SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly']
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

if __name__ == '__main__':
    # Run the Flask app without the reloader
    webbrowser.open('https://127.0.0.1:5000')
    app.run(debug=False, ssl_context=(CERTIFICATE_PATH, PRIVATE_KEY_PATH))
    
