import hashlib
import os
from cryptography.fernet import Fernet
import json


def encrypt_text(plaintext):
    with open("System.json", 'rb') as file:
        data = json.load(file)
        Ckey = data['System']['ENCkey']

    plaintext_as_bytes = json.dumps(plaintext).encode('utf-8')

    cipher = Fernet(Ckey.encode('utf-8'))
    encrypted_data = cipher.encrypt(plaintext_as_bytes)

    return encrypted_data

def decrypt_text(encrypted_data_str):
    try:
        with open("System.json", 'rb') as file:
            data = json.load(file)
            Ckey = data['System']['ENCkey']

        cipher = Fernet(Ckey.encode('utf-8'))

        # Remove the "b" prefix if it exists
        if encrypted_data_str.startswith("b'") and encrypted_data_str.endswith("'"):
            encrypted_data_str = encrypted_data_str[2:-1]

        # Convert the string representation to bytes
        encrypted_data_inner = encrypted_data_str.encode('utf-8')

        decrypted_data_as_bytes = cipher.decrypt(encrypted_data_inner)
        decrypted_data = json.loads(decrypted_data_as_bytes.decode('utf-8'))

        return decrypted_data
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Error while decrypting: {e}")
        return None
    
#v = decrypt_text()
#print(v)

#key = Fernet.generate_key()
#print(key)



#Encrypt the JSON file
#encrypt_json_file('Cookies.json', key=Ckey)

# Decrypt the JSON file
#decrypt_json_file('Cookies.json', key=Ckey)
# Hashing functions
def hash_password(password):
    salt = os.urandom(32)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + pwdhash.hex()

def verify_password(stored_password, provided_password):
    salt = bytes.fromhex(stored_password[:64])
    stored_password = bytes.fromhex(stored_password[64:])
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt, 100000)
    return pwdhash == stored_password
def create_database_directory():
    # Get the current working directory
    current_directory = os.getcwd()
    database_directory_name = 'Database'
    database_directory_path = os.path.join(current_directory, database_directory_name)
    if os.path.exists(database_directory_path):
        print(f"Directory '{database_directory_path}' already exists. Skipping creation.")
        return

    os.makedirs(database_directory_path)
    
    bin_directory = os.path.join(database_directory_path, 'bin')
    os.makedirs(bin_directory)

    data_file_path = os.path.join(database_directory_path, 'Data.json')
    with open(data_file_path, 'w') as data_file:
        json.dump(
            {
                "Login": {
                    "L_email": "",
                    "E_APIKEY": ""
                },
                "User": {
                    "S_Active": False,  
                    "NewUser": True
                },
                "User_email": "",
                "Time_Bi_Login": 0
            }
        , data_file, indent=2)  # Indent for better readability
    
    content_file_path = os.path.join(database_directory_path, 'Content.json')
    with open(content_file_path, 'w') as content_file:
        json.dump(
            {
                "Email": "",
                "Subject": "",
                "massage": "",
                "Name": "",
                "message": "",
                "status": "",
                "system": " "
            }
        , content_file, indent=2)  # Indent for better readability
    
    cookies_file_path = os.path.join(database_directory_path, 'cookies.json')
    with open(cookies_file_path, 'w') as cookies_file:
        json.dump([{"name": "defult", "email": "defult"}], cookies_file, indent=2) 
        
    output_file_path = os.path.join(database_directory_path, 'Output.json')
    with open(output_file_path, 'w') as output_file:
        json.dump({"Email": "", "Subject": "", "Message": "", "System": ""}, output_file, indent=2)

    print(f"Database directory '{database_directory_path}' created successfully.")