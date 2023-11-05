#from Libraries import json
import json 
def GET_POST_Email(status, email):
    with open("Email.json", 'r') as file:
        data = json.load(file)
    if status == "post":
      data["Email"] = email  
      with open("Email.json", 'w') as file:
         json.dump(data, file, indent=4)
    elif status == "get":
        return data["Email"]  
    else:
        return 501
    
def GET_POST_Subject(status, subject):
    with open("Email.json", 'r') as file:
        data = json.load(file)
    if status == "post":
      data["Subject"] = subject  
      with open("Email.json", 'w') as file:
         json.dump(data, file, indent=4)
    elif status == "get":
        return data["Subject"]  
    else:
        return 501
    
def GET_POST_Message(status, msg):
    with open("Email.json", 'r') as file:
        data = json.load(file)
    if status == "post":
      data["message"] = msg  
      with open("Email.json", 'w') as file:
         json.dump(data, file, indent=4)
    elif status == "get":
        return data["message"]  
    else:
        return 501
    
def GET_POST_Name(status, name):
    with open("Email.json", 'r') as file:
        data = json.load(file)
    if status == "post":
      data["Name"] = name  
      with open("Email.json", 'w') as file:
         json.dump(data, file, indent=4)
    elif status == "get":
        return data["Name"]  
    else:
        return 501


