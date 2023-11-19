import requests
import json

url = ""
content = ""
apikey = "5HVEIRO8zc8X6XF-b9Ys0kWXmrSUVjZ0RwGVbD9QsSY="
headers = {
    'Content-Type': 'application/json',
    'ApiKey': f'{apikey}' 
}

def Get_record_by_email(email):
    url = f'http://localhost:5108/api/Voices-Do-services/ByEmail/{email}'
    pass

def Post_record(data):
    
    pass

def Delete_record_by_email(email):
    pass

def Update_record_by_email(email):
    pass