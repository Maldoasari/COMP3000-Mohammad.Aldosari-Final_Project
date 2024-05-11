import subprocess
import json
import email, imaplib
from Voice_Assistant.Read_Email_Voice_Inputs import Get
from Voice_Assistant.Speak import Speak
from EmailService.EmailStatus import Check_Email_Status
import speech_recognition as sr
from EmailService.EmailSender import send_email
from Security.Resttful_API import Get_record_by_email
from Security.Cryptography import decrypt_text


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
    return mapping.get(word, None)

recognizer = sr.Recognizer()
num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twleve"]

def Check_Email_Accessability():
 # check if the email is accessable or not, this can be achived if credentials.json is not found
 Check_Email = Check_Email_Status() 

 if(Check_Email): 
  return True
 # if not found activate the Link_Gmail_Auth0.py script, which is about auth using Google console project created before
 else:
  command = ["python", "EmailService/Link_Gmail_Auth0.py"]
  subprocess.Popen(command)
  Speak("A window has been opned. you can login securly. to your gmail account to activate the email service", -1, 1.0)
  # to have a smooth and fast responce i created a json file that acts as a bridge between Link_Gmail_Auth0.py and this function
  # if the email status and useremail has chnaged to not None. then break, else keep running. 
  while True:
        data = Get("Database/Data.json")
        if isinstance(data, dict):
         status = data.get("email_ststus")
         useremail = data.get("User_email")
         
        if (status is not None) and (useremail is not None):
         status = status
         useremail = useremail
         
        if (status):
            send_email("Success", f"Email Service activated with Success", useremail, "User", "system email")
            break
        
        else:
            continue
        
  Speak("Brilint. you have activated the email service", -1, 1.0)
  return True
# a function to extract code and change the formate of the text when needed. 
# (e.g. from alphabetical formate to numrical values)
def Code_extractor():
    code = ""
    # listen for code
    with sr.Microphone() as source:
    
     while True:
        audio = recognizer.listen(source)
        
        try:
            
         Capture = recognizer.recognize_google(audio).lower()
         # get each element in Capture (user speaks the code)
         for c in Capture:
            # get each element in Num (a list of alphabetical formate numbers e.g. "zero", "one"...etc)
            for n in num:
                # if an element in Capture is one of the element in the list of alphabetical formate numbers. 
                # then convert it to numrical value and store it in x, then from from x store place it in code var.
                # this is when the alphabetical formate numbers is found or detected
                if c == n:
                    x = ''
                    x = word_to_number(c)
                    code = code + x
                # on the other hand, if an element in Capture is numrical value, then move it stright away to code var
                elif c.isdigit():
                    code = code + c
                    break 
                # the operation will be in a loop until it meets the req. 
                else:
                    continue
         break
     
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            continue
        
        except sr.RequestError:
            print("API unavailable or quota exceeded.")
            continue
        
    return code

"""""
def Store_Contacts():
    try:
      with open("Database/Data.json", "r") as file:
          data = json.load(file)
          if(data["User_email"] == ""):
              return 401
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    Getdata = Get_record_by_email(data["User_email"])
    decryptKey = decrypt_text(Getdata["email_service_login_pass"])
    IMAP_email = Getdata['email_service_login_email']
    IMAP = decryptKey
    # Gmail IMAP settings
    imap_url = 'imap.gmail.com'
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(IMAP_email, IMAP)
    mail.select('inbox')  

    result, data = mail.search(None, 'ALL')
    email_ids = data[0].split()

    contacts = {}

    for e_id in email_ids:
        
        result, data = mail.fetch(e_id, '(RFC822)')
        raw_email = data[0][1]
        
        email_message = email.message_from_bytes(raw_email)

        
        from_header = email.utils.parseaddr(email_message['From'])
        email_addr = from_header[1]
        name = from_header[0]
    
        if name:
            name = str(email.header.make_header(email.header.decode_header(name)))
        
        if email_addr and email_addr not in contacts:
            contacts[email_addr] = name

    contacts_list = [{'name': name, 'email': email} for email, name in contacts.items()]


    with open('Database/cookies.json', 'w') as json_file:
        json.dump(contacts_list, json_file, indent=4)


    mail.logout()
"""