import sys

import talib
import datetime
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import yfinance as yf
import math
import numpy as np

def download_data(symbol, start_date, end_date):
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
    return data_df

symbol = "TQQQ"
start_date = "2021-01-30"
end_date = "2022-01-30"
data_df = download_data(symbol, start_date, end_date)

periods = [16, 32, 64]
time_shifts = [2, 4, 6, 8, 10]

def optim_func(series):

    if series["# Trades"] < 5:
         return -1

    return series["Equity Final [$]"]/ series ["Exposure Time [%]"]

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


class VelocityStrategy(Strategy):
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


#for time_shift in time_shifts:
#    add_velocity_time_shift(data_df, period, time_shift)




"""
bt = Backtest(data_df, RsiOscillator, cash=10_000)
stats = bt.optimize(
     upper_bound = range(55,85,5),
     lower_bound = range(10,45,5),
     rsi_window = range(10,30,2),
     maximize = optim_func,
     constraint = lambda param: param.upper_bound > param.lower_bound
)
"""
# bt = Backtest(data_df, WmaStrategy, cash = 10_000) # 124% return
#bt = Backtest(data_df, HmaStrategy, cash = 10_000) # 104%
bt = Backtest(data_df, VelocityStrategy, cash = 10_000) # 181%
#bt = Backtest(data_df, AccelerationStrategy, cash = 10_000) # 105%

stats = bt.run()
print(stats)
bt.plot(filename=filename)
