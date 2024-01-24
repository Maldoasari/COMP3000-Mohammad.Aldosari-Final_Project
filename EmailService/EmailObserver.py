import base64
import os
import json
import re
import speech_recognition as sr
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Assuming Voice_Assistant.Speak module exists in your project
from Voice_Assistant.Speak import Speak
num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

def word_to_number(word):
    mapping = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
        "nineteen": 19, "twenty": 20
    }
    return mapping.get(word, word)

def get_credentials():
    creds = None
    if os.path.exists('Database/credentials.json'):
        with open('Database/credentials.json', 'r') as file:
            creds_data = json.load(file)
        creds = Credentials(token=creds_data.get('token'),
                            refresh_token=creds_data.get('refresh_token'),
                            token_uri=creds_data.get('token_uri'),
                            client_id=creds_data.get('client_id'),
                            client_secret=creds_data.get('client_secret'),
                            scopes=['https://www.googleapis.com/auth/gmail.readonly'])

        if creds and creds.expired:
            creds.refresh(Request())

    return creds

def get_emails():
    credentials = get_credentials()
    service = build('gmail', 'v1', credentials=credentials)
    
    try:
        # Fetching only unread emails
        response = service.users().messages().list(userId='me', q='is:unread').execute()
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    messages = response.get('messages', [])
    emails = []

    for msg in messages:
        try:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            payload = txt['payload']
            headers = payload['headers']
            subject = next(d['value'] for d in headers if d['name'] == 'Subject')
            sender = next(d['value'] for d in headers if d['name'] == 'From')

            parts = payload.get('parts', [payload])
            body = ""
            for part in parts:
                part_body = part.get('body', {})
                part_data = part_body.get('data')
                if part_data:
                    part_data = part_data.replace("-", "+").replace("_", "/")
                    decoded_data = base64.b64decode(part_data)
                    body += decoded_data.decode('utf-8')
            emails.append((msg['id'], sender, subject, body))
        except Exception as e:
            print(f"An error occurred while processing message {msg['id']}: {e}")

    return emails


def view_email_content(email_id, email_list):
    for e_id, sender, subject, body in email_list:
        if e_id == email_id:
            print(f"\nFrom: {sender}")
            print(f"Subject: {subject}")
            print(f"\n{body}")
            Speak(f"Email From: {sender}. Subject: {subject}. Message: {body}", -1, 1.0)
            return
    print("Email not found.")

def listen_for_id(emails):
    Speak("Which email you want to open", 0, 1.0)
    recognizer = sr.Recognizer()
    emailID = None

    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            Capture = recognizer.recognize_google(audio).lower()
            index_to_change = None
            
            for n in num:
                if n in Capture:
                    index_to_change = word_to_number(n)
                    if index_to_change is not None and index_to_change < len(emails):
                        emailID = emails[index_to_change][0]  # Getting the email ID
                        break
            
            if index_to_change is None:
                numbers = re.findall(r'\b\d+\b', Capture)
                if numbers:
                    index_to_change = int(numbers[0])
                    if index_to_change < len(emails):
                        emailID = emails[index_to_change][0]

        except sr.UnknownValueError:
            Speak("Sorry, I couldn't understand the audio.", 0, 1.0)
        except sr.RequestError as e:
            Speak("API unavailable or quota exceeded.", 0, 1.0)

    return emailID

    