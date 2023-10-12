from Requirments.Install_Packages import install_packages

try:
 from Voice_Assistant.Lib import *  
 ##here
except ModuleNotFoundError as e:
    install_packages()
    
from Voice_Assistant.Lib import *  
greetings = shuffleTxtEntry()
Speak(greetings, -1, 1.0)

def listen_for_keywords():
  
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio).lower()
        print("You said:", recognized_text)

        
        if ("Taylor" in recognized_text):
            print("ty t!")
            
        
        elif ("quit" in recognized_text):
            Speak("Quiting..")
            print("quiting..")
            subprocess.Popen(["python", "System_Activision.py"])
            quit()
        ###########################################
        ## Email Services: Send email ##
        ###########################################
        elif ("send an email" in recognized_text):
                time.sleep(0.1)
                Speak("This is the email service.. still in progress", -1, 1.0)
                pass
         
        ###########################################
        ## Email Services: observe emails ##
        ###########################################   
        elif ("observe" in recognized_text) or ("new emails" in recognized_text):
            Speak("This is the email service.. still in progress", -1, 1.0)
            pass
        ###########################################
        ## Wbsite hanlder: ##
        ###########################################
        elif ("open" and "website" in recognized_text):
            Speak("This is the open website service.. still in progress", -1, 1.0)
            pass
        
        ###########################################
        ## Clear data stored in json file ##
        ###########################################   
        elif ("clear data" in recognized_text):
            pass
        else:
            print("No specific keyword detected.")

    except sr.UnknownValueError:
        Speak("I could not understand the audio", -1, 1.0)
        listen_for_keywords()
    except sr.RequestError as e:
        Speak("Could not request results; {0}".format(e), -1, 1.0)
        listen_for_keywords()
#while True:
    #listen_for_keywords()
while True:
   listen_for_keywords() 
