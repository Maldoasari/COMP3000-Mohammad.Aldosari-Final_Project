import hashlib
import os
from cryptography.fernet import Fernet
import json


def encrypt_json_file(file_path, key):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Convert JSON data to string and then to bytes
    data_as_bytes = json.dumps(data).encode('utf-8')

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data_as_bytes)

    with open(file_path, 'wb') as file:
        file.write(encrypted_data)

def decrypt_json_file(file_path, key, write_back=True):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()

    cipher = Fernet(key)
    decrypted_data_as_bytes = cipher.decrypt(encrypted_data)

    # Convert bytes back to string and then to JSON
    decrypted_data = json.loads(decrypted_data_as_bytes.decode('utf-8'))

    if write_back:
        with open(file_path, 'w') as file:
            json.dump(decrypted_data, file)
    else:
        return decrypted_data


#key = Fernet.generate_key()
#print(key)
with open("System.json", 'rb') as file:
    data = json.load(file)
    Ckey = data['System']['ENCkey']


#Encrypt the JSON file
#encrypt_json_file('Cookies.json', key=Ckey)

# Decrypt the JSON file
#decrypt_json_file('Cookies.json', key=Ckey)
