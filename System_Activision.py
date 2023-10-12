import speech_recognition as sr
import subprocess
import pyttsx3
import json
# Initialize speech recognition
recognizer = sr.Recognizer()

# Initialize text-to-speech
engine = pyttsx3.init()
engine.say("Hello. to activate the system say activate.")
engine.runAndWait()

# Function to recognize speech and execute commands
def activate_system():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        if ("activate" in command) or ("activate" in command):
            engine.say("System activated.")
            engine.runAndWait()
            with open("Config.json", 'r') as file:
             data = json.load(file)
             data["System"]["Active"] = True
             data["System"]["Time_Bi_Login"] =+1
              # Write the updated data back to the JSON file
            with open("Config.json", 'w') as file:
             json.dump(data, file, indent=4)
             
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
