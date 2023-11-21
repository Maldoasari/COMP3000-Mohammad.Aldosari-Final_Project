from Libraries import json, tk
from Voice_Assistant.Speak import Speak

def system_Info_On():
    try:
        with open("Database/Data.json", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def system_check():
     data = system_Info_On()
     data["User"]["S_Active"] = True
     data["User"]["NewUser"] = False
     data["User"]["Time_Bi_Login"] = data["User"]["Time_Bi_Login"] + 1
     with open("System.json", 'w') as file:
        json.dump(data, file, indent=4)
     Speak("System activated.", -1, 1.0)
        

    