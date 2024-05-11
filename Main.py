# THIS IS THE MAIN FILE AND ALL OPERATIONS/OTHER FILES ARE LINKED HERE
# THE FIRST SECTION OF THIS FILE IS ADDING AND IMPORTING THE NECESSARY MODULES
import threading # Threads for increasing exe time 
from Voice_Assistant.Speak import Speak  # Custom module for text-to-speech
import asyncio  # For asynchronous programming
import shutil  # For file operations
import subprocess  # For running subprocesses
import time  # For time-related operations
import speech_recognition as sr  # For speech recognition
from Security.Cryptography import create_database_directory

#uncomment the following line to enable login and sign up functionality:
#from Configuration.LoginORsignIN import LoginOrSign  # Custom module for login or sign-in functionality
from EmailCreation.EmailAbout import ReadMsg  # Custom module for writing email messages with user's voice
from EmailCreation.EmailCheck import check  # Custom module for email checking before sending (confirmation)
from EmailCreation.EmailName import ReadName  # Custom module for writing email receiver's name with user's voice
from EmailCreation.EmailWhat import Subject  # Custom module for writing email subject with user's voice
from EmailCreation.EmailWho import AddNew_or_ChooseFromStorage, storage, storageCheck, whoIStheR  # Custom modules for managing email recipients and writing an email with user's voice
from EmailService.CodeGeneration import shuffleTxtEntry  # Custom module for shuffling text entries
from EmailService.EmailAccessability import Check_Email_Accessability  # Custom module for checking email accessibility
from EmailService.EmailObserver import get_emails, listen_for_id, view_email_content  # Custom modules for email observation and interaction
from EmailService.EmailSender import send_email  # Custom module for sending emails
from EmailService.EmailsStorage import get_name_email  # Custom module for storing email addresses
#from Voice_Assistant.Audio_Processor import IsSpeech, delete_recording, get_random_joke, save_audio_as_wav  # Custom modules for audio processing
from Voice_Assistant.Audio_Processor import get_random_joke  # Custom function for randomly picking jokes 
from Voice_Assistant.Read_Email_Voice_Inputs import POST  # Custom module for reading email voice inputs for display
from Voice_Assistant.Sleep_Mode import SleepMode  # Custom module for sleep mode functionality
from Web_BrowsingService.OpenWeb import Website_openPage_Handler, web_Search, webNameHandler  # Custom modules for web browsing functionality
from Web_BrowsingService.WebBrowsing import Website_Browsing_openPage_Handler  # Custom modules for browsing web pages

# Name of the software to be called as a way to activate the system or include to execute any command. This is how it's spoken.
software_Name = ['Taylor', 'Tyler']

