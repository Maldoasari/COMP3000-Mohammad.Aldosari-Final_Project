from Libraries import json
from Security.Resttful_API import Get_record_by_email
def Check_Email_Status():
    with open("Database/Data.json", "r") as file:
          GetEmail = json.load(file)
          GetEmail = GetEmail["User_email"]
          
    data = Get_record_by_email(GetEmail)
    
    try:
          if (len(data["email_service_login_email"]) > 0) and (len(data["email_service_login_pass"]) > 0):
               return True, GetEmail
          else:
              return False, GetEmail
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    