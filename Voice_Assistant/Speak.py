import pyttsx3
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