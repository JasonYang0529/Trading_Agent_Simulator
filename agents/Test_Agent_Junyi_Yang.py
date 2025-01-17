def decide_trades_ma(current_data, cash, holdings, short_window=5, long_window=20, max_units=1):
   
    decisions = {}

    for stock in current_data.columns:
        # Ensure there is enough data for both moving averages
        if len(current_data) < long_window:
            continue

        # Calculate moving averages
        short_ma = current_data[stock].rolling(window=short_window).mean().iloc[-1]
        long_ma = current_data[stock].rolling(window=long_window).mean().iloc[-1]

        # Current price
        current_price = current_data[stock].iloc[-1]

        # Decision logic
        if short_ma > long_ma:  # Buy signal
            if current_price > 0:  # Ensure the price is valid
                quantity_to_buy = min(max_units, cash // current_price)
                if quantity_to_buy > 0:
                    decisions[stock] = ("buy", quantity_to_buy)
        elif short_ma < long_ma:  # Sell signal
            if stock in holdings and holdings[stock] > 0:
                quantity_to_sell = min(max_units, holdings[stock])
                if quantity_to_sell > 0:
                    decisions[stock] = ("sell", quantity_to_sell)

    return decisions
