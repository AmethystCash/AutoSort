import os
import discord
from discord.ext import commands
from discord.ui import View
from firebase import *
from charts import charts
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


class StatsView(View):
    def __init__(self, data):
        super().__init__(timeout=60)
        self.data = data
        self.message = None  # to keep track of the correct message
    
    @discord.ui.select(
        placeholder="Pick a chart",
        options=[
            discord.SelectOption(
                label=option,
                emoji=charts[option]['emoji'],
                description=charts[option]['short_desc']
            ) for option in charts
        ]
    )
    async def select_callback(self, interaction, select):
        choice = select.values[0]
        chart = charts[choice]
        image = chart['image_gen'](self.data)
        image_file = discord.File(image, filename="chart.png")
        
        embed = discord.Embed(
            title=choice,
            description=chart['long_desc'],
            color=discord.Color.blurple())
        embed.set_image(
            url=f"attachment://{image_file.filename}")
        embed.set_footer(
            text=rn_fancy())
    
        await interaction.response.edit_message(embed=embed, attachments=[image_file], view=self)

    async def on_timeout(self):
        for item in self.children:
            item.disabled = True

        await self.message.edit(view=self)

        
@bot.tree.command(name="stats", description="Data collected from AutoSort in many forms")
async def stats(interaction: discord.Interaction):
    await interaction.response.defer()  # wait because...
    data = get_all_useful_data()        # because firebase

    view = StatsView(data)

    embed = discord.Embed(
        title="Statistics and data visualization",
        description="Explore various statistics and performance metrics of AutoSort, our cutting-edge automated sorting system.",
        color=discord.Color.blurple())
    
    message = await interaction.followup.send(view=view, embed=embed)
    view.message = message


keep_alive()
try:
    bot.run(os.environ['TOKEN'])
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system('kill 1')
    os.system("python restarter.py")
