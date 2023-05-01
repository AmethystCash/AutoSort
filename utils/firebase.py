import firebase_admin
from firebase_admin import db
import time

cred_obj = firebase_admin.credentials.Certificate('autosort-c230c-3aa20a6e2336.json')
default_app = firebase_admin.initialize_app(
    cred_obj, 
    {'databaseURL': "https://autosort-c230c-default-rtdb.europe-west1.firebasedatabase.app"}
)
ref = db.reference("/bin1-entries")  # bin1 db location


def into_firebase(data):
    material = data['material']
    accuracy = data['certainty']
    
    most_recent = time.strftime("%X %x")  # format: hr:min:sec dd/mm/yy
    entries_len = len(ref.get())
    entry_set = {"Accuracy %": accuracy, "Time": most_recent, "Type": material}
    #test_set = {"Test": "test"}

    entry_num = entries_len
    entry_name = str(entry_num)
    ref.child(entry_name).update(entry_set)
    print(f"Firebase entries length: {entries_len}")