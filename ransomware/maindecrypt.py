import discover
import modify
from Crypto.Cipher import AES
from Crypto.Util import Counter
import base64
import os
import platform
import discover
import modify

extension = ".wasted"  # Custom encrypted extension

def decrypt(base64_aes_key):
    key = base64.b64decode(base64_aes_key)

    # Create AES CTR cipher
    ctr = Counter.new(128)
    crypt = AES.new(key, AES.MODE_CTR, counter=ctr)

    # Target folder
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        startdirs = [os.environ['HOME'] + '/Desktop/Netsec']
    elif plt == "Windows":
        startdirs = [os.environ['USERPROFILE'] + '\\Desktop\\Netsec']
    else:
        print("Unidentified OS.")
        return

    # Decrypt all files with .wasted
    for currentDir in startdirs:
        for file in discover.discoverFiles(currentDir):
            if file.endswith(extension):
                modify.modify_file_inplace(file, crypt.encrypt)
                original = os.path.splitext(file)[0]
                os.rename(file, original)
                print(f"[+] Decrypted: {original}")

