import re
from Libraries import tk, json, messagebox
import email, imaplib
from Voice_Assistant.Speak import Speak
from EmailService.EmailStatus import Check_Email_Status
import speech_recognition as sr
#from Module import Check_Email_Status, send_email, delete_all_emails
from EmailService.EmailSender import checkAccess, send_email, delete_all_emails
from EmailService.CodeGeneration import generate_random_5_digit_number
from Configuration.Config import SetUpApp
from Security.Resttful_API import Get_record_by_email, Update_record_by_email
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
 SMTP_SERVER = 'smtp.gmail.com'
 SMTP_PORT = 587
 Check_Email, email = Check_Email_Status() 
 if(Check_Email == False):
     Speak("The System cannot access your email. Here you go", -1, 1.0)
     root = tk.Tk()
     app = SetUpApp(root, "Set up Email", "lightblue", "grey", "Email")
     root.mainloop()
     data = Get_record_by_email(email)
     decryptKey = decrypt_text(data["email_service_login_pass"])
     SMTP_email = data["email_service_login_email"]
     SMTP_pass = decryptKey
     
     status = checkAccess(SMTP_SERVER, SMTP_PORT, SMTP_email, SMTP_pass)
     
     if status == 0:
        return False
    
     codeIS = generate_random_5_digit_number()
     x = send_email("Success", f"Please provide this email to the software to varify your email: \n {codeIS}", SMTP_email, "User", "system email")
     
     #0 is returning a flase.  
     if  x == 0:
            messagebox.showerror("Error", "The Given email or and password is incorrect")
            #data = {"Login": {"L_email": "", "L_password": ""}}
            update_data = {
            "email_service_login_email": " ",
            "email_service_login_pass": " "}
            Update_record_by_email(email, update_data)
            return False
     else:
            Speak("What is the code:\n", 0, 1.0)
            get_code = Code_extractor()
            if(codeIS == get_code):   
             messagebox.showinfo("Success", "Email Service configured with success")
             Store_Contacts()
            else:
                Speak("Invalid code \n", 0, 1.0)
                return False
            return True
 else:
     return True
 

def Code_extractor():
    code = ""
    with sr.Microphone() as source:
     while True:
        audio = recognizer.listen(source)
        try:
         Capture = recognizer.recognize_google(audio).lower()
         for c in Capture:
            for n in num:
                if c == n:
                    x = ''
                    x = word_to_number(c)
                    code = code + x
                elif c.isdigit():
                    code = code + c
                    break  
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
