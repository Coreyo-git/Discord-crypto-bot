import os
from discord.embeds import Embed
import requests
import random
import discord
import pickle
from dotenv import load_dotenv
from discord.ext import commands




load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

with open('coinList', 'rb') as filehandle:
    # read the data as binary data stream
    coinList = pickle.load(filehandle)

with open('memeList', 'rb') as filehandle:
    # read the data as binary data stream
    memeList = pickle.load(filehandle)


# Adds coin to coinList with !add coin
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
        #Dump Coin to list for persistance past shutdown
        with open('coinList', 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(coinList, filehandle)

# print the coin list to the channel
@bot.command()
async def coins(ctx): 
    await ctx.send(coinList)

# Prints the price of a coin with the MOTD
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

    await ctx.channel.send("> **"+input+"**" + ": **Price:** `$" + usdPirce + "` | **24 Hour Change:** `%" + dayChange + "` | MOTD: `" + motd[rand] + "`")



# Gets Coin stats from Coin List
@bot.command()
async def updates(ctx):
    updateList = []
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
        respone = "> **"+input+"**" + ": **Price:** \t`$" + usdPirce + "` \t| **24 Hour Change:** \t`%" + dayChange + "`\n"
        updateList.append(str(respone))
        #await ctx.channel.send("> **"+input+"**" + ": **Price:** \t`$" + usdPirce + "` \t| **24 Hour Change:** \t`%" + dayChange + "`")
    updates=''.join(updateList)
    await ctx.channel.send(updates)

    #rand = random.randrange(len(memeList))
    #await ctx.channel.send(memeList[rand])

@bot.command()
async def addmeme(ctx, meme):
    addedmeme = str(meme)
    if any([str(i) in str(addedmeme) for i in memeList]):
        await ctx.send("meme is already in list")
        return

    await ctx.send("adding meme to list!")
    memeList.append(addedmeme)
    #Dump Coin to list for persistance past shutdown
    with open('memeList', 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(memeList, filehandle)

bot.run(TOKEN)