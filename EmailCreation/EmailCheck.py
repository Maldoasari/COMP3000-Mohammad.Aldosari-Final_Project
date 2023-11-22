from Libraries import time, sr, recognizer
def check():
    b = None
    print("Want to send it?")
    with sr.Microphone() as source:
      while True:
       audio = recognizer.listen(source)
       try:
         Capture = recognizer.recognize_google(audio).lower()
         if ("yes" in Capture) or ("confirm" in Capture):
          b = True
          break
         elif ("no" in Capture):
          b = False
          break
         else:
          continue
       except sr.UnknownValueError:
         print("Could not understand audio")
         continue
       except sr.RequestError as e:
         print("Could not request results; {0}".format(e))
         continue
    return b 