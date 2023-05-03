import os
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
import time
import firebase_admin
from firebase_admin import db
from keepalive import keep_alive

cred_obj = firebase_admin.credentials.Certificate('autosort-c230c-3aa20a6e2336.json')
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': "https://autosort-c230c-default-rtdb.europe-west1.firebasedatabase.app"})
ref = db.reference("/bin1-entries")

packaging = ['plastic', 'paper', 'glass', 'misc']
def BotTest(packaging):
    
    perbin = []
    mattotals = {}
    for x in range(len(packaging)):
        perbin.append(BotTest2(packaging[x]))
        mattotals[packaging[x]] = perbin[x]
    return mattotals
def BotTest2(vlad):
    datain = ref.get()
    #print(datain)
    count = 0

    firebase_convert = list(datain) # converts to list for next line to get the object indexing
    firebase_convert.pop(0) #removing the 0th entry of firebase
    for x in range(len(datain)-1): # -1 due to removing blank 0th entry
        entry_listing = dict(firebase_convert[x]) # converts list from before into usable dictionary to find material val per entry
        entrymatval = entry_listing['Type']
        if entrymatval == vlad:
            count+=1

    return count 



bot = commands.Bot(command_prefix="=", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is connected to Discord")

@bot.command(name="hello") #when in text chat, type '=hello' to execute the bot command
async def hello_com(ctx):
    await ctx.send("hullo")

@bot.command(name="tester", help="tests for iot proj")
async def tester(ctx):
    with open('packaging.txt', 'r') as file:
        msg_test = file.read()
        await ctx.send(msg_test)

@bot.command(name="graph")
async def grapher(ctx):
    mattotals = BotTest(packaging)
    for x in range(len(mattotals)):
        plt.bar(packaging[x], mattotals[packaging[x]])
    plt.savefig('graph.png')
    with open('graph.png', 'rb') as fh:
        f = discord.File(fh, filename="graph.png")
        await ctx.send(file=f)


my_secret = os.environ['dcbotkey']
bot.run(my_secret)

keep_alive()
try:
    bot.run(my_secret)
except discord.errors.HTTPException:
    print("Rate limited, restarting now")
    os.system('kill 1')
    os.system("python restarter.py")
