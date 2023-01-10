import pandas as pd
import yfinance as yf
import numpy as np

data = yf.Ticker('AAPL').history(period="1d", interval="5m")
# data.assign('id' = lambda x: range(1, len(x))
data.insert(0, 'id', range(1, 1 + len(data)))
data.index = data['id']

# Create a list of the different combinations of MACD parameters to test
parameters = [(12, 26, 9), (10, 20, 5), (15, 30, 10), (20, 50, 15)]

# Initialize a dictionary to store the results of the backtest for each parameter combination
results = {}

# Iterate over each parameter combination
for params in parameters:
    # Extract the individual parameter values
    fast_period, slow_period, signal_period = params
    # Calculate the MACD and signal line for each day using the given parameters
    data['macd'] = data['Close'].ewm(span=fast_period).mean() - data['Close'].ewm(span=slow_period).mean()
    data['signal'] = data['macd'].ewm(span=signal_period).mean()

    # Initialize a variable to store the total profit made using this parameter combination
    total_profit = buy_price = sell_price = profit = 0

    # Iterate over each day in the data
    for i in range(1, len(data)):
        # If the MACD crosses above the signal line, buy the security
        if data.loc[i, 'macd'] > data.loc[i, 'signal'] and data.loc[i - 1, 'macd'] <= data.loc[i - 1, 'signal']:
            buy_price = data.loc[i, 'Close']

        # If the MACD crosses below the signal line, sell the security
        elif data.loc[i, 'macd'] < data.loc[i, 'signal'] and data.loc[i - 1, 'macd'] >= data.loc[i - 1, 'signal']:
            sell_price = data.loc[i, 'Close']
            profit = sell_price - buy_price
            total_profit += profit

    # Store the total profit made using this parameter combination in the results dictionary
    results[params] = total_profit

# Find the parameter combination that resulted in the highest total profit
best_params = max(results, key=results.get)

# Print the best parameters and the corresponding total profit
print("Best parameters:", best_params)
print("Total profit:", results[best_params])
