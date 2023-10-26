import imaplib
from email import policy
from email.parser import BytesParser
import re
from Voice_Assistant.Speak import Speak
import speech_recognition as sr
import json

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

def get_emails(n=5):
    try:
      with open("Database/Data.json", "r") as file:
          data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    EMAIL = data['Login']['L_email']
    APP_PASSWORD = data['Login']['E_APIKEY']
    
    # Connect to Gmail and fetch emails
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL, APP_PASSWORD)
    mail.select('inbox')
    status, email_ids = mail.search(None, 'ALL')
    email_ids = email_ids[0].split()
    # Retrieve and print the latest n emails
    emails = []
    num = 0
    for e_id in email_ids[-n:]:
        num = num + 1
        status, data = mail.fetch(e_id, '(RFC822)')
        email_bytes = data[0][1]  # Get the email bytes
        msg = BytesParser(policy=policy.default).parsebytes(email_bytes)
        emails.append((e_id.decode('utf-8'), msg))
        print(f"{num}. {msg['from']}. This email has {e_id.decode('utf-8')} as an ID")
        #Speak(f"{e_id.decode('utf-8')}. From, {msg['from']}", 0, 1.0)
    Speak(f"you have got{n} new emails", 0, 1.0)

    mail.logout()
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


recognizer = sr.Recognizer()
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

