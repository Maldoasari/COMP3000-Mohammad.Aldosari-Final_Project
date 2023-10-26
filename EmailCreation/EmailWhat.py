from Voice_Assistant.Speak import Speak
from Libraries import sr, recognizer
   
def checkSub(sub):
    Do_Again = sub
    subject = ''
    Speak("Say yes to confirm. or no to rewrite the subject\n", 0, 1.0)
    with sr.Microphone() as source:
     print("\nYes or No...")
     audio = recognizer.listen(source)
     Capture = recognizer.recognize_google(audio).lower()
    try:
     if "yes" in Capture:
        subject = sub.capitalize() 
        Speak(f"Subject is {subject}\n", 0, 1.0)
        print("Structring Subject...")
        return subject
    
     elif "no" in Capture:
        Speak(f"What would you like me to chnage to?\n", 0, 1.0)
        subject = Subject()
     else:
        Speak(f"Sorry, Didn't catch it\n", 0, 1.0)
        print("Sorry, Didn't catch it")
        subject = checkSub(Do_Again)
    except sr.UnknownValueError:
        Speak("Could not understand audio", 0, 1.0)
        print("Could not understand audio")
        subject = checkSub(Do_Again)
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
        subject = recognizer.recognize_google(audio).lower()
    try:
        Speak(f"Do You Confirm That you have said:{subject}\n", 0, 1.0)
        print("Do You Confirm That you have said:\n", subject)
        Email_Subject = checkSub(subject)
        return Email_Subject 
    except sr.UnknownValueError:
        Speak("Could not understand audio", 0, 1.0)
        print("Could not understand audio")
        Speak("What is the Subject?", -1, 1.0)
        Email_Subject = Subject() 
    except sr.RequestError as e:
        Speak("Could not request results {0}".format(e), 0, 1.0)
        print("Could not request results; {0}".format(e))
        Speak("Retrying, What is the Subject?", -1, 1.0)
        Email_Subject = Subject() 
    return Email_Subject 
