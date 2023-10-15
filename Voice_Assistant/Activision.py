import json
from Voice_Assistant.Libraries import *


def system_Info_On():
    try:
        with open("System.json", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def system_check():
     #if the user is new, Go throgh this function
     data = system_Info_On()
     if(data["System"]["NewUser"] == True):
         NewUser(data)
     else: 
      data["System"]["Active"] = True
      data["System"]["Time_Bi_Login"] = data["System"]["Time_Bi_Login"] + 1
      with open("System.json", 'w') as file:
        json.dump(data, file, indent=4)
      Speak("System activated.", -1, 1.0)
        
def NewUser(data):
    data["System"]["NewUser"] = False
    with open("System.json", 'w') as file:
        json.dump(data, file, indent=4)
    print("New User")
    system_check()
    