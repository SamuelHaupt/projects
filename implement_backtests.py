import talib
import datetime
from backtesting import Backtest, Strategy 
from backtesting.lib import crossover
import pandas as pd
import yfinance as yf
import math
import numpy as np
#from risk_management import RiskData

def download_and_add_atr(symbol, start_date, end_date, periods, time_shifts):
    # Download data
    data_df = yf.download(
        tickers=symbol,
        start=start_date,
        end=end_date,
        interval='1d',
        auto_adjust=True,
        rounding=True
    )
    data_df.sort_index(ascending=True, inplace=True)
    data_df.drop_duplicates(inplace=True)

    # Calculate ATR and add to data frame
    def add_avg_true_range(data_df, period):
        data_df_index = data_df.index
        high = data_df['High']
        low = data_df['Low']
        close_previous = data_df['Close'].shift(1)
        true_range_components = pd.DataFrame(index=data_df_index)
        true_range_components["h_l"] = high - low
        true_range_components["h_c_previous"] = np.abs(high - close_previous)
        true_range_components["l_c_previous"] = np.abs(low - close_previous)
        true_range = true_range_components.max(axis=1)

        average_true_range = pd.Series(np.zeros(len(data_df)), index=data_df_index)
        average_true_range.iloc[0] = true_range.iloc[0]
        weights = np.array([1 / period, (period - 1) / period])
        for index in range(1, len(data_df)):
            tr = true_range.iloc[index]
            atr_previous = average_true_range.iloc[index - 1]
            atr_current = tr * weights[0] + atr_previous * weights[1]
            average_true_range.iloc[index] = atr_current

        data_df[f"feature_atr_{period}p"] = np.log(average_true_range)
        data_df[f"atr_{period}p"] = average_true_range

    def add_avg_true_range_time_shift(data_df, period, time_shift):
        atr_shifted = data_df[f"feature_atr_{period}p"].shift(time_shift)
        data_df[f"feature_atr_{period}p_{time_shift}ts"] = atr_shifted

    # Apply ATR functions for each period and time shift
    for period in periods:
        add_avg_true_range(data_df, period)
        for time_shift in time_shifts:
            add_avg_true_range_time_shift(data_df, period, time_shift)

    return data_df

# Define parameters

# different symbols to test back tests with
symbol = "TQQQ"
#symbol = "GOOG"
# symbol = "^GSPC"
# symbol = "MSFT"
# symbol = "BTC_USD"

# Can use different start and stop dates
# start_date = "2018-01-30"
start_date = "2021-01-30"
end_date = "2022-01-30"
#end_date = "2021-11-09"
periods = [16, 32, 64]
time_shifts = [2, 4, 6, 8, 10]

data_df = download_and_add_atr(symbol, start_date, end_date, periods, time_shifts)

def optim_func(series):
    # Penalize strategies with fewer than a set minimum number of trades
    min_trades = 5
    if series["# Trades"] < min_trades:
        return -np.inf  


    exposure_time_penalty = 1 - (series["Exposure Time [%]"] / 100)
    return series["Equity Final [$]"] * exposure_time_penalty

def calculate_hma(close_series, period):
    # WMA with period n/2 and n
    wma_half_n = close_series.rolling(window=int(period / 2)).apply(
        lambda x: np.dot(x, np.arange(1, int(period / 2) + 1)) / np.arange(1, int(period / 2) + 1).sum(), raw=True)
    wma_n = close_series.rolling(window=period).apply(
        lambda x: np.dot(x, np.arange(1, period + 1)) / np.arange(1, period + 1).sum(), raw=True)

    # HMA Calculation
    hma_intermediate = 2 * wma_half_n - wma_n
    hma = hma_intermediate.rolling(window=int(math.sqrt(period))).apply(
        lambda x: np.dot(x, np.arange(1, int(math.sqrt(period)) + 1)) / np.arange(1, int(math.sqrt(period)) + 1).sum(), raw=True)
    return hma

def weighted_moving_average(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(window=period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)


def calculate_velocity(close_series, period):
    hma = calculate_hma(close_series, period)
    velocity = hma.diff()
    return velocity


class RsiOscillator(Strategy):
       
        upper_bound = 70
        lower_bound = 30
        rsi_window = 14
        
        def init(self):
            #self.data.Close can be Open, can be any column header
            # RSI takes a price and a window of time (14)
            self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)
        
        def next(self):
            # trading logic goes here
            if crossover(self.rsi, self.upper_bound):
                 self.position.close()
            
            elif crossover(self.lower_bound, self.rsi):
                 self.buy()


