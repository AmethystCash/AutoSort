import firebase_admin
from firebase_admin import db
from colorama import Fore, Back, Style

# TODO:
# add a proper setup func

try:
    cred_obj = firebase_admin.credentials.Certificate('autosort-c230c-3aa20a6e2336.json')
    default_app = firebase_admin.initialize_app(
        cred_obj, 
        {'databaseURL': "https://autosort-c230c-default-rtdb.europe-west1.firebasedatabase.app"}
    )
    ref = db.reference("/bin1-entries")  # bin1 db location
except:
    ref = None
    print(Fore.RED + "Couldn't connect to Firebase" + Style.RESET_ALL)


def into_firebase(data):
    if ref is None:
        print(Fore.RED + "Firebase is not connected" + Style.RESET_ALL)
        return
    
    material = data['material']
    accuracy = data['certainty']
    most_recent = data['datetime']
    
    entries_len = len(ref.get())
    entry_set = {"Accuracy %": accuracy, "Time": most_recent, "Type": material}
    # test_set = {"Test": "test"}

    entry_name = str(entries_len)
    ref.child(entry_name).update(entry_set)
    # print(f"Firebase entries length: {entries_len}")
    
    print(Fore.GREEN + "Firebase entry added successfully" + Style.RESET_ALL)