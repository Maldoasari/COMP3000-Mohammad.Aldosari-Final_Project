from Libraries import tk, sd, wav, messagebox

class VoiceRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Recorder")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.record_button = tk.Button(root, text="Record", command=self.animate_button_text)
        self.record_button.pack(pady=20)
        self.record_button.config(state=tk.NORMAL)
       
        self.root.geometry("300x200")
        self.root.resizable(False, False)
    def animate_button_text(self):
        self.record_button.config(state=tk.DISABLED)
        self.record_button.update_idletasks()
        self.animate_text("3 2 1...", 0)

    def animate_button_text(self):
        self.record_button.config(state=tk.DISABLED)
        self.record_button.update_idletasks()
        self.animate_countdown(3)

    def animate_countdown(self, count):
        if count >= 0:
            self.record_button.config(text=str(count))
            self.root.after(1000, self.animate_countdown, count - 1)
            if count == 0:
               self.record_button.config(state=tk.DISABLED, text="Speak")
               self.record_button.update_idletasks()
               
        else:
            self.start_recording()

    def start_recording(self):
        samplerate = 44100  
        duration = 5  

        audio_data = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
        sd.wait()

        # Save the recorded audio to a WAV file
        if len(audio_data) > 0:
            wav.write("Database/User.wav", samplerate, audio_data)

        self.root.destroy()

        
    def on_closing(self):
        # This function will be called when the "X" icon is pressed.
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            quit()


