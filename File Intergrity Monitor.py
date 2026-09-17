import hashlib
import os

#Storage for baseline fingerprints

baseline_data = {}

def create_baseline():

    print ("\n--- Creating Baseline ---")

    target_files = os.listdir("Monitored_files")

    for filename in target_files:

        file_path = os.path.join("Monitored_files", filename)

        with open (file_path, "rb") as f:

            file_bytes = f.read()

            file_hash = hashlib.sha256(file_bytes).hexdigest()
        
        print (f"Found File: {filename}")

        baseline_data[filename] = file_hash

    

def check_integrity():

    print ("\n--- Running Integrity Check --- ")

    pass
    

def view_baseline():

    print ("\n--- Current Baseline Snapshot ---")

    if not baseline_data:

        print ("No baseline data found. Please run Option 1 first.")


    for filename, file_hash in baseline_data.items():

        print (f"File: {filename} \nHash: {file_hash}\n")
    
    

    

#MENU

while True:

    print ("\nFile Integrity Monitor")

    print ("\n1. Create Baseline")

    print ("\n2. Run Integrity  Check")

    print ("\n3. View Baseline Data")

    print ("\n4. Exit")

    user_choice = input("\nChoose an option: ")

    if user_choice == "1":

        create_baseline()



    elif user_choice == "2":

        check_integrity()

    elif user_choice == "3":

        view_baseline()

    elif user_choice == "4":

        print ("\nExiting...")
        break

    else:

        print ("Invalid, Please choose 1-4.")

