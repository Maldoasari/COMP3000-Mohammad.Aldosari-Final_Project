import speech_recognition as sr

recognizer = sr.Recognizer()
def SleepMode():
      while True:
       with sr.Microphone() as source2:
            try:
                audio_data_Wait = recognizer.listen(source2, timeout=10)
                WakUPcommand = recognizer.recognize_google(audio_data_Wait).lower()
                if "taylor wake up" in WakUPcommand:
                    break
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue
            except sr.WaitTimeoutError:
                continue

            