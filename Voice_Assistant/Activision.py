from Voice_Assistant.Libraries import *
from Security.Biomatric import VoiceRecorderApp

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
    Speak("It seems that you are a new user. please record yourself for 5 sec. to enjoy the app with more security", -1, 1.0)
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
    data["System"]["NewUser"] = False
    with open("System.json", 'w') as file:
        json.dump(data, file, indent=4)
    Speak("Wonderfull. all set for you", -1, 1.0)
    system_check()
    