class WmaStrategy(Strategy):
    period = 14 

    def init(self):
        # Convert _Array to Pandas Series
        close_series = pd.Series(self.data.Close)

        # Calculate Weighted Moving Average (WMA) on the Pandas Series
        weights = np.arange(1, self.period + 1)
        self.wma = self.I(lambda s: pd.Series(s).rolling(window=self.period).apply(
            lambda x: np.dot(x, weights) / weights.sum(), raw=True),
            close_series)

    def next(self):
        if crossover(self.data.Close, self.wma):
            self.buy()
        elif crossover(self.wma, self.data.Close):
            self.position.close()


class HmaStrategy(Strategy):
    period = 14 

    def init(self):
        close_series = pd.Series(self.data.Close)

        self.hma = self.I(calculate_hma, close_series, self.period)

    def next(self):
        if crossover(self.data.Close, self.hma):
            self.buy()
        elif crossover(self.hma, self.data.Close):
            self.position.close()


class HMAVelocityStrategy(Strategy):
    period = 14 

    def init(self):
        close_series = pd.Series(self.data.Close)
        close_log = np.log(close_series)
        
        # Calculate HMA on log of closing prices
        hma = calculate_hma(close_log, self.period)

        # Calculate velocity as the difference of HMA
        self.velocity = self.I(pd.Series.diff, hma)

    def next(self):
        if crossover(self.velocity, 0):
            self.buy()

        elif crossover(0, self.velocity):
            self.position.close()

class AccelerationStrategy(Strategy):
    period = 14  

    def init(self):
        close_series = pd.Series(self.data.Close)
        close_log = np.log(close_series)

        # Calculate velocity
        velocity = calculate_velocity(close_log, self.period)

        # Calculate acceleration as the difference of velocity
        self.acceleration = self.I(pd.Series.diff, velocity)

    def next(self):
        if crossover(self.acceleration, 0):
            self.buy()
        elif crossover(0, self.acceleration):
            self.position.close()


class ATRStrategy(Strategy):
    atr_period = 14  # Period for ATR calculation

    def init(self):
        # Extract high, low, and close as numpy arrays
        high = np.array(self.data.High)
        low = np.array(self.data.Low)
        close = np.array(self.data.Close)

        # Calculate ATR using TA-Lib
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)

    def next(self):
        # Implement your trading logic here
        if not self.position and self.data.Close[-1] > self.data.Close[-2] + self.atr[-1]:
            self.buy()
        elif self.position and self.data.Close[-1] < self.data.Close[-2] - self.atr[-1]:
            self.position.close()


