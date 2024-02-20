import requests


apikey = "5HVEIRO8zc8X6XF-b9Ys0kWXmrSUVjZ0RwGVbD9QsSY="
headers = {
    'Content-Type': 'application/json',
    'ApiKey': f'{apikey}' 
}

def Get_record_by_email(email):
    url = f'http://localhost:5108/api/Voices-Do-services/ByEmail/{email}'
    try:
        #GET request to the specified URL
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    pass


def Post_record(data):
    url = 'http://localhost:5108/api/Voices-Do-services'
    try:
        #POST request with JSON data
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
"""""
new_record_data = {
    "email_login": "12Mohammad@gmail.com",
    "pincode_login": "string",
    "password_login": "string",
    "email_service_login_email": "string",
    "email_service_login_pass": "string",
    "netflix_username": "string",
    "netflix_pass": "string",
    "primeVideo_username": "string",
    "primeVideo_pass": "string",
    "spotify_Client_ID": "string",
    "spotify_Client_Secret": "string"
}

created_record = Post_record(new_record_data)
print(created_record)
"""

def Delete_record_by_email(email):
    url = f"http://localhost:5108/api/Voices-Do-services/ByEmail/{email}"
    try:
        #DELETE request
        response = requests.delete(url)
        if response.status_code == 200:
            print(f"Record with email {email} deleted successfully.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"An error occurred: {e}")
    pass
"""""
email_to_delete = "12Mohammad@gmail.com"
Delete_record_by_email(email_to_delete)
"""

def Update_record_by_email(email, The_Updated_Data):
    # Retrieve the existing record
    url = f'http://localhost:5108/api/Voices-Do-services/ByEmail/{email}'
    try:
        response = requests.get(url)
        existing_record = response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"An error occurred while retrieving the existing record: {e}")
        existing_record = None

    if existing_record:
        # Merge the existing record with the updated data
        merged_data = {**existing_record, **The_Updated_Data}

        # Update the record
        url = f'http://localhost:5108/api/Voices-Do-services/ByEmail/{email}'

        try:
            # Make a PATCH request
            response = requests.put(url, json=merged_data)
            if response.status_code == 200:
                try:
                # Try to parse the JSON data from the response
                 print("suceess")
                 return response.json()
                 
                except ValueError:
                 return None
            
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    else:
        print(f"No record found for email {email}")
        return None

"""""
update_data = {
    "pincode_login": "new_pincode",
    "password_login": "new_password",
    "email_service_login_email": "it works!",
    "email_service_login_pass": "yes it"
    
}

email_to_update = "Mohammad@gmail.com"
updated_record = Update_record_by_email(email_to_update, update_data)
"""