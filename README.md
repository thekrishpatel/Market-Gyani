# Market Gyani Bot

Market Gyani is a Telegram bot that helps users stay informed about the stock market by providing updates on the top gainers, top losers, and the most popular stocks. The bot can also provide current stock prices and allows users to add stocks to their watchlist.

## Features

- **Top Gainers**: Get the top 3 stocks with the highest percentage price change over the past 10 days.
- **Top Losers**: Get the top 3 stocks with the lowest percentage price change over the past 10 days.
- **Most Popular**: Get the top 3 stocks with the highest trading volume over the past 10 days.
- **Stock Price**: Check the current price of any stock.
- **Add Stock**: Add a stock to the watchlist.
- **Appreciation**: Send a thank you message to the bot.
- **Exit**: Exit the chat with the bot.

## Commands

- `/start`: Start interacting with the bot and see available commands.
- `/MTG`: Get the top 3 most gainer stocks.
- `/MTL`: Get the top 3 most losers stocks.
- `/MMV`: Get the top 3 most popular stocks.
- `/PRICE`: Check the current price of any stock.
- `/Addstock`: Add a stock to the watchlist.
- `/THANKS`: Appreciate the bot.
- `/BYE`: Exit the chat with the bot.

## Requirements

- Python 3.6+
- Libraries:
  - `telebot`
  - `yfinance`
  - `pandas`
  - `matplotlib`

## Installation

1. Clone the repository:

```sh
git clone https://github.com/thekrishpatel/Market-Gyani
cd Market-Gyani/Python_individual
```

2. Install the required libraries:

```sh
pip install -r requirements.txt
```

3. Set your Telegram Bot API key in the script:

```python
API_KEY = 'YOUR_TELEGRAM_BOT_API_KEY'
```

4. Run the bot:

```sh
python bot.py
```

## Usage

Start a chat with your bot on Telegram and use the commands listed above to interact with it. The bot will provide you with information about the stock market based on the command you use.

## Functions

### `top_gain(stocks, top_n=3)`

Fetches the top `top_n` stocks with the highest percentage price change over the past 10 days.

### `get_highest_price_percentage_loss(stocks, top_n=3)`

Fetches the top `top_n` stocks with the lowest percentage price change over the past 10 days.

### `top_volume(stocks, top_n=3)`

Fetches the top `top_n` stocks with the highest trading volume over the past 10 days.

### `generate_graph(stock_data, stock_name)`

Generates a graph of the stock prices and saves it as an image.

### `handle_mtg(message)`

Handles the `/MTG` command.

### `handle_mtl(message)`

Handles the `/MTL` command.

### `handle_mmv(message)`

Handles the `/MMV` command.

### `handle_price(message)`

Handles the `/PRICE` command.

### `process_stock_name(message)`

Processes the stock name entered by the user for the `/PRICE` command.

### `handle_add_stock(message)`

Handles the `/Addstock` command.

### `add_stock(message)`

Adds a stock to the watchlist.

## Contributing

Feel free to submit issues and enhancement requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Reference

For a detailed explanation of the bot's functionality and usage, please refer to the attached PowerPoint presentation (`Python_individual.pptx`).
