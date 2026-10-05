import hashlib
import os
import json
import time 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONITORED_DIR = os.path.join(BASE_DIR, "Monitored_files")
BASELINE_FILE = os.path.join(BASE_DIR, "baseline.json")



#Storage for baseline fingerprints
baseline_data = {}

def create_baseline():
    if not os.path.isdir(MONITORED_DIR):

        print(f"[ERROR] Folder not found: {MONITORED_DIR}")

        return
    print ("\n--- Creating Baseline ---")

    global baseline_data
    baseline_data = {}

    target_files = os.listdir(MONITORED_DIR)

    for filename in target_files:

        file_path = os.path.join(MONITORED_DIR, filename)

        if os.path.isdir(file_path): 
            continue

        with open (file_path, "rb") as f:

            file_bytes = f.read()

            file_hash = hashlib.sha256(file_bytes).hexdigest()
        
        print (f"Found File: {filename}")

        baseline_data[filename] = file_hash

    with open (BASELINE_FILE, "w") as f:

        json.dump(baseline_data, f)


    

def check_integrity():
    

    
        
    if not baseline_data:
            
        print ("\n[ERROR] No baseline data found. Create a baseline first.")
        return
    
    print ("\n--- Monitoring Directory... Press Ctrl + C to Stop ---")


    try:
        
        reported = set()

        while True:

            for filename in os.listdir(MONITORED_DIR):

                file_path = os.path.join(MONITORED_DIR, filename)

                if os.path.isdir(file_path): 
                    continue
  
                if filename not in baseline_data:

                    key = ("new", filename)

                    if key not in reported:
                    
                        print (f"[ALERT] New file detected: {filename}")
                        reported.add(key)


            for filename in baseline_data.keys():

                file_path = os.path.join(MONITORED_DIR, filename)

                if not os.path.exists(file_path):

                    key = ("deleted", filename)

                    if key not in reported:
                
                        print (f"[ALERT] File deleted: {filename}")
                        reported.add(key)
                    continue

                with open (file_path, "rb") as f:

                    file_bytes = f.read()

                    current_hash = hashlib.sha256(file_bytes).hexdigest()
                        
                
                if baseline_data[filename] != current_hash:

                    key = ("modified", filename)

                    if key not in reported:

                        print (f"[WARNING] File has been modified: {filename}")
                        reported.add(key)

            time.sleep(2)
            
    except KeyboardInterrupt:

            print ("\n--- Monitoring Stopped. returning to Menu. ---")
                            
def view_baseline():

    print ("\n--- Current Baseline Snapshot ---")

    if not baseline_data:

        print ("No baseline data found. Please run Option 1 first.")


    for filename, file_hash in baseline_data.items():

        print (f"File: {filename} \nHash: {file_hash}\n")
    
    
try:

    with open (BASELINE_FILE, "r") as f:

        baseline_data = json.load(f)

except FileNotFoundError:

    pass
    

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

        print ("\nExiting...\n")
        break

    else:

        print ("Invalid, Please choose 1-4.")

