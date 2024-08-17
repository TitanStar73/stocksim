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

try:
    with open("portfolio.json") as f:
        portfolio = json.load(f)
    print("Welcome back to Finance Sim!! Your portfolio has been loaded.")
except FileNotFoundError:
    print("""Welcome to Finance Sim!!
    You will start of with $1000 and you can invest in stocks.""")

    portfolio = {"cash":1000}

while True:
    command = input("Enter command: ")
    if command == 'exit':
        with open("portfolio.json", "w+") as f:
            json.dump(portfolio, f)
    elif command == 'quit':
        break
    elif command in {'help','h','?'}:
        print(HELP)
        continue
    elif command in {'portfolio', 'p', 'net', 'worth'}:
        print("Portfolio:")
    elif command.split()[0] in {'buy','b'}:
        stock = command.split()[1]
        amount = int(command.split()[2])
        if amount < 0:
            print("Amount cannot be negative")
        print(f"Buying {amount} of {stock}")
    elif command.split()[0] in {'sell','s'}:
        stock = command.split()[1]
        amount = int(command.split()[2])
        if amount < 0:
            print("Amount cannot be negative")
        print(f"Selling {amount} of {stock}")
    else:
        print("Invalid command. Type 'h' for help")
        continue
