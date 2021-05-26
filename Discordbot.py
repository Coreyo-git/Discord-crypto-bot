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

        if input.__contains__('addcoin'):
            await message.channel.send("testing add coin")
            return

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

        # Checks if 24 hour change contains - or not
        if dayChange.__contains__('-'):
            motd = ["Sell ASAP", "HODL", "Funds are safu", "Should have brought Dogecoin...", "Feels bad...", "panik", "Diamond hands brotha", "Do u kno da wae?", "Crack Open The Crackers bro, you're eating cheap tonight"]
            bad = random.randrange(len(badMotd))
            rand = bad
        else:
            motd = ["Wait for the dump?", "BITCONNNECCCTTT", "Buy up!", "Sub to Pewdiepie","Can't hurt to sell bro..","Nice One Bruv", "Fuck yeah bro", "Chicken Dinner?", "Up the dog!", "Nice 1 bruva"]
            good = random.randrange(len(goodMotd))
            rand = good

        await message.channel.send("> **"+input+"**" + ": **Price:** `$" + usdPirce + "` | **27 Hour Change:** `%" + dayChange + "` | MOTD: `" + motd[rand] + "`")


client.run(TOKEN)
