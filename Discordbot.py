import os
import requests
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

coinList = ['ethereum','bitcoin']

@bot.command()
async def addcoin(ctx, coin):
    coin = coin.lower()
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+coin+'&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true').json()
    await ctx.send(r)

# Gets Coin stats from Coin List
@bot.command()
async def update(ctx):
    for coin in coinList:

        input = str(coin)
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

        await ctx.channel.send("> **"+input+"**" + ": **Price:** `$" + usdPirce + "` | **24 Hour Change:** `%" + dayChange + "`")



bot.run(TOKEN)