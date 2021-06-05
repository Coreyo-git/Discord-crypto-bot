# Discord-crypto-bot
### Simple Discord bot that works with the coingecko public api to request data.

### Features: 
- Fetches current price of coins via discord command.
- Allows users to add coins to an update list, tracking users favorite coins.
- User Managed List of active trades, including buys/sells.
- Allows Users to input their buys/sells amount and price, if no price is specefied it pulls the current price of the coin.
- Calculates Profit/Loss on the trade after selling.

API Documentation: [Coin Gecko API](https://www.coingecko.com/en/api#explore-api)
## First Python Project.
### Commands:
> Commands are executed via the `!` symbol before commands: `!price Ethereum`

`!price <coin>`
> Checks the current price of a coin, to get the coins request check the [Coin Gecko API](https://www.coingecko.com/en/api#explore-api) for more infop

`!addcoin <coin>`
> Adds the coin to a list where it tracks prices, gives updates etc.

`!coins` 
> Shows Current List of tracked coins.

`!updates`
> Shows current coin list and prices

`!buy <coin> <amount> <price>`
> Allows users to buy coins, adding them into a trade list, if price is left blank it requests the current price.
> 
> e.g. `!buy Ethereum 20 2770.34`

`!sell <coin> <amount> <price>`
> Allows users to sell coins they've added to the active trade list via the index, which can be found via the `!trades` command, if price is left blank it requests the current price.  | Currently doesn't support amount.
> 
> e.g. `!sell 1 20 2770.34 | !sell 0`

`!trades`
> Shows a list of the active trades.

`!cleartrades`
> Clears the active trade list

A few bugs remain as this is a personal project to get farmilliar with python.
