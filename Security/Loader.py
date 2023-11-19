import tkinter as tk
from tkinter import ttk

def Loader(DurationPerSecond):
    # Function to update the text
    def update_text():
        # Define your list of messages
        messages = ["Creating your account", "Creating your account.", "Creating your account..", "Creating your account..."]
        # Update the label text to the next message in the list
        loading_label.config(text=messages[update_text.index])
        # Increment the index and reset if it goes beyond the list length
        update_text.index = (update_text.index + 1) % len(messages)
        # Schedule the update_text function to run again after 1000ms
        root.after(1000, update_text)

    # Initialize the index attribute
    update_text.index = 0

    # Create the main window
    root = tk.Tk()
    root.title("Loading Page")
    root.config(bg="lightgrey")
    # Optionally, make the window borderless
    root.overrideredirect(True)  # This will remove the title bar
    root.geometry("1400x40")  # Set the window size
    root.attributes('-topmost', True)
    loading_label = tk.Label(root, text="Welcome From the system", font=("Courier New", 12), bg="lightgrey")
    loading_label.pack(expand=True)
    loading_label.pack(side='top', anchor='center')

    # Add a determinate progress bar
    progress = ttk.Progressbar(root, orient="horizontal", length=1400, mode="determinate")
    progress.pack(pady=2, fill='x', expand=True)  # Add some padding below the progress bar

    # Call the update_text function to start changing the text
    root.after(2000, update_text)

    # Start the loading process
    # Here you would have your actual loading process logic
    # For demonstration, we'll just increment the progress bar value
    
    def start_loading():
        progress['value'] += 1
        if progress['value'] < 100:
            # Schedule the start_loading function to run again after 100ms
            root.after(DurationPerSecond, start_loading)
        else:
            root.destroy()

    start_loading()

    # Run the main loop
    root.mainloop()
Loader(100)

