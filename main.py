BROKERAGE_FEE = 1 # In percentage

HELP = """
Commands:
    - buy <stock> <amount>
    - sell <stock> <amount>
    - portfolio

This sim uses realtime data so you can use any stock on NYSE
      
Need to take a break? Type 'exit' to exit the sim. We will save your portfolio for you in portfolio.json
Want to start afresh? Type 'quit' to delete your portfolio and start afresh (this will not delete your portfolio.json file but will stop the program without creating a new one)

Need to see this again? Type 'help' or 'h' or '?'
"""

import json
import requests

def get_stock_price(symbol):
    url = f"https://finance.yahoo.com/quote/{symbol}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        start = html.find('data-field="regularMarketPreviousClose" class="yf-tx3nkj">') + 58
        end = html.find('</fin-streamer>', start)
        if len(html[start:end]) > 30:
            return None
        price = float(html[start:end])
        return price
    else:
        return -1

try:
    with open("portfolio.json") as f:
        portfolio = json.load(f)
    print("Welcome back to Finance Sim!! Your portfolio has been loaded.")
except FileNotFoundError:
    print("""Welcome to Finance Sim!!
    You will start of with $1000 and you can invest in stocks.""")

    portfolio = {"cash":1000}

while True:
    try:
        command = input("Enter command: ")
        if command == 'exit':
            with open("portfolio.json", "w+") as f:
                json.dump(portfolio, f)
            break
        elif command == 'quit':
            break
        elif command in {'help','h','?'}:
            print(HELP)
            continue
        elif command in {'portfolio', 'p', 'net', 'worth'}:
            print(f"Portfolio: {portfolio}")

        elif command.split()[0] in {'buy','b'}:
            stock = command.split()[1]
            amount = int(command.split()[2])
            if amount < 0:
                print("Amount cannot be negative")
                continue

            price = get_stock_price(stock)
            if price == None:
                print("Invalid stock symbol")
                continue
            if price == -1:
                print("ERROR: Could not get stock price. Please try again later")
                continue

            price *= (1+(BROKERAGE_FEE/100))

            if portfolio["cash"] < price*amount:
                print(f"You do not have enough cash to buy this stock. The most you can buy is {portfolio['cash']//price} stock(s)")
                continue

            print(f"Buying {amount} of {stock} for ${price*amount}")
            if stock not in portfolio:
                portfolio[stock] = 0
            portfolio[stock] += amount
            portfolio["cash"] -= price*amount

        elif command.split()[0] in {'sell','s'}:
            stock = command.split()[1]
            amount = int(command.split()[2])
            if amount < 0:
                print("Amount cannot be negative")
                continue
            try:
                portfolio[stock]
            except KeyError:
                print("You do not own this stock")
                continue

            if amount > portfolio[stock]:
                print(f"You do not have enough stocks to sell. {portfolio[stock]} stocks available")
                continue
            
            price = get_stock_price(stock)
            if price == None:
                print("Invalid stock symbol")
                continue
            if price == -1:
                print("ERROR: Could not get stock price. Please try again later")
                continue
            
            price *= (1-(BROKERAGE_FEE/100))
            portfolio[stock] -= amount
            portfolio["cash"] += price*amount
            print(f"Selling {amount} of {stock}. Received ${price*amount} for {amount} of {stock}")
            
        else:
            print("Invalid command. Type 'h' for help")
            continue
    except:
        pass
