import os
import io
import discord
from discord.ext import commands
import matplotlib.pyplot as plt
from helpers import *  # import everything from helpers.py
from keep_alive import keep_alive


bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print(f"{bot.user} is now running!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)
{}


@bot.command()
async def ping(ctx):
    await ctx.send("pong")
{}


@bot.command(name="graph")
async def graph(ctx):
    packaging = ['plastic', 'paper', 'glass', 'misc']
    mattotals = get_all_totals(packaging)

    for x in range(len(mattotals)):
        plt.bar(packaging[x], mattotals[packaging[x]])
    plt.savefig('graph.png')

    with open('graph.png', 'rb') as fh:
        f = discord.File(fh, filename="graph.png")
        await ctx.send(file=f)
{}






@bot.tree.command(name="test", description="testtt")
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("hi")
{}


@bot.tree.command(name="barchart", description="get a bar chart")
async def barchart(interaction: discord.Interaction):
    packaging = ['plastic', 'paper', 'glass', 'misc']
    mattotals = get_all_totals(packaging)

    # this makes sending files possible (without having to save them)
    img_data = io.BytesIO()

    plt.clf()  # blank graph before graphing

    for x in range(len(mattotals)):
        plt.bar(packaging[x], mattotals[packaging[x]])
        
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    f = discord.File(img_data, filename="barchart.png")

    embed = discord.Embed(
        title="Bar Chart", color=discord.Color.blurple())
    embed.set_image(
        url="attachment://barchart.png")
    embed.set_footer(
        text=rn_fancy())

    await interaction.response.send_message(embed=embed, file=f)
{}


keep_alive()
try:
    bot.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')
    os.system("python restarter.py")