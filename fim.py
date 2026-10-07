import hashlib
import os
import json
import time 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MONITORED_DIR = os.path.join(BASE_DIR, "Monitored_files")
BASELINE_FILE = os.path.join(BASE_DIR, "baseline.json")



#Storage for baseline fingerprints
baseline_data = {}


def hash_file(path, chunk_size = 8192):

    sha256 = hashlib.sha256()

    with open(path, "rb") as f:

        while chunk := f.read(chunk_size):

            sha256.update(chunk)

    return sha256.hexdigest()

def scan_folder(folder):

    hashes = {}
    skipped = []

    for dirpath, dirnames, filenames in os.walk(folder):

        for name in filenames:

            full_path = os.path.join(dirpath, name)
            relative = os.path.relpath(full_path, folder).replace(os.sep, "/")

            try:

                hashes[relative] = hash_file(full_path)

            except OSError:

                skipped.append(relative)

    return hashes, skipped

def compare(baseline, current):

    modified = []
    added = []
    deleted = []

    for path, current_hash in current.items():

        if path not in baseline:
            added.append(path)

        elif baseline[path] != current_hash:
            modified.append(path)

    for path in baseline:

        if path not in current:
            deleted.append(path)

    return {

        "modified": sorted(modified),
        "added": sorted(added),
        "deleted": sorted(deleted),
    }

            

def create_baseline():

    if not os.path.isdir(MONITORED_DIR):

        print(f"[ERROR] Folder not found: {MONITORED_DIR}")
        return
    
    print ("\n--- Creating Baseline ---")

    global baseline_data

    baseline_data, skipped = scan_folder(MONITORED_DIR)

    with open (BASELINE_FILE, "w") as f:

        json.dump(baseline_data, f)

    print (f"Recorded {len(baseline_data)} files")

    for name in skipped:

        print(f"[WARNING] Could not read: {name}")

def check_integrity():
    
        
    if not baseline_data:
            
        print ("\n[ERROR] No baseline data found. Create a baseline first.")
        return
    
    print ("\n--- Monitoring Directory... Press Ctrl + C to Stop ---\n")

    reported = set()

    try:
        
        while True:

            current, skipped = scan_folder(MONITORED_DIR)
            changes = compare(baseline_data, current)

            for path in changes["added"]:

                key = ("new", path)

                if key not in reported:

                    print(f"[ALERT] New file detected: {path}")
                    reported.add(key)

            for path in changes["modified"]:

                key = ("modified", path)

                if key not in reported:

                    print (f"[WARNING] File has been modified: {path}")
                    reported.add(key)

            for path in changes["deleted"]:

                key = ("deleted", path)

                if key not in reported:

                    print(f"[ALERT] File deleted: {path}")
                    reported.add(key)

            time.sleep(2)
            
    except KeyboardInterrupt:

            print ("\n--- Monitoring Stopped. Returning to Menu. ---")
                            
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

    print ("\n2. Run Integrity Check")

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