class TradingBotStrategy(Strategy):
    '''Trading bot implemented as a trading streategy. Uses ATR as a buy indicator to get into the market.
    looks st standard dveiation after buys, movements ourside of 2 standard deviation are either bought more, or sold.
    Then looks at risk profile, trailing stop loss, total amount lost, and temporal risk management. 
    Sells if any of them indicate too much risk.
    '''

    n_days = 10

    def init(self):
        period = 32
        high = self.data.High
        low = self.data.Low
        close = self.data.Close
        self.initial_balance = self.equity

        # Shift the close array and prepend NaN
        close_shifted = np.roll(close, 1)
        close_shifted[0] = np.nan

        # ATR claculations
        tr1 = high - low
        tr2 = np.abs(high - close_shifted)
        tr3 = np.abs(low - close_shifted)
        true_range = pd.DataFrame({'TR1': tr1, 'TR2': tr2, 'TR3': tr3}).max(axis=1)
        self.atr = true_range.rolling(window=period, min_periods=1).mean()

        # Allows for rolling calculations in backtesting.py
        close_series = pd.Series(self.data.Close)

        # Calculate ATR and Std Dev
        self.trailing_std_dev = close_series.rolling(self.n_days).std()
        self.trailing_avg = close_series.rolling(self.n_days).mean()

        # Risk Calculation to simulate temportal stop loss
        self.entry_price = None
        self.days_since_entry = 0

        # Trailing Stop Loss
        self.peak_price = None
        self.trailing_stop_loss = 0.02  # 5% trailing stop loss

        #was yesterday a buy
        self.last_action_was_buy = False

    def next(self):
        
        # Current price of asset
        current_price = self.data.Close[-1]

        # bot is set up to use half of portfolio value on buys
        half_equity = self.equity / 2
        current_price = self.data.Close[-1] 
        num_shares_to_buy = half_equity // current_price
                        
        # Standard deviation to ensure buy was good
        reward = 0
        current_close = self.data.Close[-1]
        prev_close = self.data.Close[-2]
        
        trailing_std = self.trailing_std_dev.iloc[-1]
        trailing_avg = self.trailing_avg.iloc[-1]
        
        
        
        if len(self.data.Close) < self.n_days:
            return
                
        # Logic to calculate reward based on trailing standard deviation
        if (self.last_action_was_buy == True):
            if prev_close > trailing_avg + trailing_std:
                reward += 1
                if prev_close > trailing_avg + 2 * trailing_std:
                    reward += 10
                    if prev_close > trailing_avg + 3 * trailing_std:
                        reward += 100

            if prev_close < trailing_avg - trailing_std:
                reward -= 1
                if prev_close < trailing_avg - 2 * trailing_std:
                    reward -= 10
                    if prev_close < trailing_avg - 3 * trailing_std:
                        reward -= 100
        
            elif reward < -80 and self.position:
                print("Current Date:", self.data.index[-1]) 
                print("Negative reward triggered sale, reward less than -80")
                self.position.close()
                self.last_action_was_buy = False
            else:
                self.last_action_was_buy = False
        
        # buy signal based on atr
        if self.atr.iloc[-1] > 0.5:
            if not self.position:
                print("Shares to be bought: " + str(num_shares_to_buy))
                self.buy(size = num_shares_to_buy)
                self.last_action_was_buy = True


        # Trailing Stop Loss 
        if self.position:
            if self.entry_price is None:
                # Initialize for a new position
                self.entry_price = current_price
                self.days_since_entry = 0
                self.peak_price = current_price
            else:
                self.days_since_entry += 1
                # Update peak price only if it's not None
                if self.peak_price is not None:
                    self.peak_price = max(self.peak_price, current_price)

                # Trailing stop loss check
                if self.peak_price is not None:
                    stop_loss_price = self.peak_price * (1 - self.trailing_stop_loss)
                    if current_price <= stop_loss_price:
                        print("Current Date:", self.data.index[-1]) 
                        print(f"Trailing stop loss triggered. Selling at {current_price}, stop loss at {stop_loss_price}")
                        self.position.close()
                        self.entry_price = None
                        self.peak_price = None

        else:
            # Reset variables if there's no open position
            self.entry_price = None
            self.days_since_entry = 0
            self.peak_price = None

        # Risk Management - Temporal Stop Loss
        if self.position:
            if self.entry_price is None:
                # Store the entry price and reset the days counter when a new position is opened
                self.entry_price = current_price
                self.days_since_entry = 0
            else:
                # Increment the days counter
                self.days_since_entry += 1

                # Start checking after 3 days have passed
                if self.days_since_entry > 0:
                    required_price_increase = self.entry_price * (1 + 0.01 * (self.days_since_entry - 3))

                    # Check if the current price is less than the required price increase
                    if current_price < required_price_increase:
                        print("Current Date:", self.data.index[-1]) 
                        print(f"Closing position on Day {self.days_since_entry}: The price has not increased more than 1% per day since entry after 3 days. Current Price: {current_price}, Required Increase: {required_price_increase}")
                        self.position.close()
                        self.entry_price = None  # Reset the entry price for the next position
        else:
            # Reset entry price and days counter if there's no open position
            self.entry_price = None
            self.days_since_entry = 0


