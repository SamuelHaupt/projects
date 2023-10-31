"""
Preprocessor module for data downloaded. Cleans data and adds
indicators.
"""

import pandas as pd
import yfinance as yf
import numpy as np
import math


class DataProcessor():

    def __init__(self) -> None:
        self.symbol = None
        self.start_date = None
        self.end_date = None

    def download_data_df_from_yf(
        self,
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        """Downloads asset data from yFinance.

        Args:
            symbol (str): asset symbol on yfinance
            start_date (str): standard form is '2021-01-30'
            end_date (str): standard form is '2021-02-01'

        Returns:
            pd.DataFrame: Dataframe for requested symbol

        Example pd.DataFrame.head():
                     Open   High    Low  Close    Volume
        Date
        2021-02-01  45.96  48.16  45.07  47.71  52829800
        2021-02-02  49.07  50.58  49.01  50.02  46373200
        2021-02-03  51.06  51.20  49.44  49.44  47586000
        2021-02-04  50.13  51.24  49.49  51.19  36404400
        2021-02-05  51.68  52.21  50.88  51.73  43307600
        """

        start_date = pd.Timestamp(start_date)
        end_date = pd.Timestamp(end_date)
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        time_interval = '1d'

        # download and save the data to pandas DataFrame
        data_df = yf.download(
            tickers=self.symbol,
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
        simplify the amount of libraries required to clean data. ffill
        and bfill are applied to normalize data.

        Args:
            data_df (pd.DataFrame): DataFrame to clean

        Returns:
            pd.DataFrame: Cleansed data with ffill and bfill applied
        """
        spy = self.download_data_df_from_yf(
            'SPY',
            self.start_date,
            self.end_date)
        spy.dropna(subset='Close', inplace=True)
        spy.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                 inplace=True)
        # use trading days from SPY to clean data.
        new_df = spy.join(data_df, how='left')

        # fill Dataframe forwards or backwards to normalize values.
        new_df.ffill(inplace=True)
        new_df.bfill(inplace=True)

        return new_df

    def add_daily_returns(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Adds daily returns to the dataframe.

        Args:
            data_df (pd.DataFrame): DataFrame to which the daily returns will
            be added.

        Returns:
            pd.DataFrame: Dataframe with the daily returns column added.
        """
        data_df["Daily Returns"] = data_df["Close"].pct_change()
        return data_df

    def weighted_moving_average(
            self,
            series: pd.Series,
            period: int) -> pd.Series:
        """Calculates the weighted moving average of a series.

        Args:
            series (pd.Series): Series for which the weighted moving average
            is to be calculated.
            period (int): The period for which WMA is to be calculated.

        Returns:
            pd.Series: Series with the WMA values.
        """
        weights = np.arange(1, period + 1)
        return series.rolling(window=period).apply(lambda x:
                                                   np.dot(x, weights) /
                                                   weights.sum(), raw=True)

    def hull_moving_average(
            self,
            data_df: pd.Series,
            period: int
            ) -> pd.Series:
        """Calculates the Hull moving average.

        Args:
            data_df (pd.Series): Series on which HMA is calculated.
            period (int): The period for which HMA is to be calculated.

        Returns:
            pd.Series: HMA series to be used by velocity calculation.
        """
        # WMA with period n/2
        wma_half_n = self.weighted_moving_average(data_df["Close"], int(
            period / 2))

        # WMA with period n
        wma_n = self.weighted_moving_average(data_df["Close"], period)

        # HMA intermediate value
        hma_intermediate = 2 * wma_half_n - wma_n

        # Compute HMA
        hma_series = pd.Series(self.weighted_moving_average(
            hma_intermediate, int(math.sqrt(period))), index=data_df.index)

        return hma_series.dropna()

    def add_velocity(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Adds Velocity based on Close price.

        Args:
            data_df (pd.DataFrame): changes are applied to df

        Returns:
            pd.DataFrame: df after adding velocity
        """
        series_diff = pd.Series(data_df["feature_HMA"].diff(),
                                index=data_df.index)
        data_df = data_df.assign(feature_Velocity=series_diff)
        return data_df.dropna()

    def add_velocity_time_shift(
            self,
            data_df: pd.DataFrame,
            time_shift: int
            ) -> pd.DataFrame:
        """Shifts Velocity by number of days selected.

        Args:
            data_df (pd.DataFrame): changes are applied to df
            time_shift (int): time shift by number of days

        Returns:
            pd.DataFrame: df after adding time shifted velocity
        """
        series_shift = pd.Series(data_df["feature_Velocity"].shift(time_shift),
                                 index=data_df.index)
        data_df[f"feature_{time_shift}d_Shifted_Velocity"] = series_shift
        return data_df.dropna()

    def add_acceleration(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Adds Acceleration based on Velocity rate.

        Args:
            data_df (pd.DataFrame): changes are applied to df

        Returns:
            pd.DataFrame: df after adding acceleration
        """
        series_diff = pd.Series(data_df["feature_Velocity"].diff(),
                                index=data_df.index)
        data_df["feature_Acceleration"] = series_diff
        return data_df.dropna()

    def add_acceleration_time_shift(
            self,
            data_df: pd.DataFrame,
            time_shift: int
            ) -> pd.DataFrame:
        """Shifts Acceleration by number of days selected

        Args:
            data_df (pd.DataFrame): changes are applied to df
            time_shift (int): time shift by number of days

        Returns:
            pd.DataFrame: df after adding time shifted acceleration
        """
        series_shift = pd.Series(
            data_df["feature_Acceleration"].shift(time_shift),
            index=data_df.index)
        data_df[f"feature_{time_shift}d_Shifted_Acceleration"] = series_shift
        return data_df.dropna()

    def preprocess_data(self, data_df: pd.DataFrame,
                        hma_period: int) -> pd.DataFrame:
        """Applies various preprocessing steps to the data.

        Args:
            data_df (pd.DataFrame): DataFrame to preprocess.
            hma_period (int): The period for which HMA is to be calculated.

        Returns:
            pd.DataFrame: Preprocessed dataframe.
        """
        # Clean data
        cleaned_data = self.clean_data(data_df)

        # Add daily returns
        preprocessed_data = self.add_daily_returns(cleaned_data)

        # Add Hull Moving Average
        # preprocessed_data = self.add_hull_moving_average(
        #     preprocessed_data, hma_period)

        preprocessed_data = self.add_velocity(preprocessed_data)
        preprocessed_data = self.add_velocity_time_shift(preprocessed_data, 3)
        preprocessed_data = self.add_acceleration(preprocessed_data)
        preprocessed_data = self.add_acceleration_time_shift(
            preprocessed_data, 3)
        return preprocessed_data


if __name__ == "__main__":
    data_processor = DataProcessor()
    symbol = "TQQQ"
    start_date = "2021-01-30"
    stop_date = "2022-01-30"
    data_df = data_processor.download_data_df_from_yf(
        symbol, start_date, stop_date)
    preprocessed_df = data_processor.preprocess_data(data_df, 50)
    print(preprocessed_df.head(60).to_string())
