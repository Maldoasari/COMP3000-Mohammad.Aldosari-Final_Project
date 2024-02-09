from Voice_Assistant.Speak import Speak
from Voice_Assistant.Read_Email_Voice_Inputs import POST
import speech_recognition as sr
recognizer = sr.Recognizer()
def checkSub(sub):
    Do_Again = sub
    subject = ''
    Speak("Say yes to confirm. or no to rewrite the subject\n", 0, 1.0)
    with sr.Microphone() as source:
     print("\nYes or No...")
     audio = recognizer.listen(source)
    try:
     Capture = recognizer.recognize_google(audio).lower()
     if "yes" in Capture:
        subject = sub.capitalize() 
        POST("Database/Content.json", "system", "post", f"Subject is:\n {subject}")
        return subject
    
     elif "no" in Capture:
        Speak(f"What would you like me to change it to?\n", 0, 1.0)
        POST("Database/Content.json", "system", "post", " ")
        subject = Subject()
        return subject
     else:
        Speak(f"Sorry, Didn't catch it\n", 0, 1.0)
        print("Sorry, Didn't catch it")
        subject = checkSub(Do_Again)
        return subject
    except sr.UnknownValueError:
        Speak("Could not understand audio", 0, 1.0)
        print("Could not understand audio")
        subject = checkSub(Do_Again)
        return subject
    except sr.RequestError as e:
        Speak("Could not request results {0}".format(e), 0, 1.0)
        print("Could not request results; {0}".format(e))
        subject = checkSub(Do_Again)
        return subject
    

def Subject():
    
    Email_Subject = ''
    print("Subject?")
    #time.sleep(1.5)
    with sr.Microphone() as source:
       # print("Listening...")
        audio = recognizer.listen(source)
    try:
        subject = recognizer.recognize_google(audio).lower()
        Speak(f"Do You Confirm That you have said:{subject}\n", 0, 1.0)
        POST("Database/Content.json", "system", "post", f"DO You Confirm That you have said:\n {subject}")
        Email_Subject = checkSub(subject)
        return Email_Subject 
    except sr.UnknownValueError:
        Speak("Could not understand audio", 0, 1.0)
        print("Could not understand audio")
        Speak("What is the Subject?", -1, 1.0)
        Email_Subject = Subject()
        return Email_Subject 
    except sr.RequestError as e:
        Speak("Could not request results {0}".format(e), 0, 1.0)
        print("Could not request results; {0}".format(e))
        Speak("Retrying, What is the Subject?", -1, 1.0)
        Email_Subject = Subject() 
        return Email_Subject
    
