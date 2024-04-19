import asyncio
import os
import shutil
import json
import subprocess
import time
import speech_recognition as sr
from Voice_Assistant.Speak import Speak
from Configuration.LoginORsignIN import LoginOrSign
from EmailCreation.EmailAbout import ReadMsg
from EmailCreation.EmailCheck import check
from EmailCreation.EmailName import ReadName
from EmailCreation.EmailWhat import Subject
from EmailCreation.EmailWho import AddNew_or_ChooseFromStorage, storage, storageCheck, whoIStheR
from EmailService.CodeGeneration import shuffleTxtEntry
from EmailService.EmailAccessability import Check_Email_Accessability
from EmailService.EmailObserver import get_emails, listen_for_id, view_email_content
from EmailService.EmailSender import send_email
from EmailService.EmailsStorage import get_name_email
from Voice_Assistant.Audio_Processor import IsSpeech, delete_recording, get_random_joke, save_audio_as_wav
from Voice_Assistant.Read_Email_Voice_Inputs import POST
from Voice_Assistant.Sleep_Mode import SleepMode
from Web_BrowsingService.OpenWeb import Website_openPage_Handler, web_Search, webNameHandler
from Web_BrowsingService.WebBrowsing import Website_Browsing_openPage_Handler, listen_for_Taylor

async def DisableSys():
    try:
        with open("System.json", "r") as file:
            data = json.load(file)
            data["System"]["Active"] = False
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    with open("System.json", 'w') as file:
        json.dump(data, file, indent=4)
        
software_Name = ['Taylor', 'Tyler']

async def Generate_Email():
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

async def listen_for_service():
    with sr.Microphone() as source:
        try:      
            audio_data = recognizer.listen(source) 
            save_audio_as_wav(audio_data, "Database/bin/user_input.wav")
            recognized_text =  IsSpeech("Database/bin/user_input.wav")
            if(recognized_text == False):
                return
            elif(recognized_text == 500):
                return
            else:
                return recognized_text
             
        except sr.UnknownValueError:
               return
                

async def listen_for_keywords():
    recognized_text = await listen_for_service()
    if (recognized_text is None) or (recognized_text is False):
        Speak("sorry, could not understand what you said", -1, 1.0)
        await listen_for_keywords()
    try:
        delete_recording("Database/bin/resampled_audio_file1.wav", "Database/bin/processed_audio.wav", "Database/bin/user_input.wav", "Database/bin/vad_combined_audio.wav", "Database/bin/IsTaylor.wav")
        if (software_Name[0] or software_Name[1] in recognized_text) and ("how are you" in recognized_text):
            Speak("I am good. how about you?", -1, 1.0)
            await listen_for_keywords()
        
        elif (software_Name[0] or software_Name[1] in recognized_text) and ("tell me" in recognized_text) or ("tell me another" in recognized_text):
            joke = get_random_joke()
            Speak(f"Hear this, {joke}", -1, 1.0)
            await listen_for_keywords()
            
        elif (software_Name[0] or software_Name[1] in recognized_text)and("quit" in recognized_text):
            Speak("quitting..", -1, 1.0)
            SleepMode()
            Speak("taylor is on..", -1, 1.0)
            await listen_for_keywords()

            
        ###########################################
        ## Email Services: Send email ##
        ###########################################
        elif(software_Name[0] or software_Name[1] in recognized_text)and("send an email" in recognized_text) or ("send email" in recognized_text) or ("email service" in recognized_text):
                status = Check_Email_Accessability()
                if(status == False):
                   Speak("Email Configuration Failed", -1, 1.0)
                   DisableSys()
                   subprocess.Popen(["python", "System_Activision.py"])
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
        ## Email Services: observe emails ##
        ###########################################   
        elif (software_Name[0] or software_Name[1] in recognized_text)and("observe" in recognized_text) or ("new emails" in recognized_text) or ("check email" in recognized_text):
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
        ## Wbsite hanlder: ##
        ###########################################
        elif (software_Name[0] or software_Name[1] in recognized_text)and("open" in recognized_text) and ("website" in recognized_text):
            url = await webNameHandler(recognized_text)
            url = await web_Search(url)
            await Website_openPage_Handler(url)
            await listen_for_keywords()
            
        ###########################################
        ## Wbsite Browsing (Google): ##
        ###########################################
        elif (software_Name[0] or software_Name[1] in recognized_text)and("search" in recognized_text) and ("engine" in recognized_text):
            Speak("openning google search engine. Just to give you a haeds up, if you want to exit say exit service", -1, 1.0)
            url = "https://www.google.com"
            await Website_Browsing_openPage_Handler(url)
            #asyncio.run(Website_Browsing_openPage_Handler(url))
            await listen_for_keywords()

        ###########################################
        ## Clear data stored in json file ##
        ###########################################   
        elif (software_Name[0] or software_Name[1] in recognized_text)and("clear cache" in recognized_text):
            pass
        ###########################################
        ## Log out ##
        ########################################### 
        elif (software_Name[0] or software_Name[1] in recognized_text)and("log me out" in recognized_text):
            try:
                shutil.rmtree('Database')
                Speak("You have successfully logged out", -1, 1.0)
            except OSError as e:
                Speak(f"Error: {e.strerror}", -1, 1.0)
            quit() 
        ###########################################
        ## Feedback from the system if the command is not recognised ##
        ########################################### 
        elif (software_Name[0] or software_Name[1] in recognized_text) and not ("send an email" in recognized_text) or ("send email" in recognized_text) or ("email service" in recognized_text) or ("observe" in recognized_text) or ("new emails" in recognized_text) or ("check email" in recognized_text) or ("open" in recognized_text and "website" in recognized_text) or ("search" in recognized_text and "engine" in recognized_text):
            Speak("invalid command, please refer to the documentation", -1, 1.0)
            await listen_for_keywords()
            
        elif (recognized_text is None):
            Speak("invalid, None Type detected", -1, 1.0)
            await listen_for_keywords()
            
        else:
            await listen_for_keywords()

    except sr.UnknownValueError:
        await listen_for_keywords()
    except sr.RequestError as e:
        await listen_for_keywords()

if __name__ == "__main__":
    Speak("Openning application...", -1, 1.0)
    valid = LoginOrSign()
    if not valid[0]:
        Speak("Login or Sign up Failed", -1, 1.0)
        quit()
    greetings = shuffleTxtEntry()
    Speak(greetings, -1, 1.0)
    recognizer = sr.Recognizer()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(listen_for_keywords())
    #asyncio.run(listen_for_keywords()) 
