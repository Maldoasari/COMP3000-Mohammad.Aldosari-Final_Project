
#Modules import here:
from EmailService.CodeGeneration import shuffleTxtEntry
from EmailService.EmailSender import send_email, delete_all_emails
from EmailService.EmailStatus import Check_Email_Status
from EmailService.EmailAccessability import Check_Email_Accessability
from EmailCreation.EmailWho import whoIStheR, AddNew_or_ChooseFromStorage, storage
from EmailCreation.EmailWhat import Subject
from Voice_Assistant.Audio_Processor import process_wav_file, delete_recording, save_audio_as_wav
from Voice_Assistant.Sleep_Mode import SleepMode
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

    