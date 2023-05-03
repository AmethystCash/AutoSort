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


def get_all_totals(packaging):
    perbin = []
    mattotals = {}

    for x in range(len(packaging)):
        perbin.append(get_total(packaging[x]))
        mattotals[packaging[x]] = perbin[x]

    return mattotals
{}


def get_total(material):
    datain = ref.get()
    # print(datain)
    count = 0

    firebase_convert = list(
        datain)  # converts to list for next line to get the object indexing
    firebase_convert.pop(0)  #removing the 0th entry of firebase

    for x in range(len(datain) - 1):  # -1 due to removing blank 0th entry
        entry_listing = dict(
            firebase_convert[x]
        )  # converts list from before into usable dictionary to find material val per entry
        entrymatval = entry_listing['Type']
        if entrymatval == material:
            count += 1

    return count
{}


def rn_fancy():
    rn = datetime.now(pytz.timezone('Eire'))
    day = int(rn.strftime('%e'))
    nice_datetime = rn.strftime(f"%X - %B {p.ordinal(day)} %Y")
    return nice_datetime
{}