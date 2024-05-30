import telebot
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

stocks = ['NHPC.NS','SJVN.NS', 'YESBANK.NS','IREDA.NS','SUZLON.NS','HFCL.NS','RPOWER.NS','PAYTM.NS','IDEA.NS','MUTHOOTMF.NS','ATGL.NS','COALINDIA.NS','IOC.NS','ONGC.NS']

API_KEY = 'Your_API'


bot = telebot.TeleBot(API_KEY)
print('Bot has been started')

@bot.message_handler(commands=['THANKS'])
def thanks(message):
    bot.reply_to(message, "Glad I could help you!")


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, "Hello! I am Market Gyani aka Kp's bot.\nYou can use the following commands:\n1. /MTG = to know the top 3 most gainer stocks.\n2. /MTL = to know the top 3 most losers stocks.\n3. /MMV = to know the top 3 most popular stocks.\n4. /PRICE = to check the current price of any stock.\n5./Addstock = to add stock in the watchlist.\n6. /THANKS = if you want to appreciate the bot\n7. /BYE = to exit the chat")

@bot.message_handler(commands=['BYE'])
def bye(message):
    bot.reply_to(message, "Bye. See you around later :)")

def top_gain(stocks, top_n=3):
    top_stocks = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='10d', interval='1d')
        if not data.empty:
            closing_prices = data['Close']
            price_percentage_change = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100
            top_stocks.append((stock, price_percentage_change))
    top_stocks.sort(key=lambda x: x[1], reverse=True)
    return top_stocks[:top_n]

def get_highest_price_percentage_loss(stocks, top_n=3):
    top_losers = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='10d', interval='1d')
        if not data.empty:
            closing_prices = data['Close']
            price_percentage_change = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100
            top_losers.append((stock, price_percentage_change))
    top_losers.sort(key=lambda x: x[1])
    return top_losers[:top_n]

def top_volume(stocks, top_n=3):
    top_stocks = []
    for stock in stocks:
        data = yf.download(tickers=stock, period='10d', interval='1d')
        if not data.empty:
            volumes = data['Volume']
            avg_volume = volumes.mean()
            top_stocks.append((stock, avg_volume))
    top_stocks.sort(key=lambda x: x[1], reverse=True)
    return top_stocks[:top_n]

def generate_graph(stock_data, stock_name):
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data.index, stock_data['Close'], label='Close Price', color='blue')
    plt.title(f'Stock Price for {stock_name.rsplit(".NS",1)[0]}')
    plt.xlabel('Date')
    plt.ylabel('Price (INR)')
    plt.legend()
    image_path = f"{stock_name}.png"
    plt.savefig(image_path)
    plt.close()
    return image_path

@bot.message_handler(commands=['MTG'])
def handle_mtg(message):
    top_stocks = top_gain(stocks, top_n=3)
    if top_stocks:
        response = "Top 3 stocks with the highest percentage price change over the past 10 days:\n"
        for i, (stock, percentage_change) in enumerate(top_stocks, start=1):
            stock_name = stock.rsplit('.NS', 1)[0]
            response += f"{i}. {stock_name}: Percentage change of {percentage_change:.2f}%\n"
        bot.send_message(message.chat.id, response)

        top_gainer_data = {}
        for stock, _ in top_stocks:
            data = yf.download(tickers=stock, period='10d', interval='1d')
            if not data.empty:
                top_gainer_data[stock] = data

        combined_percentage_change = pd.DataFrame()
        for stock, data in top_gainer_data.items():
            percentage_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
            combined_percentage_change[stock] = [percentage_change]

        plt.figure(figsize=(10, 6))
        for stock in combined_percentage_change.columns:
            plt.bar(stock.rsplit('.NS', 1)[0], combined_percentage_change[stock].values[0], label=stock.rsplit('.NS', 1)[0])
        plt.title('Comparison of Top 3 Gainers (Percentage Change)')
        plt.ylabel('Percentage Change (%)')
        plt.legend()
        image_path = "top_gainers_percentage_change.png"
        plt.savefig(image_path)
        plt.close()
        
        bot.send_photo(message.chat.id, open(image_path, 'rb'))
        os.remove(image_path)
    else:
        bot.send_message(message.chat.id, "Failed to fetch data for stocks.")

