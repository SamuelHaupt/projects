# flake8: noqa
# import gymnasium as gym
import pandas as pd
import yfinance as yf
import os
# import gym_trading_env

from datetime import date
from datetime import timedelta

class YFDownloader():

    def __init__(self) -> None:
        self.symbol = None
        self.start_date = None
        self.end_date = None
    
    def download_data_df(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """_summary_

        Args:
            symbol (str): asset symbol on yfinance
            start_date (str): standard form is '2021-01-30'
            end_date (str): standard form is '2021-02-01'

        Returns:
            pd.DataFrame: Dataframe for requested symbol
        """

        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        time_interval = '1d'

        # download and save the data to pandas DataFrame
        data_df = yf.download(
            tickers = self.symbol,
            start=self.start_date,
            end=self.end_date,
            interval=time_interval,
            auto_adjust=True,  # overwrites adj_close values to close column
            rounding=True)  # rounds to two decimals
        data_df.sort_index(ascending=True, inplace=True)
        data_df.drop_duplicates(inplace=True)

        return data_df

    def clean_data(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Cleans data by using SPY's Close non-Nan, rather than grabbing
        New York Stock Exchanges trading days. This is a workaround to 
        simply the amount of libraries required to clean data. ffill and bfill
        are applied to normalize data.

        Args:
            data_df (pd.DataFrame): DataFrame to clean

        Returns:
            pd.DataFrame: Cleansed data with ffill and bfill applied
        """
        spy = self.download_data_df('SPY', self.start_date, self.end_date)
        spy.dropna(subset='Close', inplace=True)
        spy.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
        
        # use trading days from SPY to clean data.
        new_df = spy.join(data_df, how='left')

        # fill Dataframe forwards or backwards to normalize values.
        new_df.ffill(inplace=True)
        new_df.bfill(inplace=True)

        return new_df


if __name__ == "__main__":
    yf_downloader = YFDownloader()
    symbol = 'SPY'
    start_date = '2021-01-30'
    stop_date = '2022-01-30'
    data_df = yf_downloader.download_data_df(symbol, start_date, stop_date)
    clean_data_df = yf_downloader.clean_data(data_df)
