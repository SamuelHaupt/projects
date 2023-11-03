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
        self.data_df = None
        self.symbol = None
        self.start_date = None
        self.end_date = None
        self.periods = [16, 32, 64]
        self.time_shifts = [2, 4, 6, 8, 10]

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

    def clean_data(self) -> None:
        """Cleans data by using SPY's Close non-Nan, rather than grabbing
        New York Stock Exchanges trading days. This is a workaround to
        simplify the amount of libraries required to clean data. ffill
        and bfill are applied to normalize data.
        """
        spy = self.download_data_df_from_yf(
            'SPY',
            self.start_date,
            self.end_date)
        spy.dropna(subset='Close', inplace=True)
        spy.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'],
                 inplace=True)
        # use trading days from SPY to clean data.
        new_df = spy.join(self.data_df, how='left')

        # fill Dataframe forwards or backwards to normalize values.
        new_df.ffill(inplace=True)
        new_df.bfill(inplace=True)
        new_df.columns = new_df.columns.str.lower()
        self.data_df = new_df

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
            data_series: pd.Series,
            period: int
            ) -> pd.Series:
        """Calculates the Hull moving average.

        Args:
            data_series (pd.Series): Series on which HMA is calculated.
            period (int): The period for which HMA is to be calculated.

        Returns:
            pd.Series: HMA series to be used by velocity calculation.
        """
        # WMA with period n/2
        wma_half_n = self.weighted_moving_average(data_series, int(period / 2))

        # WMA with period n
        wma_n = self.weighted_moving_average(data_series, period)

        # HMA intermediate value
        hma_intermediate = 2 * wma_half_n - wma_n

        # Compute HMA
        hma_series = pd.Series(self.weighted_moving_average(
            hma_intermediate, int(math.sqrt(period))), index=data_series.index)

        return hma_series.dropna()

    def add_velocity(self, period: int) -> None:
        """Adds Velocity based on log Close price.

        Args:
            period (int): determines period for HMA
        """
        close_series = self.data_df['close']
        close_log = pd.Series(np.log(close_series), index=close_series.index)
        hma_series = self.hull_moving_average(close_log, period)
        velocity = hma_series.diff()
        velocity.dropna(inplace=True)
        self.data_df[f"feature_v_{period}p"] = velocity

    def add_velocity_time_shift(
            self,
            period: int,
            time_shift: int
            ) -> None:
        """Shifts Velocity by number of days selected.

        Args:
            period (int): correlated period to shift
            time_shift (int): time shift by number of days
        """
        series_shift = pd.Series(
            self.data_df[f"feature_v_{period}p"].shift(time_shift),
            index=self.data_df.index)
        series_shift.dropna(inplace=True)
        self.data_df[f"feature_v_{period}p_{time_shift}s"] = series_shift

    def add_acceleration(
            self,
            period: int
            ) -> None:
        """Adds Acceleration based on Velocity rate.

        Args:
            period (int): correlated velocity period
        """
        acceleration = pd.Series(
            self.data_df[f"feature_v_{period}p"].diff(),
            index=self.data_df.index)
        acceleration.dropna(inplace=True)
        self.data_df[f"feature_a_{period}p"] = acceleration

    def add_acceleration_time_shift(
            self,
            period: int,
            time_shift: int
            ) -> None:
        """Shifts Acceleration by number of days selected.

        Args:
            period (int): correlated period to shift
            time_shift (int): time shift by number of days
        """
        series_shift = pd.Series(
            self.data_df[f"feature_a_{period}p"].shift(time_shift),
            index=self.data_df.index)
        series_shift.dropna(inplace=True)
        self.data_df[f"feature_a_{period}p_{time_shift}s"] = series_shift

    def add_avg_true_range(self, period: int) -> None:
        """Calculates true range and adds average true range to data_df.
        Uses Wilder smoothing: tr_t * 1/period + atr_t-1 * (period-1)/period.

        Reference: https://www.macroption.com/atr-calculation/

        Args:
            period (int): period for which ATR should be calculated.
        """
        data_df_index = self.data_df.index
        high = self.data_df['high']
        low = self.data_df['low']
        close_previous = self.data_df['close'].shift(1)
        true_range_components = pd.DataFrame(index=data_df_index)
        true_range_components["h_l"] = high - low
        true_range_components["h_c_previous"] = np.abs(high - close_previous)
        true_range_components["l_c_previous"] = np.abs(low - close_previous)
        true_range = true_range_components.max(axis=1)

        average_true_range = pd.Series(np.zeros(len(self.data_df)),
                                       index=data_df_index)
        average_true_range.iloc[0] = true_range.iloc[0]
        weights = np.array([1 / period, (period - 1) / period])
        for index in range(1, len(self.data_df)):
            tr = true_range.iloc[index]
            atr_previous = average_true_range.iloc[index-1]
            atr_current = tr * weights[0] + atr_previous * weights[1]
            average_true_range.iloc[index] = atr_current
        self.data_df[f"feature_atr_{period}p"] = average_true_range

    def add_avg_true_range_time_shift(
            self,
            period: int,
            time_shift: int
            ) -> None:
        """Shifts ATR by number of days based on periods.

        Args:
            period (int): period to which to match time shift
            time_shift (int): time shift by number of days
        """
        atr_shifted = self.data_df[f"feature_atr_{period}p"].shift(time_shift)
        self.data_df[f"feature_atr_{period}p_{time_shift}ts"] = atr_shifted

    def preprocess_data(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Applies various preprocessing steps to the data.

        Args:
            data_df (pd.DataFrame): DataFrame to preprocess.

        Returns:
            pd.DataFrame: Preprocessed dataframe.
        """
        self.data_df = data_df
        self.clean_data()

        # Add velocity, acceleration, and correlated time shifts
        for period in self.periods:
            self.add_velocity(period)
            for time_shift in self.time_shifts:
                self.add_velocity_time_shift(period, time_shift)
            self.add_acceleration(period)
            for time_shift in self.time_shifts:
                self.add_acceleration_time_shift(period, time_shift)

        period = 14
        self.add_avg_true_range(period)
        for time_shift in self.time_shifts:
            self.add_avg_true_range_time_shift(period, time_shift)
        return self.data_df


if __name__ == "__main__":
    data_processor = DataProcessor()
    symbol = "TQQQ"
    start_date = "2021-01-30"
    stop_date = "2022-01-30"
    data_df = data_processor.download_data_df_from_yf(
        symbol, start_date, stop_date)
    preprocessed_df = data_processor.preprocess_data(data_df)
    print(preprocessed_df.head(5).to_string())
