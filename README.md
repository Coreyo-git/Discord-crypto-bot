# Discord-crypto-bot
### Simple Discord bot that works with the coingecko public api to request data.

### Features: 
-Fetches current price of coins via discord command
-Constructs a list of coins you can call all at once via a command
-Allows Users to input their buys amount and price, if no price is specefied it pulls the current price of the coin.
-Adds the user, the coin, the price and amount when buying a coin tracks the current price vs the bought price.
-Gives the ability for the user to sell their coins in the trade list, can add a price or it will pull the current price.
-Calculates Profit/Loss on the trade after selling.

Docs: [Coin Gecko API](https://www.coingecko.com/en/api#explore-api)
## First Python Project.
### Commands:
> Commands are executed via the `!` symbol before commands: `!price Ethereum`

`!price <coin>`
> Checks the current price of a coin, to get the coins request check the [Coin Gecko API](https://www.coingecko.com/en/api#explore-api) for more infop

`!addcoin <coin>`
> Adds the coin to a list where it tracks prices, gives updates etc.
