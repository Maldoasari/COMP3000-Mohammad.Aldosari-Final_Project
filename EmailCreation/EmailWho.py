from Libraries import sr, time, json, re, recognizer
from Voice_Assistant.Speak import Speak
from Voice_Assistant.Read_Email_Voice_Inputs import POST
num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twleve"]
top_level_domain  = ['gmail', 'outlook', 'yahoo', 'hotmail', 'mail', 'icloud'] 

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

def ChangerTool(reciver):
    email_address = ''
    do_Again = reciver
    new_stri = list(reciver)
    #print(len(reciver))
    x = ''
    count = 0
    for index, letter in enumerate(reciver):
        count = count + 1 
        x = x + f"letter {letter} : at {index},\n"
    count = count / 2 - 2.5
    if(count < 0):
        count = 2
    print(count)
    POST("Database/Email.json", "system", "post", f"{x}")
    time.sleep(count)
    Speak("Look at the console. say what index you want to change", 0, 1.0)
    
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=3)
            Capture = recognizer.recognize_google(audio).lower()
            index_to_change = None  
            for n in num:
                if n in Capture:
                    index_to_change = word_to_number(n)
                    if index_to_change is None or index_to_change > len(reciver)-1:
                        Speak("list index out of range", 0, 1.0)
                        email_address = ChangerTool(do_Again)   
                    else:
                        break
                
            if index_to_change is None:
                numbers = re.findall(r'\b\d+\b', Capture)
                if numbers:
                    index_to_change = int(numbers[0])
                    if index_to_change > len(reciver)-1:
                        Speak("list index out of range", 0, 1.0)
                        email_address = ChangerTool(do_Again)   # Using return to ensure we break out
                        
            if index_to_change is None:
                Speak("Let's try again", 0, 1.0)
                email_address = ChangerTool(do_Again)  # Using return to ensure we break out
            #print(int(Capture[-1]))

            if index_to_change is not None and index_to_change < len(new_stri):
                time.sleep(1.5)
                Speak("What letter?", 0, 1.0)
                with sr.Microphone() as source1:
                    print("What letter?")
                    audio2 = recognizer.listen(source1)
                    Capture2 = recognizer.recognize_google(audio2).lower()
                    
                    new_stri[index_to_change] = Capture2[-1]
                    POST("Database/Email.json", "system", "post", " ")
                    p = ""
                    p = f"FROM {reciver[index_to_change].upper()} : TO {Capture2[-1].upper()}"
                    POST("Database/Email.json", "system", "post", f"{p}")
                    time.sleep(0.5)
                    Speak(f"From {reciver[index_to_change].upper()}, To {Capture2[-1].upper()}", 0, 1.0)
                    POST("Database/Email.json", "system", "post", " ")
                #print("lets try again\n")
                #print(Capture)
                #ChangerTool(do_Again)
            else:
                print("lets try again\n")
                Speak("lets try again\n", 0, 1.0)
                email_address = ChangerTool(do_Again)
                
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
            Speak("Sorry, I couldn't understand the audio.", 0, 1.0)
            print("lets try again\n")
            Speak("lets try again\n", 0, 1.0)
            email_address = ChangerTool(do_Again)
        except sr.RequestError:
            print("API unavailable or quota exceeded.")
            email_address = ChangerTool(do_Again)
            
    email_address = ''.join(new_stri)
    #time.sleep(1)
    
    return email_address

