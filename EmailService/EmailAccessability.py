from Libraries import tk, json, messagebox
from Voice_Assistant.Speak import Speak
from Module import Check_Email_Status, send_email, delete_all_emails
from Configuration.Config import SetUpApp
def Check_Email_Accessability():
 Check_Email = Check_Email_Status() 
 if(Check_Email == False):
     Speak("The System cannot access your email. Here you go", -1, 1.0)
    
     root = tk.Tk()
     app = SetUpApp(root, "Set up Email", "lightblue", "grey", "Email")
     root.mainloop()
     try:
         with open("Database/Data.json", "r") as file:
            dataCheck = json.load(file)
     except (FileNotFoundError, json.JSONDecodeError):
         pass  # If file doesn't exist or is empty, continue with an empty list
     x = send_email("Success", "The email has been set up for you! \n Enjoy!", dataCheck["Login"]["L_email"], "User")
     
     #0 is returning a flase.  
     if  x == 0:
            messagebox.showerror("Error", "The Given email or and password is incorrect")
            #data = {"Login": {"L_email": "", "L_password": ""}}
            with open("Database/Data.json", 'r') as file:
             data = json.load(file)
             data["Login"]["L_email"] = ""
             data["Login"]["E_APIKEY"] = ""
              # Write the updated data back to the JSON file
            with open("Database/Data.json", 'w') as file:
             json.dump(data, file, indent=4)
            return False
     else:
            messagebox.showinfo("Success", "Email Service configured with success")
            return True
 else:
     return True