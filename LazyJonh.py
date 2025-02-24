import re
import subprocess
import os
import time
from datetime import datetime

# Colores para el texto
Red = "\033[1;91m"
Green = "\033[0;92m"
Yellow = "\033[0;93m"
Blue = "\033[1;94m"
White = "\033[0;97m"

# Configuración global
WORDLIST_DIR = "wordlists"
LOG_FILE = "lazy_john.log"
DEFAULT_WORDLIST = os.path.join(WORDLIST_DIR, "rockyou.txt")

# Crear directorio de wordlists si no existe
if not os.path.exists(WORDLIST_DIR):
    os.makedirs(WORDLIST_DIR)

# Banner de Lazy John 
def banner():
    print(f"""{Red}
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ _                               _                _     @
@| |                             | |              | |    @
@| |      __ _  ____ _   _       | |  ___   _ __  | |__  @
@| |     / _` ||_  /| | | |  _   | | / _ \ | '_ \ | '_ \ @
@| |____| (_| | / / | |_| | | |__| || (_) || | | || | | |@
@|______|\__,_|/___| \__, |  \____/  \___/ |_| |_||_| |_|@
@                     __/ |                              @
@                    |___/                               @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    {Yellow}
    The most advanced lazy script for John the Ripper and Hashcat.
    Automate hash cracking with advanced features.
    {Green}
    Developed by: Your Name
    Version: 2.0 Pro
    {White}""")

