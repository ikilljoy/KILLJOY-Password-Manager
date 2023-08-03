from cryptography.fernet import Fernet
import os
import random
import string
import getpass
import hashlib
import pyperclip

### Logo ###
art = '''
\033[32m~~~~~~~~~~ KILLJOY.DEV ~~~~~~~~~~~ \033[0m
\033[36m██╗  ██╗     ██╗██████╗ ███╗   ███╗\033
\033[36m██║ ██╔╝     ██║██╔══██╗████╗ ████║\033
\033[36m█████╔╝      ██║██████╔╝██╔████╔██║\033
\033[36m██╔═██╗ ██   ██║██╔═══╝ ██║╚██╔╝██║\033
\033[36m██║  ██╗╚█████╔╝██║     ██║ ╚═╝ ██║\033
\033[36m╚═╝  ╚═╝ ╚════╝ ╚═╝     ╚═╝     ╚═╝\033
\033[32m~~~~ KILLJOY PASSWORD MANAGER ~~~~ \033[0m
'''
cyan_art = "\033[36m" + art + "\033[0m"
### Logo end ###
### LOGO2 ####
art2 = '''
\033[31m
                            ______
                         .-"      "-.
                        /            '
            _          |              |          _
           ( \         |,  .-.  .-.  ,|         / )
            > "=._     | )(__/  \__)( |     _.=" <
           (_/"=._"=._ |/     /\     \| _.="_.="\_)
                  "=._ (_     ^^     _)"_.="
                      "=\__|IIIIII|__/="
                     _.="| \IIIIII/ |"=._
           _     _.="_.="\          /"=._"=._     _
          ( \_.="_.="     `--------`     "=._"=._/ )
           > _.="            KJPM            "=._ <
          (_/                                    \_)
██ ███    ██  ██████  ██████  ██████  ██████  ███████  ██████ ████████ 
██ ████   ██ ██      ██    ██ ██   ██ ██   ██ ██      ██         ██    
██ ██ ██  ██ ██      ██    ██ ██████  ██████  █████   ██         ██    
██ ██  ██ ██ ██      ██    ██ ██   ██ ██   ██ ██      ██         ██    
██ ██   ████  ██████  ██████  ██   ██ ██   ██ ███████  ██████    ██    
                                                                       
 ██████   █████  ███████ ███████ ██     ██  ██████  ██████  ██████  
 ██   ██ ██   ██ ██      ██      ██     ██ ██    ██ ██   ██ ██   ██ 
 ██████  ███████ ███████ ███████ ██  █  ██ ██    ██ ██████  ██   ██ 
 ██      ██   ██      ██      ██ ██ ███ ██ ██    ██ ██   ██ ██   ██ 
 ██      ██   ██ ███████ ███████  ███ ███   ██████  ██   ██ ██████  
'''
red_art = "\033[31m" + art2 + "\033[0m"
##### LOGO2 END ####

MEMORY_FOLDER = "Memory"

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt data using the key
def encrypt_password(key, data):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special):
    characters = ""
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_lowercase:
        characters += string.ascii_lowercase
    if use_numbers:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    
    if not characters:
        print("Please select at least one character type.")
        return
    
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def create_master_password():
    master_password = getpass.getpass("Create a master password: ")
    hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
    
    # Save the hashed master password to a file
    with open(os.path.join(MEMORY_FOLDER, "Key.txt"), "w") as key_file:
        key_file.write(hashed_password)

def list_services():
    print("List of Services:")
    files = [f for f in os.listdir(MEMORY_FOLDER) if f.endswith('.txt') and f != 'Key.txt']
    services = [f[:-4] for f in files]  # Remove the '.txt' extension
    for idx, service in enumerate(services, start=1):
        print(f"{idx}. \033[33m{service}\033[0m")  # Use "\033[33m" for yellow color



# New function for password retrieval and decryption
def retrieve_password():
    master_password = getpass.getpass("Enter the master password: ")
    hashed_input_password = hashlib.sha256(master_password.encode()).hexdigest()

    with open(os.path.join(MEMORY_FOLDER, "Key.txt"), "r") as key_file:
        hashed_master_password = key_file.read().strip()
        if hashed_input_password != hashed_master_password:
            print(red_art)  # Print the red ASCII art
            return

        service_name = input("Enter the Service / Password Name: ")
        file_path = os.path.join(MEMORY_FOLDER, f"{service_name}.txt")

        if not os.path.exists(file_path):
            print("Password not found for the given service.")
            return

        with open(file_path, "rb") as file:
            data = file.read().splitlines()

        if len(data) != 2:
            print("Password data is corrupted.")
            return

        key = data[0]
        encrypted_password = data[1]

        fernet = Fernet(key)
        decrypted_password = fernet.decrypt(encrypted_password).decode()

        try:
            pyperclip.copy(decrypted_password)
            print("\033[32mPassword copied to clipboard.\033[0m")
        except ImportError:
            print("Password:", decrypted_password)

def main():
    ### Print the art
    print(cyan_art)

    # Create the "Memory" folder if it doesn't exist
    if not os.path.exists(MEMORY_FOLDER):
        os.makedirs(MEMORY_FOLDER)

    # Check if the master password exists
    if not os.path.exists(os.path.join(MEMORY_FOLDER, "Key.txt")):
        print("No master password found, Let's create one!")
        create_master_password()
        print("Master password created successfully.")

    while True:
        print("\033[1m\nMenu:\033[0m")
        print("\033[31m1.\033[0m Generate Password")
        print("\033[31m2.\033[0m Retrieve Password")
        print("\033[31m3.\033[0m Services")
        print("\033[31m4.\033[0m Exit")

        choice = input("Select an option: ")

        if choice == "1":
            length = int(input("Enter the desired password length: "))
            use_uppercase = input("Include uppercase letters? (y/n): ").strip().lower() == 'y'
            use_lowercase = input("Include lowercase letters? (y/n): ").strip().lower() == 'y'
            use_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
            use_special = input("Include special characters? (y/n): ").strip().lower() == 'y'
            
            # Generate a new encryption key
            key = generate_key()
            
            password = generate_password(length, use_uppercase, use_lowercase, use_numbers, use_special)
            if password:
                service_name = input("Enter the Service / Password Name: ")
                encrypted_password = encrypt_password(key, password)
                print("Generated Password:", password)
                
                # Save the encrypted password and key to a file in the "Memory" folder
                file_path = os.path.join(MEMORY_FOLDER, f"{service_name}.txt")
                with open(file_path, "wb") as file:
                    file.write(key + b'\n')
                    file.write(encrypted_password)
        elif choice == "2":
            retrieve_password()
        elif choice == "3":
            list_services()
        elif choice == "4":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
