import os
import sys
from tkinter import messagebox
import unittest
from unittest.mock import mock_open, patch, MagicMock, create_autospec
import speech_recognition as sr
import json
# Adjusting the Python path to include necessary directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)

# Importing functions from the modules
from EmailService.EmailStatus import (
   Check_Email_Status
)
class TestCheckEmailStatusFunction(unittest.TestCase):

    def test_check_email_status(self):
        # Test case 1: Valid data in the file
        with open("Database/Data.json", "w") as test_file:
            json.dump({"Login": {"L_email": "test@example.com", "E_APIKEY": "test_api_key"}}, test_file)

        result = Check_Email_Status()
        print("Test case 1 result:", result)
        self.assertTrue(result)

        # Test case 2: Missing L_email in the file
        with open("Database/Data.json", "w") as test_file:
            json.dump({"Login": {"L_email": "", "E_APIKEY": "test_api_key"}}, test_file)

        result = Check_Email_Status()
        print("Test case 2 result:", result)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()