@bot.message_handler(commands=['MTL'])
def handle_mtl(message):
    top_losers = get_highest_price_percentage_loss(stocks, top_n=3)
    if top_losers:
        response = "Top 3 stocks with the lowest percentage price change over the past 10 days:\n"
        for i, (stock, percentage_change) in enumerate(top_losers, start=1):
            stock_name = stock.rsplit('.NS', 1)[0]
            response += f"{i}. {stock_name}: Percentage change of {percentage_change:.2f}%\n"
        bot.send_message(message.chat.id, response)

        top_loser_data = {}
        for stock, _ in top_losers:
            data = yf.download(tickers=stock, period='10d', interval='1d')
            if not data.empty:
                top_loser_data[stock] = data

        combined_percentage_change = pd.DataFrame()
        for stock, data in top_loser_data.items():
            percentage_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100
            combined_percentage_change[stock] = [percentage_change]

        plt.figure(figsize=(10, 6))
        for stock in combined_percentage_change.columns:
            plt.bar(stock.rsplit('.NS', 1)[0], combined_percentage_change[stock].values[0], label=stock.rsplit('.NS', 1)[0])
        plt.title('Comparison of Top 3 Losers (Percentage Change)')
        plt.ylabel('Percentage Change (%)')
        plt.legend()
        image_path = "top_losers_percentage_change.png"
        plt.savefig(image_path)
        plt.close()

        bot.send_photo(message.chat.id, open(image_path, 'rb'))
        os.remove(image_path)
    else:
        bot.send_message(message.chat.id, "Failed to fetch data for stocks.")

@bot.message_handler(commands=['MMV'])
def handle_mmv(message):
    top_stocks = top_volume(stocks, top_n=3)
    if top_stocks:
        response = "Top 3 stocks with the highest volume over the past 10 days:\n"
        for i, (stock, volume) in enumerate(top_stocks, start=1):
            stock_name = stock.rsplit('.NS', 1)[0]
            response += f"{i}. {stock_name}: Average volume = {volume}\n"
        bot.send_message(message.chat.id, response)

        top_volume_data = {}
        for stock, _ in top_stocks:
            data = yf.download(tickers=stock, period='10d', interval='1d')
            if not data.empty:
                top_volume_data[stock] = data

        plt.figure(figsize=(10, 6))
        for stock, data in top_volume_data.items():
            plt.plot(data.index, data['Volume'], label=stock.rsplit('.NS', 1)[0])
        plt.title('Comparison of Top 3 Volume Stocks')
        plt.xlabel('Date')
        plt.ylabel('Volume')
        plt.legend()
        image_path = "top_volume_stocks.png"
        plt.savefig(image_path)
        plt.close()

        bot.send_photo(message.chat.id, open(image_path, 'rb'))
        os.remove(image_path)
    else:
        bot.send_message(message.chat.id, "Failed to fetch data for stocks.")

@bot.message_handler(commands=['PRICE'])
def handle_price(message):
    bot.send_message(message.chat.id, "Enter the name of the Stock (e.g., NHPC):")
    bot.register_next_step_handler(message, process_stock_name)

def process_stock_name(message):
    stock_name = message.text.strip().upper() + '.NS'
    if len(stock_name) < 2:
        bot.send_message(message.chat.id, "Invalid Stock")
    else:
        data = yf.download(tickers=stock_name, period='1d', interval='1m')
        data1 = yf.download(tickers=stock_name, period='1d', interval='30m')
        if not data.empty:
            data = data.reset_index()
            data["format_date"] = data['Datetime'].dt.strftime('%d/%m%I:%M%p')
            data.set_index('format_date', inplace=True)
            image_path = generate_graph(data, stock_name)
            bot.send_message(message.chat.id, data1['Close'].to_string(header=True))
            bot.send_photo(message.chat.id, open(image_path, 'rb'))
            os.remove(image_path) 
        else:
            bot.send_message(message.chat.id, "No data found.")

@bot.message_handler(commands=['Addstock'])
def handle_price(message):
    bot.send_message(message.chat.id, "Enter the name of the Stock (e.g., NHPC):")
    bot.register_next_step_handler(message, Add_stock)

def Add_stock(message):
    stock_name = message.text.strip().upper() + '.NS'
    data = yf.download(tickers=stock_name, period='1d', interval='1m')
    if not data.empty:
        stocks.append(stock_name)
        bot.send_message(message.chat.id, "Added successfully")
    else:
        bot.send_message(message.chat.id, "Stock name is not found.")
    print(stocks)

bot.polling()
