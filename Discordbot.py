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
    input = str(coin)
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+coin+'&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true').json()
    data = r[input]
    usdPrice = str(data["usd"])
    if any([x in coin for x in coinList]):
        await ctx.send("Coin is already in list")
        return
    if len(usdPrice) != 0:
        coin = coin
        await ctx.send("adding " + coin + " to list!")
        coinList.append(coin)

@bot.command()
async def coins(ctx): 
    await ctx.send(coinList)

@bot.command()
async def price(ctx, coin):
    input = coin.lower()
    #Requests Coin Info
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+input+'&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true').json()        #await message.channel.send(r)
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

    await ctx.channel.send("> **"+input+"**" + ": **Price:** `$" + usdPirce + "` | **27 Hour Change:** `%" + dayChange + "` | MOTD: `" + motd[rand] + "`")


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