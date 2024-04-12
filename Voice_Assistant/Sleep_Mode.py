import speech_recognition as sr

recognizer = sr.Recognizer()
def SleepMode():
     with sr.Microphone() as source2:
        while True:
         try:
            audio_data_Wait = recognizer.listen(source2, timeout=1800, phrase_time_limit=3)
            WakUPcommand = recognizer.recognize_google(audio_data_Wait).lower()
            if "taylor wake up" in WakUPcommand:
                break
         except sr.UnknownValueError:
               continue
         except sr.RequestError:
                print("API Error")
                break
            