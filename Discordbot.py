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

# Class for Trades, stored in a list.
class Trade:
    def __init__(self, userId, user, coin, amount,price):
        self.userId = userId
        self.user = user
        self.coin = coin
        self.amount = amount
        self.price = price
        
tradeList = []

#with open('memeList', 'rb') as filehandle:
#    # read the data as binary data stream
#    memeList = pickle.load(filehandle)

# Reusable API Request
def request(coin):
    input = str(coin.lower()) # converts to string a removes capitals to satisfy api
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids='+input+'&vs_currencies=usd&include_market_cap=true&include_24hr_vol=true&include_24hr_change=true&include_last_updated_at=true').json()

    data = r[input] # stores API response DATA for Enumeration
    usdPrice = str(data["usd"]) # Stores USD Price
    dayChange = str(data["usd_24h_change"]) # Stores % Change

    #Formats string for Display
    dayChange = dayChange[0:5]
    input = coin.capitalize()

    return input, usdPrice, dayChange

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


# Tracks Who bought what for what amount
@bot.command()
async def buy(ctx, coin, amount, price="0"):
    # Pulls Author name and stores username
    user = ctx.message.author 
    user_name = user.name
    user_id = user.id
    #await ctx.channel.send("{} is your name".format(ctx.message.author.mention))
    input, usdPrice, dayChange = request(coin)
    if len(input) != 0:
        if float(price) > 0:
            tradeList.append(Trade(user_id, user_name, input, amount, float(price)))
            await ctx.channel.send(user_name + " | Bought: " + input + " | Amount: " + amount + " | for: $" + price)
        
        else:
            tradeList.append(Trade(user_id, user_name, input, amount, usdPrice))
            await ctx.channel.send(user_name + " | Bought: " + input + " | Amount:" + amount + " | for: $" + usdPrice)
    
    return
    # await ctx.channel.send(input + usdPrice + dayChange) # test line 
    

# Tracks sold coins
@bot.command()
async def sell(ctx, id, price="0"):

    user = ctx.message.author 
    user_name = user.name
    user_id = user.id

    id = int(id)
    for index, trade in enumerate(tradeList):
        if index == id:
            break
        currentTrade = tradeList[id]
        
        if user_name == format(currentTrade.user):
            await ctx.channel.send("**are you sure you want to sell " + str(id) + "?**  `[Y/N]`")
        
            await ctx.channel.send('ID: ' + str(index) + ' | User: **{}** | Coin : **{}** | Amount : **#{}** | Price : **${}**'.format(currentTrade.user, currentTrade.coin, currentTrade.amount,currentTrade.price))
            #Waites for user choice
            reply = await bot.wait_for('message', timeout=30)
            if reply.author == user:
                if reply.content == "y" or "Y":
                    input, usdPrice, dayChange = request(format(currentTrade.coin))
                    buyPrice = format(currentTrade.price)
                    amount = format(currentTrade.amount)

                    if price != "0":
                        # lazy copy and paste sorry :P 
                        now = float(price)
                        buy = float(buyPrice)
                        currentAmount = float(amount)

                        if buy > now: # Not sure about this, tired as :P
                            difference = buy - now
                        else:
                            difference = now - buy
                        total = difference * currentAmount
                        diff = str(total)

                        tradeList.pop(id)
                        await ctx.channel.send("Sold with a difference of: **$" + diff[0:6] + "** | Bought in at: **$" + str(buyPrice) + "** | the sold price is: **$" + str(now) +"**")
                        return
                    now = float(usdPrice)
                    buy = float(buyPrice)
                    currentAmount = float(amount)

                    if buy > now: # Not sure about this, tired as :P
                        difference = buy - now
                    else:
                        difference = now - buy
                    total = difference * currentAmount
                    diff = str(total)

                    tradeList.pop(id)
                    await ctx.channel.send("Sold with a difference of: **$" + diff[0:6] + "** | Bought in at: **$" + str(buyPrice) + "** | the current price is: **$" + usdPrice[0:9] +"**")
                else:
                    return
        else:
            await ctx.channel.send("No ID matches your input, `!sell <ID>`")

# Checks active trades
@bot.command()
async def ttrades(ctx):
    if len(tradeList) > 0:
        for index, trade in enumerate(tradeList):
            await ctx.channel.send('ID: ' + str(index) + ' | User: **{}** | Coin : **{}** | Amount : **#{}** | Price : **${}**'.format(trade.user, trade.coin, trade.amount,trade.price))
    else:
        await ctx.channel.send("No Active Trades")
# clears active trades
@bot.command()
async def cleartrades(ctx):
    await ctx.channel.send("Clearing active trades")


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
        #await ctx.channel.send(r)
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


#@bot.command()
#async def addmeme(ctx, meme):
#    addedmeme = str(meme)
#    if any([str(i) in str(addedmeme) for i in memeList]):
#        await ctx.send("meme is already in list")
#        return

#    await ctx.send("adding meme to list!")
#    memeList.append(addedmeme)
#    #Dump Coin to list for persistance past shutdown
#    with open('memeList', 'wb') as filehandle:
#        # store the data as binary data stream
#        pickle.dump(memeList, filehandle)

bot.run(TOKEN)