from Libraries import sr, time, recognizer
from Voice_Assistant.Speak import Speak

def checkName(nameofrec):
    cloneName = nameofrec
    name = ''  
    reciver_with_spaces = nameofrec.replace("space", " ")
    Speak("Say yes to confirm, or no to rewrite the name", 0, 1.0)

    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:  
         print("\nYes or No...")
         Capture = recognizer.recognize_google(audio).lower()
         if "yes" in Capture:
          capitalized_name = ' '.join(word.capitalize() for word in reciver_with_spaces.split())
          name = capitalized_name
          return name
         elif "no" in Capture:
          Speak("what is the name?", 0, 1.0)
          name = ReadName()
          return name
         else:
          print("\nSorry, Didn't catch it")
          name = checkName(cloneName)
          return name
        except sr.UnknownValueError:
            print("Could not understand audio")
            name = checkName(cloneName)
            return name 
        except sr.RequestError:
            print("API error")
            name = checkName(cloneName)
            return name
        return name 

def ReadName():
    name = ''
    print("What is the Name?")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    
    try:
        getname = recognizer.recognize_google(audio).lower()
        
        Speak(f"Do You Confirm That you have said:{getname}\n", 0, 1.0)
        print("Do You Confirm That you have said:\n", getname)
        name = checkName(getname)
        return name
    except sr.UnknownValueError:
        print("Could not understand audio")
        name = ReadName()
        return name
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        name = ReadName()
        return  name
    