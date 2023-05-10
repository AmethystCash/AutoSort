import os
import io
import discord
from discord.ext import commands
from discord.ui import Select, View
import matplotlib.pyplot as plt
import asyncio
from helpers import *
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



@bot.tree.command(name="piechart", description="get a pie chart")
async def piechart(interaction: discord.Interaction):
    packaging = ['plastic', 'paper', 'glass', 'misc']
    mattotals = get_all_totals(packaging)

    # this makes sending files possible (without having to save them)
    img_data = io.BytesIO()

    plt.clf()  # blank graph before graphing

    # create the pie chart with the totals and labels
    plt.pie(list(mattotals.values()), labels=list(mattotals.keys()))

    plt.savefig(img_data, format='png')
    img_data.seek(0)
    f = discord.File(img_data, filename="piechart.png")

    embed = discord.Embed(
        title="Pie Chart", color=discord.Color.blurple())
    embed.set_image(
        url="attachment://piechart.png")
    embed.set_footer(
        text=rn_fancy())

    await interaction.response.send_message(embed=embed, file=f)



def generate_barchart(totals):
    img_data = io.BytesIO()
    plt.clf()

    plt.bar(list(totals.keys()), list(totals.values()))

    plt.savefig(img_data, format='png')
    img_data.seek(0)
    f = discord.File(img_data, filename="piechart.png")

    return f
{}


def generate_piechart(totals):
    img_data = io.BytesIO()
    plt.clf()

    plt.pie(list(totals.values()), labels=list(totals.keys()))

    plt.savefig(img_data, format='png')
    img_data.seek(0)
    f = discord.File(img_data, filename="piechart.png")

    return f
{}



charts = {
    'Bar chart': {
        'emoji': '📊',
        'short_desc': 'Representing the amounts of each material',

        'long_desc': '',
        'image_gen': lambda totals: generate_barchart(totals)
    },
    'Pie chart': {
        'emoji': '🥧',
        'short_desc': 'Representing the percentages of each material',

        'long_desc': '',
        'image_gen': lambda totals: generate_piechart(totals)
    }
}


@bot.tree.command(name="stats", description="Data collected from AutoSort in many forms")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer()  # wait for firebase
    totals = get_totals()

    embed = discord.Embed(
        title="Statistics and data visualization",
        description="Explore various statistics and performance metrics of AutoSort, our cutting-edge automated sorting system.",
        color=discord.Color.blurple())
    
    select = Select(
        placeholder="Pick a chart",
        options=[
            discord.SelectOption(
                label=option,
                emoji=charts[option]['emoji'],
                description=charts[option]['short_desc']
            ) for option in charts
        ]
    )

    view = View(timeout=60)
    view.add_item(select)

    async def my_callback(interaction):
        choice = select.values[0]
        chart = charts[choice]
        image_file = chart['image_gen'](totals)
        
        embed = discord.Embed(
            title=choice,
            description=chart['long_desc'],
            color=discord.Color.blurple())
        embed.set_image(
            url=f"attachment://{image_file.filename}")
        embed.set_footer(
            text=rn_fancy())
    
        await interaction.response.edit_message(embed=embed, attachments=[image_file], view=view)

    select.callback = my_callback

    await interaction.followup.send(embed=embed, view=view)
{}


keep_alive()
try:
    bot.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')
    os.system("python restarter.py")