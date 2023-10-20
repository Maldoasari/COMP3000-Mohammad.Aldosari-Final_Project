#from Libraries import json
import json
def Check_Email_Status():
    try:
      with open("Database/Data.json", "r") as file:
          data = json.load(file)
          if(data["Login"]["L_email"] != " " ) and (data["Login"]["E_APIKEY"] != " "):
              data["Login"]["Status"] = True
              with open("Database/Data.json", 'w') as file:
               json.dump(data, file, indent=4)
               return True
          else:
              data["Login"]["Status"] = False
              with open("Database/Data.json", 'w') as file:
               json.dump(data, file, indent=4)
              return False
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    