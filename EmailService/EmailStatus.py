import os
from Libraries import json
import subprocess
CREDENTIALS_FILE = 'Database/credentials.json'
def Check_Email_Status():
    try:
        if os.path.exists(CREDENTIALS_FILE):
          return True
        else:
          print("Credentials not found. Please run the app and authenticate.")
          False
    except(FileNotFoundError, json.JSONDecodeError):
        pass
    


    
    