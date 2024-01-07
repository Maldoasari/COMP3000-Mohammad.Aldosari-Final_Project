
#Modules import here:
from EmailService.CodeGeneration import shuffleTxtEntry
from EmailService.EmailSender import send_email, delete_all_emails
from EmailService.EmailStatus import Check_Email_Status
from EmailService.EmailAccessability import Check_Email_Accessability
from Web_BrowsingService.OpenWeb import webNameHandler, web_Search, Website_openPage_Handler
from EmailCreation.EmailWho import whoIStheR, AddNew_or_ChooseFromStorage, storage, storageCheck
from EmailCreation.EmailWhat import Subject
from EmailCreation.EmailAbout import ReadMsg
from EmailCreation.EmailCheck import check
from EmailCreation.EmailName import ReadName
from EmailService.EmailsStorage import get_name_email
from EmailService.EmailObserver import get_emails, Listen_for_id, view_email_content
from Voice_Assistant.Audio_Processor import process_wav_file, delete_recording, save_audio_as_wav
from Voice_Assistant.Sleep_Mode import SleepMode
from Voice_Assistant.Read_Email_Voice_Inputs import POST
from Configuration.LoginORsignIN import LoginOrSign
from EmailService.EmailSender import load_credentials
## For latter use in order to convert numbers as string to numbers as int
def word_to_number(word):
    mapping = {
        "zero": 0,
        "hero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
        "eleven": 11
    }
    return mapping.get(word, None)

    