# This function is for displaying a GUI interface (email template) and walking the user through the process of sending an email.
async def Generate_Email():
    # Open the email voice input script (email template) in a subprocess
    subprocess.Popen(["python", "Voice_Assistant/Read_Email_Voice_Inputs.py"])
    generate_email = []
    # Check if there are any stored email addresses
    check_Storage = storageCheck()
    if (check_Storage == None):
        # If no stored email addresses, prompt the user to input the email address
        Speak("Brilliant, What is the email?", -1, 1.0)
        email_address = whoIStheR()
    else:  
        # If there are stored email addresses, ask the user if they want to add a new one or choose from storage
        Speak("Would you like to add new or pick from storage?", -1, 1.0)
        Add_or_Storage = AddNew_or_ChooseFromStorage()
        if(Add_or_Storage == "add"):
           # If the user chooses to add a new email, prompt them to input the email address
           Speak("Brilliant, you have chosen the add new record service. To who?", -1, 1.0)
           email_address = whoIStheR()
        elif(Add_or_Storage == "storage"):
            # If the user chooses to pick from storage, retrieve the email address from storage
            Speak("Brilliant, you picked to choose from storage", -1, 1.0)
            email_address = storage()
            if email_address == None:
                # If there are no email addresses stored, prompt the user to add emails
                Speak("Add emails to store them", -1, 1.0)
                email_address = whoIStheR()
        else:
            # If no valid input is received, default to adding a new email address and prompt the user to input it
            Speak("The Default path is Adding new email. To who?", -1, 1.0)
            email_address = whoIStheR()
    # Post the email address to the json file to print in email template
    time.sleep(1)
    POST("Database/Content.json", "Email", "post", email_address)
    print("Email:\n", email_address)
    POST("Database/Content.json", "system", "post", " ")
    time.sleep(2)
    # Prompt the user to input the email subject
    Speak("What is the Subject?", -1, 1.0)
    email_subject = Subject()
    time.sleep(1)
    # Post the email subject to the json file to print in email template
    POST("Database/Content.json", "Subject", "post", email_subject)
    print("Subject:\n",email_subject)
    POST("Database/Content.json", "system", "post", " ")
    time.sleep(1)
    # Prompt the user to input the email message
    Speak("What is your message?", -1, 1.0)
    email_message = ReadMsg()
    time.sleep(1)
    # Post the email message to the json file to print in email template
    POST("Database/Content.json", "message", "post", email_message)
    POST("Database/Content.json", "system", "post", " ")
    print("Message:\n",email_message)
    time.sleep(1)
    # Prompt the user to input the recipient's name
    Speak("What is his, her, or its name?", -1, 1.0)
    Speak("Say space to add space", -1, 1.0)
    email_name = ReadName()
    time.sleep(1)
    # Post the recipient's name to the json file to print in email template
    POST("Database/Content.json", "Name", "post", email_name)
    print("Name:\n",email_name)
    time.sleep(1)
    # Store the generated email information in a list and return it
    generate_email = [email_subject, email_message, email_address, email_name]
    return generate_email

# The following function is for processing audio and checking the speech inside the audio.
def listen_for_service():
    with sr.Microphone() as source:
        try:      
            # Listen to audio input
            audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=3) 
            # Save audio as WAV file
            recognized_text = recognizer.recognize_google(audio_data)
            return recognized_text
        except sr.UnknownValueError:
            return
        except sr.WaitTimeoutError:
            return

                