def ChangerToolAdd(email_address):
    # Enumerate letters of email address
    x = ""
    count = 0
    for index, letter in enumerate(email_address):
        count = count + 1
        time.sleep(0.1)
        x = x + f"Letter: '{letter}' at position: {index} \n"
    count = count / 2 - 2.5
    if(count < 0):
        count = 2
    print(x)
    POST("Database/Email.json", "system", "post", f"{x}")
    while True:  # Using a loop instead of recursion
        time.sleep(count)
        Speak("Please choose two consecutive indexes to add your value in between", 0, 1.0)
        Speak("You must say: [index] and [index]", 0, 1.0)
        with sr.Microphone() as source:
            try:
                l = []
                audio = recognizer.listen(source)
                Capture = recognizer.recognize_google(audio).lower()
                print(Capture)

                # Check against num
                for b in num:
                    if b in Capture:
                        l.append(b)

                print(l) 

                # Extract numbers from Capture
                numbers = re.findall(r'\b\d+\b', Capture)
                int_numbers = [int(nums) for nums in numbers]

                if not int_numbers and l:
                    indexStart = word_to_number(l[-2]) if len(l) > 1 else None
                    indexEnd = word_to_number(l[-1]) if l else None
                elif int_numbers:
                    indexStart = int_numbers[0]
                    indexEnd = int_numbers[1] if len(int_numbers) > 1 else None
                else:
                    print("Couldn't understand the indexes, try again.")
                    continue

                if indexStart is not None and indexEnd is not None and indexStart + 1 == indexEnd:
                    print("Indexes are consecutive")
                    Speak("Now choose the letter or number that you want to add in between", 0, 1.0)
                    POST("Database/Email.json", "system", "post", " ")
                    audio = recognizer.listen(source)
                    Capture = recognizer.recognize_google(audio).lower()
                    add_letter = Capture[-1]
                    Speak("Added with success", 0, 1.0)
                    # Modify this line to insert the letter between the indices
                    return email_address[:indexEnd] + add_letter + email_address[indexEnd:]

                else:
                    print("You have chosen two indexes that are not consecutive")
                    print("Try again\n")
                    continue

            except sr.UnknownValueError:
                Speak("Could not understand audio", 0, 1.0)
                print("Could not understand audio")
                Speak("Check what you have said", 0, 1.0)
                continue  # Go back to the start of the loop and try again

            except sr.RequestError:
                Speak("API error", 0, 1.0)
                print("API error")
                continue  # Go back to the start of the loop and try again
def Top_level_domain():
    domain = ''
    Speak("Choose domain", 0, 1.0)
    with sr.Microphone() as source:
        try:
            
            print("\nChoose domain")
            audio = recognizer.listen(source)
            Capture = recognizer.recognize_google(audio).lower()
            for i in top_level_domain:
                if(i in Capture):
                    Speak(f"Done. you have chosen {i}", 0, 1.0)
                    return i 
                else:
                    Speak("the given domain is not found", 0, 1.0)
                    print("the given domain is not found")
                    domain = Top_level_domain()
                return i
        except sr.UnknownValueError:
            Speak("Could not understand audio", 0, 1.0)
            print("Could not understand audio")
            Speak("Check what you have said", 0, 1.0)
            domain = Top_level_domain()
        except sr.RequestError:
            Speak("API error", 0, 1.0)
            print("API error")
            domain = Top_level_domain()
        
    return domain

def checkWho(reciver):
    
    email_address = ''
    reciver_without_spaces = reciver.replace(" ", "")
    time.sleep(0.1)
    Speak("Confirm.. or Change letters... or insert a letter ", 0, 1.0)
    with sr.Microphone() as source:
        try:
            print("\nConfirm.. or Change letters... or insert a letter")
            audio = recognizer.listen(source, timeout=3)
            Capture = recognizer.recognize_google(audio).lower()

            if ("yes" in Capture) or ("confirm" in Capture) or ("posative" in Capture):
                time.sleep(0.5)
                TopLevelDomain = Top_level_domain()
                email_address = reciver_without_spaces + "@" + TopLevelDomain +".com"
                POST("Database/Email.json", "system", "post", " ")
                return email_address
                
            elif ("no" in Capture) or ("change letter" in Capture) or ("change" in Capture):
                Speak("Change letters within the email", 0, 1.0)
                result = ChangerTool(reciver_without_spaces)
                Speak("Modified Successfully", 0, 1.0)
                POST("Database/Email.json", "system", "post", f"{result}: \n is the first part of the email \n are you happy with it?")
                time.sleep(7)
                email_address = checkWho(result)
                return email_address 
            
            elif ("add a letter" in Capture) or ("add letters" in Capture) or ("insert" in Capture):
                Speak("Add letters in the email", 0, 1.0)
                print("Add letters in the email")
                result = ChangerToolAdd(reciver_without_spaces)
                Speak("Modified", 0, 1.0)
                POST("Database/Email.json", "system", "post", f"{result}: \n is the first part of the email \n are you happy with it?")
                time.sleep(7)
                email_address = checkWho(result)
                return email_address
                #return email_address
            elif("try again" in Capture) or ("new attempt" in Capture):
                Speak("okey, to who?", 0, 1.0)
                email_address = whoIStheR()
                
            else:
                Speak("Sorry, Didn't catch it", 0, 1.0)
                print("Sorry, Didn't catch it")
                Speak("Check what you have said", 0, 1.0)
                print(f"{reciver_without_spaces}")
                email_address = checkWho(reciver_without_spaces)
        except sr.UnknownValueError:
            Speak("Could not understand audio", 0, 1.0)
            print("Could not understand audio")
            Speak("Check what you have said", 0, 1.0)
            email_address = checkWho(reciver_without_spaces)
        except sr.RequestError:
            Speak("API error", 0, 1.0)
            print("API error")
            email_address = checkWho(reciver_without_spaces)
    
