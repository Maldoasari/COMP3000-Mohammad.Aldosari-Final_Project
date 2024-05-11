# This file also need alot of work, as it should display a GUI interface for the user to observe the emails content
# it has the same structure as the email tamplet in Read_Email_Voice_Inputs.py but there should be a way to combain them 
# and it has been commented for not affacting the system performnce in one script. 
"""""
import json, os, tkinter as tk
   
def Email_gui_output_template():
    # Nested function to load JSON data
    def load_jsonFile(json_file):
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return "File not found."
        except json.JSONDecodeError:
            return "Error decoding JSON."
    #typing effect function for labels
    def typing_effect_in_labels(label, full_text, speed=80):
        def add_character(char_iter):
            try:
                char = next(char_iter)
                label.config(text=label.cget("text") + char)
                root.after(speed, add_character, char_iter)
            except StopIteration:
                pass  

        label.config(text='') 
        char_iter = iter(full_text)  
        add_character(char_iter)  

     #typing effect function for widget
    def typing_effect_in_widget(text_widget, full_text, speed=10):
        text_widget.config(state="normal")
        text_widget.delete('1.0', tk.END)

        def add_character(char_iter):
            try:
                char = next(char_iter)
                text_widget.insert(tk.END, char)  
                text_widget.see(tk.END)  
                if char.isspace():  
                    text_widget.after(speed, add_character, char_iter)
                else:
                    text_widget.after(speed, add_character, char_iter)
            except StopIteration:
                text_widget.config(state="disabled")  

        char_iter = iter(full_text)  
        add_character(char_iter)  

    # updating labels and text widgets functionality
    def updating_labels(data):
        typing_effect_in_labels(email_label, data.get('Email', ''))
        typing_effect_in_labels(subject_label, data.get('Subject', ''))
        typing_effect_in_widget(msg_text, data.get('Message', ''))
        typing_effect_in_widget(system_text, data.get('System', '')) 

    #  polling JSON file for changes functionality 
    def poll_json():
        nonlocal last_modified_time
        try:
            current_modified_time = os.path.getmtime(json_file)
            if current_modified_time != last_modified_time:
                last_modified_time = current_modified_time
                json_data = load_jsonFile(json_file)
                updating_labels(json_data)
        except OSError:
            pass
        root.after(2000, poll_json)  

    #setting up GUI
    root = tk.Tk()
    root.title("Read Email Template")
    root.attributes('-topmost', True)
    root.geometry("600x500")
    root.resizable(False, False)
    root.configure(bg="lightgrey")

    #labels and text widgets creation
    tk.Label(root, text="To:", bg="lightgrey").grid(row=0, column=0, sticky="e")
    tk.Label(root, text="Subject:", bg="lightgrey").grid(row=1, column=0, sticky="e")
    tk.Label(root, text="Message:", bg="lightgrey").grid(row=3, column=0, sticky="ne")
    tk.Label(root, text="System says:", bg="lightgrey").grid(row=4, column=0, sticky="ne")

    email_label = tk.Label(root, text="", width=50, anchor="w", bg="lightgrey")
    subject_label = tk.Label(root, text="", width=50, anchor="w", bg="lightgrey")
    name_label = tk.Label(root, text="", width=50, anchor="w", bg="lightgrey")
    email_label.grid(row=0, column=1)
    subject_label.grid(row=1, column=1)
    name_label.grid(row=2, column=1)

    #frames, text widgets, and scrollbars  creataion for message and system output
    msg_frame = tk.Frame(root)
    msg_frame.grid(row=3, column=1, sticky="ew")
    systemFrame = tk.Frame(root)
    systemFrame.grid(row=4, column=1, sticky="ew")

    msg_scrollbar = tk.Scrollbar(msg_frame)
    msg_text = tk.Text(msg_frame, width=50, height=7, wrap="word", yscrollcommand=msg_scrollbar.set, bg="lightgrey")
    msg_scrollbar.config(command=msg_text.yview)
    msg_text.grid(row=0, column=0, sticky="nsew")
    msg_scrollbar.grid(row=0, column=1, sticky="ns")
    msg_frame.columnconfigure(0, weight=1)
    msg_frame.rowconfigure(0, weight=1)

    sys_scrollbar = tk.Scrollbar(systemFrame)
    system_text = tk.Text(systemFrame, width=50, height=7, wrap="word", yscrollcommand=sys_scrollbar.set, bg="lightgrey")
    sys_scrollbar.config(command=system_text.yview)
    system_text.grid(row=0, column=0, sticky="nsew")
    sys_scrollbar.grid(row=0, column=1, sticky="ns")
    systemFrame.columnconfigure(0, weight=1)
    systemFrame.rowconfigure(0, weight=1)

    # Initialize JSON file
    json_file = 'Database/Output.json'
    last_modified_time = os.path.getmtime(json_file)

    # JSON file loading and updating widgets
    json_data = load_jsonFile(json_file)
    updating_labels(json_data)

    # Start polling the JSON file for changes
    poll_json()

    # Run the main loop
    root.mainloop()

if __name__ == "__main__":
    Email_gui_output_template()

"""



