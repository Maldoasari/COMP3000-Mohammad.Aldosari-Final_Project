import json

def get_name_email(name, email):
    data = []
    status = ""
    # Try reading the existing data from the file
    try:
        with open("Database/Cache.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # If file doesn't exist or is empty, continue with an empty list

    email_exists = False
    for d in data:
        if d["email"] == email:
            email_exists = True
            print("this email already exist")
            status = status + "ZERO"
            break

    if not email_exists:
        # Append new data
        data.append({"name": name, "email": email})

        # Write the data back to the file
        with open("Database/Cache.json", "w") as file:
            json.dump(data, file, indent=4)
            print("email saved")
            status = status + "record added"
    return status

def ClearCookies():
    with open("Database/Cache.json", "w") as file:
        json.dump([{"name": "defult", "email": "defult"}], file, indent=4)
    print("All data in the storage have been deleted\n")