def whoIStheR():
    SenderEmail = ''
   # Speak("To Who?", 0, 1.0)
    with sr.Microphone() as source:
        try:
            print("To Who?")
            audio = recognizer.listen(source)
            p_reciver = recognizer.recognize_google(audio).lower().replace("period", ".")
            reciver = p_reciver.replace(" ", "")
            Speak(f"Check what you have said:\n", 0, 1.0)
            print(f"Confirm that you have said:\n {reciver}")
            time.sleep(1)
            SenderEmail = checkWho(reciver)
            return SenderEmail
        except sr.UnknownValueError:
             print("Could not understand audio")
             Speak("Could not understand audio", 0, 1.0)
             SenderEmail = whoIStheR() 
        except sr.RequestError:
            print("API error")
            SenderEmail = whoIStheR()
    return SenderEmail
   

def AddNew_or_ChooseFromStorage():
    status = ''
    print("Add new? or Choose from storage?")
   # time.sleep(0.1)
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio).lower()
            if("add new" in text):
                status = 'add'
                return status
            elif("storage" in text):
                status = 'storage'
                return status
            else:
                status = 'badRequest'
        except sr.UnknownValueError:
            print("Could not understand audio")
            status = AddNew_or_ChooseFromStorage()
        except sr.RequestError:
            print("API error")
            status = AddNew_or_ChooseFromStorage()
    return status

def list_emails():
    with open("Database\Cookies.json", "r") as file:
        data = json.load(file)
    x = "" 
    count = 0
    emails = [record["email"] for record in data]
    for index, email in enumerate(emails, start=1):
        count = count + 1
        x = x + f"{index}. {email} \n"
    
    return emails, x, count

def choose_email(emails, x, count):
    POST("Database/Email.json", "system", "post", f"your storage have {len(emails)} records")
    Speak(f"your storage have {len(emails)} records", 0, 1.0)
    if(len(emails) == 1):
        return emails[0]
    else:
     POST("Database/Email.json", "system", "post", f"{x}")
     count = count / 2 - 2.5
     if(count < 0):
        count = 2
     time.sleep(count)
     Speak("What email you want to choose?", 0, 1.0)
     with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            captureit = recognizer.recognize_google(audio).lower()
          
            for n in num:
                if n in captureit:
                    index_to_change = word_to_number(n)
                    break

           
            if index_to_change is None:
                numbers = re.findall(r'\b\d+\b', captureit)
                if numbers:
                   
                    index_to_change = int(''.join(numbers))
                else:
                     print("No numbers found in the input.")
            #print(index_to_change)   
            if index_to_change is not None and index_to_change < len(emails):
               return emails[index_to_change - 1]
            #elif captureit[-1] != len(emails[int(captureit[-1])-1]):
                #return emails[int(captureit[-1]) - 1]
            elif (index_to_change is None) or (captureit.isalpha()):
                 print("something went wrong\n lets try again aa")
                 choose_email(emails, x, count)
            else:
                print("what are you doing!!")
            return emails[index_to_change - 1]
        except sr.UnknownValueError:
            print("Could not understand the audio _-_")
            return choose_email(emails, x, count)
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return choose_email(emails, x, count)


def storage():
    emails, x, count = list_emails()
    chosen_email = choose_email(emails, x, count)
    if chosen_email:
        return chosen_email
    else:
        return None
def storageCheck():
    emails = list_emails()
    if len(emails) <= 1:
        return None
    else:
        return emails