# This function listens for keywords and performs corresponding actions based on recognized speech.
async def listen_for_keywords():
    
    # Get recognized text from audio input
    recognized_text = listen_for_service()
   
    # Check if recognized text is None or False, if so, continue listening
    if (recognized_text is None) or (recognized_text is False):
        await listen_for_keywords()
    
    # Check if software name is mentioned in recognized text
    elif(software_Name[0] in recognized_text) or (software_Name[1] in recognized_text):
        try:
            # Delete temporary audio recordings
            #delete_recording("Database/bin/resampled_audio_file1.wav", "Database/bin/processed_audio.wav", "Database/bin/user_input.wav", "Database/bin/vad_combined_audio.wav", "Database/bin/IsTaylor.wav")
            
            ###########################################
            ## Respond to specific recognized phrases ##
            ###########################################
            if (software_Name[0] or software_Name[1] in recognized_text) and ("how are you" in recognized_text):
                Speak("I am good. how about you?", -1, 1.0)
                await listen_for_keywords()
            
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("tell me" in recognized_text) or ("tell me another" in recognized_text):
                joke = get_random_joke()
                Speak(f"Hear this, {joke}", -1, 1.0)
                await listen_for_keywords()
                
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("quit" in recognized_text):
                Speak("quitting..", -1, 1.0)
                SleepMode()
                Speak("taylor is on..", -1, 1.0)
                await listen_for_keywords()

            ###########################################
            ## Email Services: Send email ##
            ###########################################
            elif(software_Name[0] or software_Name[1] in recognized_text) and ("send an email" in recognized_text) or ("send email" in recognized_text) or ("email service" in recognized_text):
                status = Check_Email_Accessability()
                if(status == False):
                    Speak("Email Configuration Failed", -1, 1.0)
                    quit()
                    
                generate_email = await Generate_Email()
                Speak("Would you like to send?", -1, 1.0)
                status = check()
                if status == True:
                    send_email(generate_email[0], generate_email[1], generate_email[2], generate_email[3], 'user email')
                    Speak("Email has been sent with success", -1, 1.0)
                    store_email = await get_name_email(generate_email[3], generate_email[2])
                    Speak(f"Also, {store_email} with success", -1, 1.0)
                else:
                    print("\nSomething went wrong\n")
                    Speak("Something went wrong", -1, 1.0)
                    await listen_for_keywords()
                await listen_for_keywords()

            ###########################################
            ## Email Services: Observe emails ##
            ###########################################
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("observe" in recognized_text) or ("new emails" in recognized_text) or ("check email" in recognized_text):
                status = Check_Email_Accessability()
                emails = await get_emails()
                if emails:
                    for i, (id, sender, subject, _) in enumerate(emails):
                        print(f"{i}: From {sender}, Subject: {subject}")
                    selected_email_id = listen_for_id(emails)
                    if selected_email_id:
                        await view_email_content(selected_email_id, emails)
                    else:
                        print("No email selected or understood.")
                else:
                    print("No new emails.")
                await listen_for_keywords()

            ###########################################
            ## Website Handler: Open website ##
            ###########################################
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("open" in recognized_text) and ("website" in recognized_text):
                url = await webNameHandler(recognized_text)
                url = await web_Search(url)
                await Website_openPage_Handler(url)
                await listen_for_keywords()

            ###########################################
            ## Website Browsing (Google): ##
            ###########################################
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("search" in recognized_text) and ("engine" in recognized_text):
                Speak("opening google search engine. Just to give you a heads up, if you want to exit say exit service", -1, 1.0)
                url = "https://www.google.com"
                await Website_Browsing_openPage_Handler(url)
                await listen_for_keywords()

            ###########################################
            ## Clear cached data ##
            ###########################################
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("clear cache" in recognized_text):
                pass

            ###########################################
            ## Log out ##
            ###########################################
            elif (software_Name[0] or software_Name[1] in recognized_text) and ("log me out" in recognized_text):
                try:
                    shutil.rmtree('Database')
                    Speak("You have successfully logged out", -1, 1.0)
                except OSError as e:
                    Speak(f"Error: {e.strerror}", -1, 1.0)
                quit() 

            ###########################################
            ## Feedback for unrecognized commands ##
            ###########################################
            elif (software_Name[0] or software_Name[1] in recognized_text) and not ("send an email" in recognized_text) or ("send email" in recognized_text) or ("email service" in recognized_text) or ("observe" in recognized_text) or ("new emails" in recognized_text) or ("check email" in recognized_text) or ("open" in recognized_text and "website" in recognized_text) or ("search" in recognized_text and "engine" in recognized_text):
                Speak("invalid command, please refer to the documentation", -1, 1.0)
                await listen_for_keywords()

            elif (recognized_text is None) or (recognized_text is False):
                Speak("invalid, None Type detected", -1, 1.0)
                await listen_for_keywords()

            else:
                await listen_for_keywords()

        except sr.UnknownValueError:
            await listen_for_keywords()
        except sr.RequestError as e:
            await listen_for_keywords()
    else:
        await listen_for_keywords()

# Check if the script is being run directly
if __name__ == "__main__":
    # Speak a message indicating that the application is opening
    Speak("Opening application...", -1, 1.0)
    """""
    Disaplying login and sign up function for smooth demostration as its functionality has been covered in the video 
    if the marker wants to see the result of the login or sign up, then i should uncomment the following lines:
    """""
    # Check if login or sign-up is successful
    #valid = LoginOrSign()
    # If login or sign-up fails, speak a failure message and quit
    #if not valid[0]:
       # Speak("Login or Sign up Failed", -1, 1.0)
        #quit()
    create_database_directory()
    # Get a random greeting message
    greetings = shuffleTxtEntry()
    # Speak the greeting
    Speak(greetings, -1, 1.0)
    # Initialize the speech recognizer
    recognizer = sr.Recognizer()
    # Get the event loop
    loop = asyncio.get_event_loop()
    # Run the function to listen for keywords
    loop.run_until_complete(listen_for_keywords())

