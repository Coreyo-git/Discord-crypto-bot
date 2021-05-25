import os
import requests
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
# Watches for client message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!'):
        #Formats message to suit API Request
        input = str(message.content)
        input = input.strip("!")
        input = input.lower()

        #Requests Coin Info
        r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+input+'&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true').json()
        #await message.channel.send(r)
        data = r[input]
        usdPirce = str(data["usd"])
        dayChange = str(data["usd_24h_change"])

        #Formats string for Display
        dayChange = dayChange[0:5]
        input = input.capitalize()

        #Displays a message of the day when requesting
        badMotd = ["Sell ASAP", "HODL", "Funds are safu", "Should have brought Dogecoin...", "Feels bad...", "panik", ]
        goodMotd = ["Wait for the dump?", "BITCONNNECCCTTT", "Buy up!", "Sub to Pewdiepie"]

        good = random.randrange(len(goodMotd))
        bad = random.randrange(len(badMotd))

        await message.channel.send("> **"+input+"**" + ": **Price:** `$" + usdPirce + "` | **24 Hour Change:** `%" + dayChange + "` | MOTD: `" + badMotd[bad] + "`")


client.run(TOKEN)