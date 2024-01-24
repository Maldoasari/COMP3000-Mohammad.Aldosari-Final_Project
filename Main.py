from distutils.command import build
import subprocess
from EmailService.EmailObserver import view_email_content
from Libraries import sr, time, recognizer, json
from Voice_Assistant.Speak import Speak
from Module import *
from Web_BrowsingService.WebBrowsing import Website_Browsing_openPage_Handler   

# Login or Sign Up checks: 
# If the user has failed to login or sign in the application will automaticlly quit

valid = LoginOrSign()
if valid[0] == False:
    Speak("Login or Sign up Failed", -1, 1.0)
    quit()

# After a successfull login or sign in the system will greet the user:
greetings = shuffleTxtEntry()
Speak(greetings, -1, 1.0)

# this is listen function that would listen non-stop, until the user quits the program
def listen_for_keywords():
    
    with sr.Microphone() as source:
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

        if ("Taylor" in recognized_text) and ("how are you" in recognized_text):
            Speak("I am good. how about you?", -1, 1.0)
            listen_for_keywords()
            
        elif ("Taylor" in recognized_text) and ("quit" in recognized_text):
            Speak("quitting..", -1, 1.0)
            DisableSys()
            subprocess.Popen(["python", "System_Activision.py"])
            quit()
            
        ###########################################
        ## Email Services: Send email ##
        ###########################################
        elif ("Taylor" in recognized_text) and ("send an email" in recognized_text) or ("send email" in recognized_text) or ("email service" in recognized_text):
                status = Check_Email_Accessability()
                if(status == False):
                   Speak("Email Configuration Failed", -1, 1.0)
                   DisableSys()
                   subprocess.Popen(["python", "System_Activision.py"])
                   quit()
                   
                generate_email = Generate_Email()
                Speak("Would you like to send?", -1, 1.0)
                status = check()
                if status == True:
                    send_email(generate_email[0], generate_email[1], generate_email[2], generate_email[3], 'user email')
                    Speak("Email has been sent with success", -1, 1.0)
                    store_email = get_name_email(generate_email[3], generate_email[2])
                    Speak(f"Also, {store_email} with success", -1, 1.0)
                else:
                    print("\nSomething went wrong\n")
                    Speak("Something went wrong", -1, 1.0)
                    listen_for_keywords()
                    
                listen_for_keywords()
                

        ###########################################
        ## Email Services: observe emails ##
        ###########################################   
        elif ("Taylor" in recognized_text) and ("observe" in recognized_text) or ("new emails" in recognized_text) or ("check email" in recognized_text):
            status = Check_Email_Accessability()
            emails = get_emails()
            if emails:
                for i, (id, sender, subject, _) in enumerate(emails):
                    print(f"{i}: From {sender}, Subject: {subject}")
                selected_email_id = listen_for_id(emails)
                if selected_email_id:
                    view_email_content(selected_email_id, emails)
                else:
                    print("No email selected or understood.")
            else:
                print("No new emails.")
            Speak("This is the email service.. still in progress", -1, 1.0)
            listen_for_keywords()
            
            
        ###########################################
        ## Wbsite hanlder: ##
        ###########################################
        elif ("open" in recognized_text) and ("website" in recognized_text):
            url = webNameHandler(recognized_text)
            url = web_Search(url)
            Website_openPage_Handler(url)
            listen_for_keywords()
            
        ###########################################
        ## Wbsite Browsing (Google): ##
        ###########################################
        elif ("search" in recognized_text) and ("engine" in recognized_text):
            url = "https://www.google.com"
            Website_Browsing_openPage_Handler(url)
            listen_for_keywords()
            
        
        ###########################################
        ## Clear data stored in json file ##
        ###########################################   
        elif ("Taylor" in recognized_text) and ("clear cache" in recognized_text):
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

def DisableSys():
    try:
     with open("System.json", "r") as file:
      data = json.load(file)
      data["System"]["Active"] = False
    except (FileNotFoundError, json.JSONDecodeError):
     pass
    with open("System.json", 'w') as file:
     json.dump(data, file, indent=4)

def Generate_Email():
    subprocess.Popen(["python", "Voice_Assistant/Read_Email_Voice_Inputs.py"])
    generate_email = []
    check_Storage = storageCheck()
    if (check_Storage == None):
        Speak("Brillent, What is the email?", -1, 1.0)
        email_address = whoIStheR()
    else:  
        Speak("Would you like to add new. or pick from storage?", -1, 1.0)
        Add_or_Storage = AddNew_or_ChooseFromStorage()
        if(Add_or_Storage == "add"):
           Speak("Brillent, you have chosen the add new record service. To who?", -1, 1.0)
           email_address = whoIStheR()
        elif(Add_or_Storage == "storage"):
            Speak("Brillent, you picked to choose from storage", -1, 1.0)
            email_address = storage()
            if email_address == None:
                Speak("Add emails to store them", -1, 1.0)
                email_address = whoIStheR()
        else:
            Speak("The Defult path is Adding new email. To who?", -1, 1.0)
            email_address = whoIStheR()
    time.sleep(1)
    POST("Database/Content.json", "Email", "post", email_address)
    print("Email:\n", email_address)
    POST("Database/Content.json", "system", "post", " ")
    time.sleep(2)
    Speak("What is the Subject?", -1, 1.0)
    email_subject = Subject()
    time.sleep(1)
    POST("Database/Content.json", "Subject", "post", email_subject)
    print("Subject:\n",email_subject)
    POST("Database/Content.json", "system", "post", " ")
    time.sleep(1)
    Speak("What is your message?", -1, 1.0)
    email_message = ReadMsg()
    time.sleep(1)
    POST("Database/Content.json", "message", "post", email_message)
    POST("Database/Content.json", "system", "post", " ")
    print("Message:\n",email_message)
    time.sleep(1)
    Speak("What his. or her. or its name?", -1, 1.0)
    Speak("Say space to add space", -1, 1.0)
    email_name = ReadName()
    time.sleep(1)
    POST("Database/Content.json", "Name", "post", email_name)
    print("Name:\n",email_name)
    time.sleep(1)
    generate_email = [email_subject, email_message, email_address, email_name]
    return generate_email
 
if __name__ == "__main__":
   listen_for_keywords() 
