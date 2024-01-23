import base64
from email import message_from_bytes
import os
from Security.Cryptography import decrypt_text
from Security.Resttful_API import Get_record_by_email
from Voice_Assistant.Speak import Speak
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from Libraries import sr, json, re, imaplib, BytesParser, policy, recognizer
def word_to_number(word):
    mapping = {
        "zero": 0,
        "hero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11
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
                            scopes=creds_data.get('scopes'))

        if creds and creds.expired:
            creds.refresh(Request())

    return creds


def get_emails(n=5):
    credentials = get_credentials()

    # Setting up the Gmail API
    service = build('gmail', 'v1', credentials=credentials)

    # Fetching the latest n emails
    try:
     response = service.users().messages().list(userId='me', maxResults=n).execute()
    except Exception as e:
     print(f"An error occurred: {type(e).__name__}, {str(e)}")
     return []


    messages = response.get('messages', [])

    emails = []
    for msg in messages:
        try:
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            # Process the message
            payload = txt['payload']
            headers = payload['headers']

            # Extract subject and sender
            subject = next(d['value'] for d in headers if d['name'] == 'Subject')
            sender = next(d['value'] for d in headers if d['name'] == 'From')

            # Extract the body
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


def extract_content(message):
    if message.is_multipart():
        # For multipart messages, we'll dive into each part.
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            # Check if it's a text/plain or text/html content.
            if content_type == "text/plain" and "attachment" not in content_disposition:
                return part.get_payload(decode=True).decode()
            elif content_type == "text/html" and "attachment" not in content_disposition:
                html_content = part.get_payload(decode=True).decode()
                # If you prefer plain text over HTML, you can use some libraries to strip HTML tags.
                # For now, I'll return HTML content as it is.
                return html_content
    else:
        # For non-multipart messages.
        return message.get_payload(decode=True).decode()

def view_email_content(email_id, email_list):
    l = 0
    for e_id, msg in email_list:
        print(e_id, email_list[l])
        l = l + 1
        if e_id == email_id:
            EmailF = msg['from']
            EmailS = msg['subject']
            print("\nFrom:", msg['from'])
            print("Subject:", msg['subject'])
            content = extract_content(msg)
            print("\n", content)
            Speak(f"Email From:{EmailF}. Subject: {EmailS}. Message: {content}", -1, 1.0)
            return
    print("Email not found.")


num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twleve"]
def Listen_for_id(emails):
    Speak("Which email you want to open", 0, 1.0)
    emailID = None
    do_again = emails
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            Capture = recognizer.recognize_google(audio).lower()
            index_to_change = None  # Initialize with None
            
            for n in num:
                if n in Capture:
                    index_to_change = word_to_number(n)
                    if index_to_change is None or index_to_change > len(emails):
                        Speak("list index out of range", 0, 1.0)
                        return Listen_for_id(do_again)   # Using return to ensure we break out
                    else:
                        break
                
            if index_to_change is None:
                numbers = re.findall(r'\b\d+\b', Capture)
                if numbers:
                    index_to_change = int(numbers[0])
                    if index_to_change > len(emails):
                        Speak("list index out of range", 0, 1.0)
                        return Listen_for_id(do_again)   # Using return to ensure we break out
                        
            if index_to_change is None:
                Speak("Let's try again", 0, 1.0)
                return Listen_for_id(do_again)  # Using return to ensure we break out
            #print(int(Capture[-1]))
            emailID = index_to_change
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            Speak("Sorry, I couldn't understand the audio.", 0, 1.0)
            print("lets try again\n")
            Speak("lets try again\n", 0, 1.0)
            return Listen_for_id(do_again)

        except sr.RequestError:
            print("API unavailable or quota exceeded.")
            return Listen_for_id(do_again)

    # If for any other reason we reach here
    #print(emailID)   # Debugging: print the emailID (should be None)
    return emailID

