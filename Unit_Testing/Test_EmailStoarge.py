import os
import sys
import unittest
# Adjusting the Python path to include necessary directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)

# Importing functions from the modules
from EmailService.EmailsStorage import (
   get_name_email
)
from Voice_Assistant.Read_Email_Voice_Inputs import POST

class TestGetNameEmailFunction(unittest.TestCase):

    def setUp(self):
        # Create a temporary test file
        self.test_file_path = "Database/Test_Cache.json"

    def tearDown(self):
        # Remove the temporary test file after the test
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_get_name_email(self):
        # Test case 1: Add a new record
        name = "John Doe"
        email = "john.doe@example.com"
        status = get_name_email(name, email)
        self.assertEqual(status, "record added")

        # Test case 2: Try to add a record with the same email (expect "ZERO" status)
        name = "Jane Doe"
        status = get_name_email(name, email)
        self.assertEqual(status, "ZERO")

        # Test case 3: Try to add a record with invalid email (expect "record added" status)
        name = "Invalid Email"
        invalid_email = "invalid_email"
        status = get_name_email(name, invalid_email)
        self.assertEqual(status, "record added")

        # Test case 4: Try to read from the file (expect "ZERO" status as email already exists)
        name = "Another Name"
        status = get_name_email(name, email)
        self.assertEqual(status, "ZERO")

if __name__ == '__main__':
    unittest.main()