# Función para registrar actividades en un log
def log_activity(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as log:
        log.write(f"[{timestamp}] {message}\n")

# Función para detectar el tipo de hash
def detect_hash(hash_str):
    hash_patterns = {
        "MD5": r"^[a-f0-9]{32}$",        # MD5
        "SHA1": r"^[a-f0-9]{40}$",       # SHA1
        "SHA256": r"^[a-f0-9]{64}$",     # SHA256
        "SHA512": r"^[a-f0-9]{128}$",    # SHA512
        "bcrypt": r"^\$2[ayb]\$.{56}$",  # bcrypt
        "sha512crypt": r"^\$6\$.{1,2}\$.+",  # SHA-512 crypt
        "sha512crypt_y": r"^\$y\$.{1,2}\$.+",  # SHA-512 crypt con $y$
        "NTLM": r"^[a-f0-9]{32}$",      # NTLM
        "LM": r"^[a-f0-9]{32}$",        # LM
        "MySQL4.1+": r"^[a-f0-9]{40}$", # MySQL 4.1+
        "Wordpress": r"^\$P\$.{31}$",   # Wordpress
    }
    
    for hash_type, pattern in hash_patterns.items():
        if re.match(pattern, hash_str):
            return hash_type
    return None

# Función para crackear con John the Ripper
def crack_with_john(hash_str, wordlist=DEFAULT_WORDLIST, attack_mode="dictionary"):
    print(f"{Green}[*] Cracking with John the Ripper... Hash: {hash_str}{White}")
    log_activity(f"Starting John the Ripper on hash: {hash_str}")
    
    # Escribir el hash en un archivo temporal
    with open("hashes.txt", "w") as f:
        f.write(hash_str + "\n")

    # Configurar el comando según el modo de ataque
    if attack_mode == "dictionary":
        command = ["john", "--wordlist=" + wordlist, "hashes.txt"]
    elif attack_mode == "brute-force":
        command = ["john", "--incremental", "hashes.txt"]
    elif attack_mode == "mask":
        mask = input(f"{Green}┌─[Enter Mask]──[~]─[John the Ripper]:\n└─────►{White} ")
        command = ["john", "--mask=" + mask, "hashes.txt"]
    
    # Ejecutar John the Ripper
    subprocess.run(command)
    log_activity(f"John the Ripper finished on hash: {hash_str}")

# Función para crackear con Hashcat
def crack_with_hashcat(hash_str, wordlist=DEFAULT_WORDLIST, hash_mode=0, attack_mode="dictionary"):
    print(f"{Green}[*] Cracking with Hashcat... Hash: {hash_str}{White}")
    log_activity(f"Starting Hashcat on hash: {hash_str}")
    
    # Escribir el hash en un archivo temporal
    with open("hashes.txt", "w") as f:
        f.write(hash_str + "\n")

    # Configurar el comando según el modo de ataque
    if attack_mode == "dictionary":
        command = ["hashcat", "-m", str(hash_mode), "-a", "0", "hashes.txt", wordlist]
    elif attack_mode == "brute-force":
        command = ["hashcat", "-m", str(hash_mode), "-a", "3", "hashes.txt", "?a?a?a?a?a?a"]
    elif attack_mode == "mask":
        mask = input(f"{Green}┌─[Enter Mask]──[~]─[Hashcat]:\n└─────►{White} ")
        command = ["hashcat", "-m", str(hash_mode), "-a", "3", "hashes.txt", mask]
    
    # Ejecutar Hashcat
    subprocess.run(command)
    log_activity(f"Hashcat finished on hash: {hash_str}")

# Menú para seleccionar el tipo de hash
def hash_type_menu():
    print(f"{Yellow}\n[ Select Hash Type ]{White}")
    print("1) MD5")
    print("2) SHA1")
    print("3) SHA256")
    print("4) SHA512")
    print("5) bcrypt")
    print("6) NTLM")
    print("7) MySQL4.1+")
    print("8) Wordpress")
    print("9) Scan and Detect Automatically")
    choice = input(f"{Green}┌─[Select Option]──[~]─[Hash Type]:\n└─────►{White} ")
    return choice

# Menú para seleccionar el modo de ataque
def attack_mode_menu():
    print(f"{Yellow}\n[ Select Attack Mode ]{White}")
    print("1) Dictionary Attack")
    print("2) Brute-Force Attack")
    print("3) Mask Attack")
    choice = input(f"{Green}┌─[Select Option]──[~]─[Attack Mode]:\n└─────►{White} ")
    return choice

# Menú principal
def main_menu():
    banner()
    print(f"{Yellow}\n[ Select Tool ]{White}")
    print("1) John the Ripper")
    print("2) Hashcat")
    print("3) Manage Wordlists")
    print("4) Exit")
    choice = input(f"{Green}┌─[Select Option]──[~]─[Main Menu]:\n└─────►{White} ")
    return choice

# Función para gestionar wordlists
def manage_wordlists():
    print(f"{Yellow}\n[ Manage Wordlists ]{White}")
    print("1) List Wordlists")
    print("2) Add New Wordlist")
    print("3) Set Default Wordlist")
    choice = input(f"{Green}┌─[Select Option]──[~]─[Wordlists]:\n└─────►{White} ")
    
    if choice == "1":
        print(f"{Green}\nAvailable Wordlists:{White}")
        for wordlist in os.listdir(WORDLIST_DIR):
            print(f"- {wordlist}")
    elif choice == "2":
        new_wordlist = input(f"{Green}┌─[Enter Path to New Wordlist]:\n└─────►{White} ")
        if os.path.isfile(new_wordlist):
            os.system(f"cp {new_wordlist} {WORDLIST_DIR}")
            print(f"{Green}[+] Wordlist added successfully.{White}")
        else:
            print(f"{Red}[-] File not found.{White}")
    elif choice == "3":
        new_default = input(f"{Green}┌─[Enter Default Wordlist Name]:\n└─────►{White} ")
        if os.path.isfile(os.path.join(WORDLIST_DIR, new_default)):
            global DEFAULT_WORDLIST
            DEFAULT_WORDLIST = os.path.join(WORDLIST_DIR, new_default)
            print(f"{Green}[+] Default wordlist set to {new_default}.{White}")
        else:
            print(f"{Red}[-] Wordlist not found.{White}")

# Función principal
def main():
    while True:
        tool_choice = main_menu()
        
        if tool_choice == "1":  # John the Ripper
            hash_choice = hash_type_menu()
            attack_choice = attack_mode_menu()
            hash_str = input(f"{Green}┌─[Enter Hash]──[~]─[John the Ripper]:\n└─────►{White} ")
            
            if hash_choice == "9":  # Escanear y detectar automáticamente
                hash_type = detect_hash(hash_str)
                if hash_type:
                    print(f"{Green}[+] Detected Hash Type: {hash_type}{White}")
                    crack_with_john(hash_str, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")
                else:
                    print(f"{Red}[-] Hash type not recognized.{White}")
            else:
                crack_with_john(hash_str, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")
        
        elif tool_choice == "2":  # Hashcat
            hash_choice = hash_type_menu()
            attack_choice = attack_mode_menu()
            hash_str = input(f"{Green}┌─[Enter Hash]──[~]─[Hashcat]:\n└─────►{White} ")
            
            if hash_choice == "9":  # Escanear y detectar automáticamente
                hash_type = detect_hash(hash_str)
                if hash_type:
                    print(f"{Green}[+] Detected Hash Type: {hash_type}{White}")
                    if hash_type == "MD5":
                        crack_with_hashcat(hash_str, hash_mode=0, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")
                    elif hash_type == "SHA1":
                        crack_with_hashcat(hash_str, hash_mode=100, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")
                    elif hash_type == "SHA256":
                        crack_with_hashcat(hash_str, hash_mode=1400, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")
                    elif hash_type == "SHA512":
                        crack_with_hashcat(hash_str, hash_mode=1700, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")
                else:
                    print(f"{Red}[-] Hash type not recognized.{White}")
            else:
                if hash_choice == "1":
                    crack_with_hashcat(hash_str, hash_mode=0, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")  # MD5
                elif hash_choice == "2":
                    crack_with_hashcat(hash_str, hash_mode=100, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")  # SHA1
                elif hash_choice == "3":
                    crack_with_hashcat(hash_str, hash_mode=1400, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")  # SHA256
                elif hash_choice == "4":
                    crack_with_hashcat(hash_str, hash_mode=1700, attack_mode="dictionary" if attack_choice == "1" else "brute-force" if attack_choice == "2" else "mask")  # SHA512
        
        elif tool_choice == "3":  # Gestionar wordlists
            manage_wordlists()
        
        elif tool_choice == "4":  # Salir
            print(f"{Red}\nThank you for using Lazy John Pro. Happy Hacking!{White}\n")
            break
        
        else:
            print(f"{Red}[-] Invalid option. Please try again.{White}")

if __name__ == "__main__":
    main()
