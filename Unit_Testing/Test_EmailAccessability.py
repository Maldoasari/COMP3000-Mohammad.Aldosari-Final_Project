import os
import sys
from tkinter import messagebox
import unittest
from unittest.mock import mock_open, patch, MagicMock, create_autospec
# Adjusting the Python path to include necessary directories
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir('.')
cur_dir = os.getcwd()
dir2_path = os.path.join(parent_dir, fr"{cur_dir}")
sys.path.append(dir2_path)

# Importing functions from the modules
from EmailService.EmailAccessability import (
   Check_Email_Accessability, Store_Contacts
)
from Voice_Assistant.Read_Email_Voice_Inputs import POST

class TestEmailAccessibility(unittest.TestCase):

    @patch('EmailService.EmailAccessability.Check_Email_Status')
    @patch('EmailService.EmailAccessability.tk.Tk')
    @patch('Configuration.Config.SetUpApp')
    @patch('Module.send_email')
    @patch('EmailService.EmailAccessability.Store_Contacts')
    @patch('Libraries.messagebox')
    def test_email_failure(self, mock_messagebox, mock_store_contacts, mock_send_email, mock_setup_app, mock_tk, mock_check_email_status):
        
         # Set up mocks
        mock_check_email_status.return_value = False
        mock_send_email.return_value = 1  
        #Case test 1: Simulate email send success
        result = Check_Email_Accessability()
        self.assertTrue(result)
        messagebox.showinfo("Success", "Email Service configured with success")
        
          # Set up mocks
        mock_check_email_status.return_value = False
        mock_send_email.return_value = 0
        with patch('builtins.open', mock_open(read_data='{"Login": {"L_email": "test@example.com", "L_password": "password"}}')):
            result = Check_Email_Accessability()
        self.assertFalse(result)
        messagebox.showinfo("Fail", "")

    @patch('EmailService.EmailAccessability.imaplib.IMAP4_SSL')
    @patch('EmailService.EmailAccessability.email.message_from_bytes')
    @patch('EmailService.EmailAccessability.json.dump') 
       
    def test_Store_Contacts(self, mock_json_dump, mock_message_from_bytes, mock_imaplib):
         # Mocking IMAP server interaction
        mock_mail = MagicMock()
        mock_imaplib.return_value = mock_mail
        mock_mail.search.return_value = ('OK', [b'1 2 3'])
        mock_mail.fetch.return_value = ('OK', [(b'1', b'raw email data')])
        
         # Mocking email processing
        mock_email_message = MagicMock()
        mock_email_message.__getitem__.return_value = 'test@example.com'
        mock_message_from_bytes.return_value = mock_email_message
        
         # Mock file reading and writing
        mock_file = mock_open(read_data='{"Login": {"L_email": "", "E_APIKEY": ""}}')
        with patch('builtins.open', mock_file):
            Store_Contacts()
        print("Success")
        # Assert file writing
        mock_json_dump.assert_called_once()
           
    # Test when Check_Email_Status returns True initially
    @patch('EmailService.EmailAccessability.Check_Email_Status', return_value=True)
    @patch('Voice_Asistant.Speak.Speak')
    @patch('EmailService.EmailSender.send_email')
    def test_email_accessible(self, mock_send_email, mock_speak, mock_check_email_status):
        result = Check_Email_Accessability()
        self.assertTrue(result)
        mock_speak.assert_not_called()
        mock_send_email.assert_not_called()
        
if __name__ == '__main__':
    unittest.main()