from Voice_Assistant.Read_Email_Voice_Inputs import POST
from Voice_Assistant.Speak import Speak
from Libraries import sr, time, re, recognizer


def edit_message(message):
    do_again = message

    message_chunks = [message[i:i+40] for i in range(0, len(message), 40)]
    x = []
    count = 0
    for index, line in enumerate(message_chunks, start=1):
        count = count + 1
        x.append(f"Line {index}: {line}")

    count = count / 2 - 2.5
    if(count < 0):
        count = 2
    print(x)
    POST("Database/Content.json", "system", "post", f"{x}")
    line_num = 0

    with sr.Microphone() as source:
        Speak("Say the line number to edit:", 0, 1.0)
        audio = recognizer.listen(source)
        try:
            capture = recognizer.recognize_google(audio).lower()
            for i in range(1, len(message_chunks)+1):
                if str(i) in capture:
                    Speak(f"The picked line is:{message_chunks[i - 1]}", 0, 1.0)
                    POST("Database/Content.json", "system", "post", f"{message_chunks[i - 1]}")
                    line_num = i - 1
                    break
                else:
                 Speak("index out of range", 0, 1.0)
                 print("index out of range")
                 return edit_message(do_again)
        except sr.UnknownValueError:
            Speak("Google Speech Recognition could not understand audio", 0, 1.0)
            print("Google Speech Recognition could not understand audio")
            return edit_message(do_again)
        except sr.RequestError as e:
            Speak(f"Could not request results from Google Speech Recognition service; {e}", 0, 1.0)
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return edit_message(do_again)

    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            Speak("Rewrite message to:", 0, 1.0)
            POST("Database/Content.json", "system", "post", "Rewrite message to:")
            capture = recognizer.recognize_google(audio).lower()
            message_chunks[line_num] = capture
            message = "\n".join(message_chunks)
       
        except sr.UnknownValueError:
            Speak("Google Speech Recognition could not understand audio", 0, 1.0)
            print("Google Speech Recognition could not understand audio")
            return edit_message(do_again)
        except sr.RequestError as e:
            Speak(f"Could not request results from Google Speech Recognition service; {e}", 0, 1.0)
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return edit_message(do_again)
    
    return message

#edit_message("the idea of being an gh hdyt utfuygu  ufuyf jhgjg iug  iug igui ")  
def checkmsg(message):
    msg  = '' 
    do_again = message
    Speak("Say yes to confirm or no to rewrite the message or edit to modify the message", 0, 1.0)
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
          print("Yes or No or edit...")
          Capture = recognizer.recognize_google(audio).lower()
    
          if "yes" in Capture:
           msg = message
           return msg
          elif "no" in Capture:
            Speak("Okey! what is your message", 0, 1.0)
            POST("Database/Content.json", "system", "post", f" ")
            msg = ReadMsg()
            return msg
          elif "edit" in Capture:
            Speak("Okey!", 0, 1.0)
            result = edit_message(message)
            organisMsg = Organise_Msg(result)
            msg = checkmsg(organisMsg)
            return msg
          else:
           Speak("Sorry, Didn't catch it", 0, 1.0)
           print("Sorry, Didn't catch it")
           msg = checkmsg(do_again)
           return msg
           
        except sr.UnknownValueError:
            Speak("Could not understand audio", 0, 1.0)
            print("Could not understand audio")
            msg = checkmsg(do_again)
            return msg
        except sr.RequestError:
            Speak("API error", 0, 1.0)
            print("API error")
            msg = checkmsg(do_again)
            return msg
   

def Organise_Msg(message):
    message = re.sub(r'\s*comma', ',', message)
    message = re.sub(r'\s*coma', ',', message)
    message = re.sub(r'\s*period', '.', message)
    message = re.sub(r'\s*dot', '.', message)
    message = re.sub(r'new line', "\n", message)
    message = re.sub(r'new space', "\n", message)
    message = re.sub(r'\s+\.', '.', message)
    
    return message.strip()



def ReadMsg():
    
    msg = ''
    print("Message?")
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try: 
        message = recognizer.recognize_google(audio).lower()
        organised_Msg = Organise_Msg(message)
        count = len(organised_Msg)
        Speak(f"Check what you have said:\n", 0, 1.0)
        POST("Database/Content.json", "system", "post", f"Do You Confirm That you have said:\n {organised_Msg}")
        count = count / 2 - 2.5
        if(count < 0):
         count = 2
        time.sleep(count)
        msg = checkmsg(organised_Msg)
        sentences = msg.split('.')
        sentences = [s.strip().capitalize() for s in sentences if s]
        msg = '. \n'.join(sentences)
        formatted_message = '\n'.join(line.strip() for line in msg.splitlines())
        return formatted_message
    except sr.UnknownValueError:
        Speak("Could not understand audio", 0, 1.0)
        print("Could not understand audio")
        msg = ReadMsg()
        return msg
    except sr.RequestError as e:
        Speak("Could not request results; {0}".format(e), 0, 1.0)
        print("Could not request results; {0}".format(e))
        msg = ReadMsg()
        return msg
 

