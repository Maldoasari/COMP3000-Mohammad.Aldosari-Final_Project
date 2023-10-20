from Libraries import json
def Check_Email_Status():
    try:
      with open("Database/Data.json", "r") as file:
          data = json.load(file)
          if(len(data["Login"]["L_email"]) > 0) and (len(data["Login"]["E_APIKEY"]) > 0):
               return True
          else:
              return False
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    