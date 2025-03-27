import os
import time
import zipfile
import itertools
import string
import pyfiglet

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
B = '\033[94m'
P = '\033[95m'
C = '\033[96m'
W = '\033[97m'
N = '\033[0m'

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def show_banner(text, color):
    clear()
    banner = pyfiglet.figlet_format(text)
    print(f"{color}{banner}{N}")

def dht_hackers_banner():
    show_banner("DHT-HACKERS", R)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{G} THIS TOOL IS PAID! TO USE IT FOR FREE:")
    print(f"{P} SUBSCRIBE TO OUR CHANNEL FOR ETHICAL HACKING TUTORIALS!")
    print(f"{B} https://youtube.com/@dht-hackers_10?si=lsdJ-naJvp7ql-QT")
    print(f"{C}────────────────────────────────────────────────────────────{N}")
    time.sleep(2)
    os.system("termux-open-url https://youtube.com/@dht-hackers_10?si=lsdJ-naJvp7ql-QT")
    input(f"{Y}Press Enter after subscribing to continue...{N}")
    clear()

def dht_zipper_banner():
    show_banner("DHT-ZIPPER", B)
    print(f"{C}────────────────────────────────────────────────────────────")
    print(f"{G} FAST & POWERFUL ZIP PASSWORD CRACKER")
    print(f"{Y} Developed by: DHT-HACKERS TEAM | Multi-threaded | High Performance")
    print(f"{C}────────────────────────────────────────────────────────────{N}")


def crack_zip(zip_file, max_length):
    start_time = time.time()
    chars = string.ascii_letters + string.digits + string.punctuation
    found = False
    password = None

    for length in range(1, max_length + 1):
        print(f"Trying passwords of length {length}...")
        for attempt in itertools.product(chars, repeat=length):
            password = ''.join(attempt)
            print(f"Trying password: {password}", end='\r')
            try:
                with zipfile.ZipFile(zip_file) as zip_file_ref:
                    zip_file_ref.extractall(pwd=password.encode('utf-8'))
                found = True
                end_time = time.time()
                print(f"\n\033[1m\033[92mPassword found: {password}\033[0m")
                print(f"\033[1m\033[92mTime taken: {end_time - start_time} seconds\033[0m")
                return
            except Exception as e:
                pass

    if not found:
        print("\n\033[1m\033[91mPassword not found\033[0m")

def crack_zip_wordlist(zip_file, wordlist):
    print(f"\nCracking ZIP file: {zip_file}\n")
    print(f"Using wordlist: {wordlist}\n")
    start_time = time.time()
    with open(wordlist, 'r') as f:
        for line in f:
            password = line.strip()
            print(f"Trying password: {password}", end='\r')
            try:
                with zipfile.ZipFile(zip_file) as zip_file_ref:
                    zip_file_ref.extractall(pwd=password.encode())
                end_time = time.time()
                print(f"\n\033[1m\033[92mPassword found: {password}\033[0m")
                print(f"\033[1m\033[92mTime taken: {end_time - start_time} seconds\033[0m")
                return
            except Exception as e:
                pass
    print("\nPassword not found")

def main():
    dht_hackers_banner()
    dht_zipper_banner()
    print("Choose a method:")
    print("1. Crack ZIP without wordlist")
    print("2. Crack ZIP with wordlist")
    choice = input("Enter your choice (1/2): ")
    zip_file = input("Enter ZIP file path: ")

    if choice == '1':
        max_length = int(input("Enter maximum password length: "))
        crack_zip(zip_file, max_length)
    elif choice == '2':
        wordlist = input("Enter wordlist file path: ")
        crack_zip_wordlist(zip_file, wordlist)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
