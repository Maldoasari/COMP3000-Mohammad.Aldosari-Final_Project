from Requirments.Install_Packages import install_packages
## try and find wheather all libraries have been download or not
try:
 from Libraries import *  
except ModuleNotFoundError as e:
    ## if the library is not found install it
    install_packages()
except OSError as e:
    print(e)
    pass

    
from Libraries import subprocess, sr, time, recognizer
from Voice_Assistant.Speak import Speak
from Module import *
from Voice_Assistant.Activision import system_Info_On
## Check if the file did not go through the activsion file (for auth)

"""""
data = system_Info_On()
if data["System"]["Active"] == False:
    pass
    subprocess.Popen(["python", "System_Activision.py"])
    quit()
else:
 status = Check_Email_Accessability()
 if(status == False):
     Speak("Email Configuration Failed", -1, 1.0)
     subprocess.Popen(["python", "System_Activision.py"])
     quit()
 else:
 
  greetings = shuffleTxtEntry()
  Speak(greetings, -1, 1.0)
"""
greetings = shuffleTxtEntry()
Speak(greetings, -1, 1.0)
 
def listen_for_keywords():
    with sr.Microphone() as source:
        #audio = recognizer.listen(source)
        try:    
         audio_data = recognizer.listen(source, timeout=1800, phrase_time_limit=6) 
         save_audio_as_wav(audio_data, "Database/bin/user_input.wav")
         start_time = time.time()
         recognized_text = process_wav_file("Database/bin/user_input.wav")
         end_time = time.time()
         elapsed_time = end_time - start_time
         print(f"Function took {elapsed_time:.6f} seconds to execute.")
         if(recognized_text == False):
            Speak("Entering Sleep MODE", -1, 1.0)
            SleepMode()
            greetings = shuffleTxtEntry()
            print(greetings)
            Speak(greetings, -1, 1.0)
            listen_for_keywords()
         elif(recognized_text == 500):
             Speak("I could not understand the audio", -1, 1.0)
             listen_for_keywords()
         else:
             pass
        #print(x)
        except sr.WaitTimeoutError:
            print("No speech detected in 30 min. Retrying...")
            SleepMode()
            greetings = shuffleTxtEntry()
            print(greetings)
            Speak(greetings, -1, 1.0)
            listen_for_keywords()
        except sr.UnknownValueError:
            Speak("Entering Sleep MODE", -1, 1.0)
            SleepMode()
            greetings = shuffleTxtEntry()
            print(greetings)
            Speak(greetings, -1, 1.0)
            listen_for_keywords()

        
    try:
        delete_recording("Database/bin/resampled_audio_file1.wav", "Database/bin/processed_audio.wav", "Database/bin/user_input.wav", "Database/bin/vad_combined_audio.wav")
         #recognized_text = recognizer.recognize_google(audio).lower()
        if ("taylor" in recognized_text) and ("how are you" in recognized_text):
            Speak("ty t!", -1, 1.0)
            
        
        elif ("quit" in recognized_text):
            Speak("quitting..", -1, 1.0)
            subprocess.Popen(["python", "System_Activision.py"])
            quit()
        ###########################################
        ## Email Services: Send email ##
        ###########################################
        elif ("send an email" in recognized_text) or ("send email" in recognized_text) or ("email service" in recognized_text):
                time.sleep(0.1)
                Speak("Would you like to add new. or pick from storage?", -1, 1.0)
                Add_or_Storage = AddNew_or_ChooseFromStorage()
                if(Add_or_Storage == "add"):
                 Speak("Brillent, you have chosen the add new record service. To who?", -1, 1.0)
                 email_address = whoIStheR()
                elif(Add_or_Storage == "storage"):
                    Speak("Brillent, you picked to choose from storage", -1, 1.0)
                    email_address = storage()
                else:
                    Speak("The Defult path is Adding new email. To who?", -1, 1.0)
                    email_address = whoIStheR()
                time.sleep(1)
                print("Email:\n", email_address)
                time.sleep(2)
                Speak("What is the Subject?", -1, 1.0)
                email_subject = Subject()
                time.sleep(1)
                print("Subject:\n",email_subject)
                time.sleep(1)
                Speak("What is your message?", -1, 1.0)
                email_message = ReadMsg()
                time.sleep(1)
                print("Message:\n",email_message)
                time.sleep(1)
                Speak("What his. or her. or its name?", -1, 1.0)
                Speak("Say space to add space", -1, 1.0)
                email_name = ReadName()
                time.sleep(1)
                print("Name:\n",email_name)
                time.sleep(1)
                Speak("Would you like to send?", -1, 1.0)
                status = check()
                if status == True:
                    send_email(email_subject, email_message, email_address, email_name)
                    Speak("Email has been sent with success", -1, 1.0)
                    x = get_name_email(email_name, email_address)
                    Speak(f"Also, {x} with success", -1, 1.0)
                else:
                    print("\nSomething went wrong\n")
                    greetings = shuffleTxtEntry()
                    print(greetings)
                    Speak(greetings, -1, 1.0)
                    listen_for_keywords()
                #send_email("hi", "hi", "aldosari.mkj@gmail.com", "name")
                Speak("This is the email service.. still in progress", -1, 1.0)
                #Debugging and full test of its functionality next day!
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
