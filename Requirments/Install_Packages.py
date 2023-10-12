import subprocess
import time

requirements_file = 'Requirments/requirements.txt'

## This Function will be responsible in installing the requiremnts needed for the project
def install_packages():
    for _ in range(10):
        print("Installing libraries...", end="\r")
        time.sleep(1)
    print("\n")  
    try:
        subprocess.check_call(['pip', 'install', '-r', requirements_file])
        print("Libraries installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to install libraries. {e}")
        return False




