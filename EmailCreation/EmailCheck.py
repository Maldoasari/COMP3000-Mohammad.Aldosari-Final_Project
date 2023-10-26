from Libraries import time, sr, recognizer

def check():
    boolg = False
    print("Want to send it?")
    try:
     with sr.Microphone() as source:
         audio = recognizer.listen(source)
    
     Capture = recognizer.recognize_google(audio).lower()

     if "yes" or "confirm" in Capture:
        boolg = True
        print(Capture)
        return boolg
     else:
        print(Capture)
        return boolg
    except sr.UnknownValueError:
        print("Could not understand audio")
        boolg = check()
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        boolg = check()
