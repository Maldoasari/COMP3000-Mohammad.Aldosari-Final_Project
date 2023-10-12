
#All Libraries must be imported here to be exttracted by the Main file
import speech_recognition as sr
import time
import subprocess
import pyttsx3
import json
#Modules import here:
from EmailService.CodeGeneration import shuffleTxtEntry

## Creating a talkitive system module
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)
volume = engine.getProperty('volume')
engine.setProperty('volume', volume + 0.25)

## Module speaks function 
def Speak(text, r, v): 
   #rate = engine.getProperty('rate') 
   engine.setProperty('rate', r) 
   #volume = engine.getProperty('volume')
   engine.setProperty('volume', v)
   engine.say(f'{text}')
   engine.runAndWait()


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

## Accessing config data
def Config_Json():
    try:
        with open("Config.json", "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # If file doesn't exist or is empty, continue with an empty list
    
    