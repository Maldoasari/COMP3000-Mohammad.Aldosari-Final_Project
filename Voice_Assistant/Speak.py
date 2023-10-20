from Libraries import pyttsx3
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