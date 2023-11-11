from Requirments.Install_Packages import install_packages
## try and find wheather all libraries have been download or not
try:
 from Libraries import *  
except ModuleNotFoundError as e:
    ## if the library is not found install it
    install_packages()
from Libraries import *
from Voice_Assistant.Speak import Speak
from Voice_Assistant.Activision import *

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