class ROCVelocityWithRisk(Strategy):
    """Another trading strategy, but uses ROC velocity to enter the market, then utilizes our custom
    risk profile to get out of the market.
    """
    
    n_days = 10
    counter = 0

    def init(self):
        period = 32
        high = self.data.High
        low = self.data.Low
        close = self.data.Close
        self.initial_balance = self.equity

        # Shift the close array and prepend NaN
        close_shifted = np.roll(close, 1)
        close_shifted[0] = np.nan

        # Allows for rolling calculations in backtesting.py
        close_series = pd.Series(self.data.Close)

        # Calculate ATR and Std Dev
        self.trailing_std_dev = close_series.rolling(self.n_days).std()
        self.trailing_avg = close_series.rolling(self.n_days).mean()

        # Risk Calculation to simulate temportal stop loss
        self.entry_price = None
        self.days_since_entry = 0

        # Trailing Stop Loss
        self.peak_price = None
        self.trailing_stop_loss = 0.02
        
        #velocity indicator
        self.roc = talib.ROC(self.data.Close, timeperiod=12)

    def next(self):
        current_price = self.data.Close[-1]

        # Check if ROC is available and not NaN
        if len(self.roc) < 13 or np.isnan(self.roc[-1]):
            return  # Skip if ROC is not yet calculable

        # Calculate the number of shares to buy
        half_equity = self.equity / 2
        if current_price > 0:
            num_shares_to_buy = half_equity / current_price
            num_shares_to_buy = max(1, int(num_shares_to_buy))  # Ensure at least one share is bought

        # Buy based on positive ROC
        if self.roc[-1] > 0 and not self.position:
            print("Current Date:", self.data.index[-1])
            print("Buying based on positive ROC (velocity). Shares to buy:", num_shares_to_buy)
            self.buy(size=num_shares_to_buy)
        
        # Risk Management - total equity loss stop loss
        if self.equity <= 0.8 * self.initial_balance:
            if self.position:
                print("Current Date:", self.data.index[-1]) 
                print("Max loss reached, closing position")
                self.position.close()

        # Trailing Stop Loss 
        if self.position:
            if self.entry_price is None:
                # Initialize for a new position
                self.entry_price = current_price
                self.days_since_entry = 0
                self.peak_price = current_price
            else:
                self.days_since_entry += 1
                # Update peak price only if it's not None
                if self.peak_price is not None:
                    self.peak_price = max(self.peak_price, current_price)

                # Trailing stop loss check
                if self.peak_price is not None:
                    stop_loss_price = self.peak_price * (1 - self.trailing_stop_loss)
                    if current_price <= stop_loss_price:
                        print("Current Date:", self.data.index[-1]) 
                        print(f"Trailing stop loss triggered. Selling at {current_price}, stop loss at {stop_loss_price}")
                        self.position.close()
                        self.entry_price = None
                        self.peak_price = None


        else:
            # Reset variables if there's no open position
            self.entry_price = None
            self.days_since_entry = 0
            self.peak_price = None

        # Risk Management - Temporal Stop Loss
        if self.position:
            if self.entry_price is None:
                # Store the entry price and reset the days counter when a new position is opened
                self.entry_price = current_price
                self.days_since_entry = 0
            else:
                # Increment the days counter
                self.days_since_entry += 1

                # Start checking after 3 days have passed
                if self.days_since_entry > 0:
                    required_price_increase = self.entry_price * (1 + 0.01 * (self.days_since_entry - 3))

                    # Check if the current price is less than the required price increase
                    if current_price < required_price_increase:
                        print("Current Date:", self.data.index[-1]) 
                        print(f"Closing position on Day {self.days_since_entry}: The price has not increased more than 1% per day since entry after 3 days. Current Price: {current_price}, Required Increase: {required_price_increase}")
                        self.position.close()
                        self.entry_price = None  # Reset the entry price for the next position
        else:
            # Reset entry price and days counter if there's no open position
            self.entry_price = None
            self.days_since_entry = 0


