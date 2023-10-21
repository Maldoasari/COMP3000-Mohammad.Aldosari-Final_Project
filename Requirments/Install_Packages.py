import subprocess
import time

requirements_file = 'Requirments/requirements.txt'

## This Function will be responsible in installing the requiremnts needed for the project
def install_packages():
    for _ in range(10):
        print("Installing libraries...", end="\r")
        time.sleep(1)
    print("\n")  
    # Open and read the requirements file
    with open(requirements_file, 'r') as f:
        libraries = f.readlines()

    # Attempt to install each library individually
    for lib in libraries:
        lib = lib.strip()  # Remove any whitespace or newline characters
        if not lib or lib.startswith("#"):  # Skip empty lines or comments
            continue
        try:
            subprocess.check_call(['pip', 'install', lib])
            print(f"'{lib}' installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to install '{lib}'. {e}")




