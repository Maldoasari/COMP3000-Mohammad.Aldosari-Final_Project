from Requirments.Install_Packages import install_packages
## try and find wheather all libraries have been download or not
try:
 from Voice_Assistant.Libraries import *  
except ModuleNotFoundError as e:
    ## if the library is not found install it
    install_packages()
from Voice_Assistant.Libraries import *
from Voice_Assistant.Activision import *
# Initialize speech recognition
recognizer = sr.Recognizer()

Speak("To activate the system say activate.", -1, 1.0)

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

# Main loop to continuously listen for activation
while True:
    activate_system()
