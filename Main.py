from Requirments.Install_Packages import install_packages
## try and find wheather all libraries have been download or not
try:
 from Libraries import *  
except ModuleNotFoundError as e:
    ## if the library is not found install it
    install_packages()

from Libraries import subprocess, sr, time 
from Voice_Assistant.Speak import Speak
from Module import *
from Voice_Assistant.Activision import system_Info_On
## Check if the file did not go through the activsion file (for auth)

data = system_Info_On()
if data["System"]["Active"] == False:
    pass
    #subprocess.Popen(["python", "System_Activision.py"])
    #quit()
else:
 #status = Check_Email_Accessability()
 #if(status == False):
     #Speak("Email Configuration Failed", -1, 1.0)
    # subprocess.Popen(["python", "System_Activision.py"])
    # quit()
 #else:
     greetings = shuffleTxtEntry()
     Speak(greetings, -1, 1.0)
 
def listen_for_keywords():
    with sr.Microphone() as source:
        #audio = recognizer.listen(source)
        try:    
         audio_data = recognizer.listen(source, timeout=1800, phrase_time_limit=5) 
         save_audio_as_wav(audio_data, "Database/bin/user_input.wav")
         recognized_text = process_wav_file("Database/bin/user_input.wav")
         delete_recording("Database/bin/resampled_audio_file1.wav")
         delete_recording("Database/bin/processed_audio.wav")
         delete_recording("Database/bin/user_input.wav")
         if(recognized_text == False):
            Speak("Entering Sleep MODE", -1, 1.0)
            SleepMode()
            greetings = shuffleTxtEntry()
            print(greetings)
            Speak(greetings, -1, 1.0)
            listen_for_keywords()
        #print(x)
        except sr.WaitTimeoutError:
            print("No speech detected for 30 min. Retrying...")
            SleepMode()
            listen_for_keywords()
        
    try:
        #recognized_text = recognizer.recognize_google(audio).lower()

        if ("Taylor" in recognized_text):
            Speak("ty t!", -1, 1.0)
            
        
        elif ("quit" in recognized_text):
            Speak("quitting..", -1, 1.0)
            subprocess.Popen(["python", "System_Activision.py"])
            quit()
        ###########################################
        ## Email Services: Send email ##
        ###########################################
        elif ("send an email" in recognized_text):
                time.sleep(0.1)
                #send_email("hi", "hi", "aldosari.mkj@gmail.com", "name")
                Speak("This is the email service.. still in progress", -1, 1.0)
                #pass
         
        ###########################################
        ## Email Services: observe emails ##
        ###########################################   
        elif ("observe" in recognized_text) or ("new emails" in recognized_text) or ("check email" in recognized_text):
            Speak("This is the email service.. still in progress", -1, 1.0)
           # pass
        ###########################################
        ## Wbsite hanlder: ##
        ###########################################
        elif ("open" and "website" in recognized_text):
            Speak("This is the open website service.. still in progress", -1, 1.0)
            #pass
        
        ###########################################
        ## Clear data stored in json file ##
        ###########################################   
        elif ("clear data" in recognized_text):
            pass
        else:
            print("No specific keyword detected.")
            listen_for_keywords()

    except sr.UnknownValueError:
        Speak("I could not understand the audio", -1, 1.0)
        listen_for_keywords()
    except sr.RequestError as e:
        Speak("Could not request results; {0}".format(e), -1, 1.0)
        listen_for_keywords()
#while True:
    #listen_for_keywords()

if __name__ == "__main__":
   listen_for_keywords() 
