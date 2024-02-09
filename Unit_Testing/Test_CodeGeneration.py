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
from EmailService.CodeGeneration import (
   generate_random_5_digit_number, shuffleTxtEntry
)
from Voice_Assistant.Read_Email_Voice_Inputs import POST

class TestAuthCodeGenerator(unittest.TestCase):

    def test_generate_random_5_digit_number(self):
        # Test the length of the generated number
        random_number = generate_random_5_digit_number()
        self.assertEqual(len(random_number), 5)

        # Test that the generated number is a string composed of digits
        self.assertTrue(random_number.isdigit())

    def test_shuffleTxtEntry(self):
        # Test that the output is one of the predefined strings after shuffling
        shuffled_text = shuffleTxtEntry()
        predefined_texts = ["Taylor. is listening..", "Taylor. is ON", "Taylor. is waiting.", "Taylor loves your voice. speak up!..."]
        self.assertIn(shuffled_text, predefined_texts)

if __name__ == '__main__':
    unittest.main()