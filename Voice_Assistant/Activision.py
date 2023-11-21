from Libraries import json, tk
from Voice_Assistant.Speak import Speak
from Security.LoginORsignIN import LoginOrSign

def system_Info_On():
    try:
        with open("System.json", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def system_check():
     data = system_Info_On()
     data["System"]["Active"] = True
     data["System"]["NewUser"] = False
     data["System"]["Time_Bi_Login"] = data["System"]["Time_Bi_Login"] + 1
     with open("System.json", 'w') as file:
        json.dump(data, file, indent=4)
     Speak("System activated.", -1, 1.0)
        

    