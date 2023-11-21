"""""
from sympy import false, true
from Requirments.Install_Packages import install_packages
## try and find wheather all libraries have been download or not
try:
 from Libraries import *  
except ModuleNotFoundError as e:
    ## if the library is not found install it
    install_packages()
"""""
from sympy import false, true
from Libraries import *
from Voice_Assistant.Speak import Speak
from Voice_Assistant.Activision import *
import os
import json

# Initialize speech recognition
recognizer = sr.Recognizer()

Speak("To activate the system, say activate.", -1, 1.0)

throttle_interval = 10

# Function to recognize speech and execute commands
def activate_system():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        if ("activate" in command) or ("activate" in command):
            system_check()
            subprocess.Popen(["python", "Main.py"])
            quit()
        else:
            print("Activation command not recognized.")
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")

def create_database_directory():
    # Get the current working directory
    current_directory = os.getcwd()

    # Specify the new directory name
    database_directory_name = 'Database'

    # Create the main database directory in the current working directory
    database_directory_path = os.path.join(current_directory, database_directory_name)

    # Check if the directory already exists
    if os.path.exists(database_directory_path):
        print(f"Directory '{database_directory_path}' already exists. Skipping creation.")
        return

    os.makedirs(database_directory_path)

    # Create the 'bin' directory inside the main database directory
    bin_directory = os.path.join(database_directory_path, 'bin')
    os.makedirs(bin_directory)

    # Create the 'Data.json' file inside the main database directory
    data_file_path = os.path.join(database_directory_path, 'Data.json')
    with open(data_file_path, 'w') as data_file:
        json.dump({
    "Login": {
        "L_email": "",
        "E_APIKEY": ""
    },
    "User": {
        "S_Active": false,
        "NewUser": true,
        "Time_Bi_Login": 1,
        "attempts": 0,
        "time": " "
    }}, data_file)  

    
    content_file_path = os.path.join(database_directory_path, 'Content.json')
    with open(content_file_path, 'w') as content_file:
        json.dump({}, content_file)  


    cookies_file_path = os.path.join(database_directory_path, 'cookies.json')
    with open(cookies_file_path, 'w') as cookies_file:
        json.dump({}, cookies_file)  

    print(f"Database directory '{database_directory_path}' created successfully.")

# Main loop to continuously listen for activation
if __name__ == "__main__":
    last_activation_time = 0  # Initialize to a time in the past
    while True:
        current_time = time.time()
        if current_time - last_activation_time >= throttle_interval:
            activate_system()
            last_activation_time = current_time
        time.sleep(1)  # Sleep for 1 second
        print(throttle_interval)
        print(current_time)
        print(last_activation_time)
        print(current_time - last_activation_time)
