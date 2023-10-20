from Libraries import tk, messagebox, json
class SetUpApp:
    def __init__(self, root, title, BGcolor, txtColor, Name_Section):
        self.root = root
        self.root.title(title)
        # Change the background color of the main window
        root.configure(bg=BGcolor)
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
         # Username label and input
        self.Section_Name = tk.Label(root, text=f"{Name_Section} Configuration:", background=BGcolor)
        self.Section_Name.pack(pady=10)
        # Username label and input
        self.username_label = tk.Label(root, text="Username:", background=BGcolor)
        self.username_label.pack(pady=10)

        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        # Set the window size and disable resizing
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        # Password label and input
        self.password_label = tk.Label(root, text="Password:", background=BGcolor)
        self.password_label.pack(pady=10)
        
        self.password_entry = tk.Entry(root, show="*")  # Use '*' to hide the password
        self.password_entry.pack(pady=5)
        
        # Button for authentication
        if(title == "Set up Email"):
         self.login_button = tk.Button(root, text="Enter to Email", command=self.Email_SetUp, background="Black", fg=txtColor, cursor="hand2", )
         self.login_button.pack(pady=20)
        if(title == "Set up Netflix"):
         self.login_button = tk.Button(root, text="Enter to Netflix", command=self.Netflix_SetUp, background="Black", fg=txtColor, cursor="hand2")
         self.login_button.pack(pady=20)
        if(title == "Set up Spotify"):
         self.login_button = tk.Button(root, text="Enter to Spotify", command=self.Spotify_SetUp, background="Black", fg=txtColor, cursor="hand2")
         self.login_button.pack(pady=20)
        if(title == "Set up Primevideo"):
         self.login_button = tk.Button(root, text="Enter to Primevideo", command=self.Primevideo_SetUp, background="Black", fg=txtColor, cursor="hand2")
         self.login_button.pack(pady=20)
        
    def Email_SetUp(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username != "" and password != "":
            with open("Database/Data.json", 'r') as file:
             data = json.load(file)
             data["Login"]["L_email"] = username
             data["Login"]["E_APIKEY"] = password
              # Write the updated data back to the JSON file
            with open("Database/Data.json", 'w') as file:
             json.dump(data, file, indent=4)
            
            messagebox.askokcancel("Configuration", "Checking...")
            self.root.destroy()
            return username
        else:
            messagebox.showerror("Empty Value/s", "Incorrect username or password")
            return False
    def Netflix_SetUp(self):
        pass
    def Spotify_SetUp(self):
        pass
    def Primevideo_SetUp(self):
        pass
    def on_closing(self):
        # This function will be called when the "X" icon is pressed.
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            quit()
            