class HMAVelocityStrategyWithRisk(Strategy):
    """Uses Hull Moving Average as a buy indictor, then our custom risk profile for sells. High Sharpe Ratio and larger 
    returns.
    """
    
    period = 14 
    n_days = 10
    counter = 0


    def init(self):
        period = 32
        high = self.data.High
        low = self.data.Low
        close = self.data.Close
        self.initial_balance = self.equity

        # Shift the close array and prepend NaN
        close_shifted = np.roll(close, 1)
        close_shifted[0] = np.nan
        
        close_series = pd.Series(self.data.Close)
        close_log = np.log(close_series)
        
        # Calculate HMA on log of closing prices
        hma = calculate_hma(close_log, self.period)

        # Calculate velocity as the difference of HMA
        self.velocity = self.I(pd.Series.diff, hma)

        # Risk Calculation to simulate temportal stop loss
        self.entry_price = None
        self.days_since_entry = 0

        # Trailing Stop Loss
        self.peak_price = None
        self.trailing_stop_loss = 0.02

    def next(self):
        current_price = self.data.Close[-1]

        # Calculate the number of shares to buy
        half_equity = self.equity / 2
        if current_price > 0:
            num_shares_to_buy = half_equity / current_price
            num_shares_to_buy = max(1, int(num_shares_to_buy))  # Ensure at least one share is bought

        # Buy based on positive hma velocity
        if crossover(self.velocity,0) and not self.position:
            print("Current Date:", self.data.index[-1])
            print("Buying based on positive ROC (velocity). Shares to buy:", num_shares_to_buy)
            self.buy(size=num_shares_to_buy)
        
        # Risk Management - total equity loss stop loss
        if self.equity <= 0.8 * self.initial_balance:
            if self.position:
                print("Current Date:", self.data.index[-1]) 
                print("Max loss reached, closing position")
                self.position.close()

        # Trailing Stop Loss 
        if self.position:
            if self.entry_price is None:
                # Initialize for a new position
                self.entry_price = current_price
                self.days_since_entry = 0
                self.peak_price = current_price
            else:
                self.days_since_entry += 1
                # Update peak price only if it's not None
                if self.peak_price is not None:
                    self.peak_price = max(self.peak_price, current_price)

                # Trailing stop loss check
                if self.peak_price is not None:
                    stop_loss_price = self.peak_price * (1 - self.trailing_stop_loss)
                    if current_price <= stop_loss_price:
                        print("Current Date:", self.data.index[-1]) 
                        print(f"Trailing stop loss triggered. Selling at {current_price}, stop loss at {stop_loss_price}")
                        self.position.close()
                        self.entry_price = None
                        self.peak_price = None

        else:
            # Reset variables if there's no open position
            self.entry_price = None
            self.days_since_entry = 0
            self.peak_price = None

        # Risk Management - Temporal Stop Loss
        if self.position:
            if self.entry_price is None:
                # Store the entry price and reset the days counter when a new position is opened
                self.entry_price = current_price
                self.days_since_entry = 0
            else:
                # Increment the days counter
                self.days_since_entry += 1

                # Start checking after 3 days have passed
                if self.days_since_entry > 0:
                    required_price_increase = self.entry_price * (1 + 0.01 * (self.days_since_entry - 3))

                    # Check if the current price is less than the required price increase
                    if current_price < required_price_increase:
                        print("Current Date:", self.data.index[-1]) 
                        print(f"Closing position on Day {self.days_since_entry}: The price has not increased more than 1% per day since entry after 3 days. Current Price: {current_price}, Required Increase: {required_price_increase}")
                        self.position.close()
                        self.entry_price = None  # Reset the entry price for the next position
        else:
            # Reset entry price and days counter if there's no open position
            self.entry_price = None
            self.days_since_entry = 0


class BuyAndHoldStrategy(Strategy):
    def init(self):
        # No specific initialization needed for buy and hold
        pass
    
    def next(self):
        # If we don't have any open positions, we buy
        if not self.position:
            self.buy()



now = datetime.datetime.now()
formatted_datetime = now.strftime("%Y-%m-%d_%H-%M-%S")
filename = f'D:\\plots\\plt_{formatted_datetime}.html'



# This is how you run the tests

# bt = Backtest(data_df, WeightedSignalStrategy, cash = 100_000)
# stats = bt.optimize(
#     atr_weight=list(np.arange(0.5, 0.9, 0.1)),
#     std_dev_weight=list(np.arange(0.05, 0.3, 0.05)),
#     atr_period=list(range(10, 20, 2)),
#     std_dev_period=list(range(5, 15, 2)),
#     maximize='# Trades',
#     constraint=lambda params: params.atr_weight + params.std_dev_weight == 1
# )
# print(stats)
# bt.plot(filename = filename)


# bt = Backtest(data_df, TradingBotStrategy, cash=100000)
# stats = bt.run()
# print(stats)
# bt.plot(filename=filename)

# bt = Backtest(data_df, ROCVelocityWithRisk, cash=100000)
# stats = bt.run()
# print(stats)
# bt.plot(filename=filename)

# bt = Backtest(data_df, WmaStrategy, cash = 100_000) # 124% return
# stats = bt.run()
# print(stats)
# bt.plot(filename=filename)

# # bt = Backtest(data_df, HmaStrategy, cash = 100_000) # 104%

# bt = Backtest(data_df, HMAVelocityStrategy, cash = 100_000) # 181%
# stats = bt.run()
# print(stats)
# bt.plot(filename=filename)

bt = Backtest(data_df, HMAVelocityStrategyWithRisk, cash=100000)
stats = bt.run()
print(stats)
bt.plot(filename=filename)

# # bt = Backtest(data_df, AccelerationStrategy, cash = 100_000) # 105%
# # bt = Backtest(data_df,ATRStrategy, cash = 100_000) # 124% return
# bt = Backtest(data_df, BuyAndHoldStrategy, cash = 100_000)
# stats = bt.run()
# print(stats)
# bt.plot(filename=filename)



#stats = bt.optimize(
#    period = range(1,35,1),
#    maximize = "# Trades"
#)
