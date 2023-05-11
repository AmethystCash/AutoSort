from datetime import datetime
import pytz
import firebase_admin
from firebase_admin import db
import json
import os
import inflect
p = inflect.engine()


firebase_creds = json.loads(os.environ['firebase_creds'])
cred_obj = firebase_admin.credentials.Certificate(firebase_creds)
default_app = firebase_admin.initialize_app(
    cred_obj, {
        'databaseURL':
        "https://autosort-c230c-default-rtdb.europe-west1.firebasedatabase.app"
    })
ref = db.reference("/bin1-entries")


def rn_fancy():
    rn = datetime.now(pytz.timezone('Eire'))
    day = int(rn.strftime('%e'))
    nice_datetime = rn.strftime(f"%X - %B {p.ordinal(day)} %Y")
    return nice_datetime



# getting all the actually useful data from firebase
def get_all_useful_data():
    data =  list(ref.get())
    data.pop(0)   
    return data


# this function takes in the data usually provided by `get_all_useful_data`
def get_totals(data):
    # definig it inside so that it could access the data from above without leaking outside
    def get_amount(packaging):
        count = 0
        
        for item in data:
            if item['Type'] == packaging:
                count += 1
    
        # print(count)
        # print(len(list(filter(lambda p: p['Type'] == packaging, data))))
        # print(len([p['Type'] for p in data if p['Type'] == packaging]))
        # funny one-liners equivalent to the for loop
        
        return count

    packagings = ['plastic', 'paper', 'glass', 'misc']
    amounts = [get_amount(p) for p in packagings]
    joined = dict(zip(packagings, amounts))

    return joined



def get_all_totals(packaging):
    perbin = []
    mattotals = {}

    for x in range(len(packaging)):
        perbin.append(get_total(packaging[x]))
        mattotals[packaging[x]] = perbin[x]

    return mattotals


def get_total(material):
    datain = ref.get()
    # print(datain)
    count = 0

    firebase_convert = list(
        datain)  # converts to list for next line to get the object indexing
    firebase_convert.pop(0)  # removing the 0th entry of firebase

    for x in range(len(firebase_convert)):
        entry_listing = dict(
            firebase_convert[x]
        )  # converts list from before into usable dictionary to find material val per entry
        entrymatval = entry_listing['Type']
        if entrymatval == material:
            count += 1

    return count