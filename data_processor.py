import numpy as np
import pandas as pd
import math


class DataProcessor():
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

    def weighted_moving_average(series: pd.Series, period: int) -> pd.Series:
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

    def add_hull_moving_average(
            self, data_df: pd.DataFrame, period: int) -> pd.DataFrame:
        """Adds the Hull Moving Average to the dataframe.

        Args:
            data_df (pd.DataFrame): DataFrame to which the HMA will be added.
            period (int): The period for which HMA is to be calculated.

        Returns:
            pd.DataFrame: Dataframe with the HMA column added.
        """
        # WMA with period n/2
        wma_half_n = self.weighted_moving_average(data_df["Close"], int(
            period / 2))

        # WMA with period n
        wma_n = self.weighted_moving_average(data_df["Close"], period)

        # HMA intermediate value
        hma_intermediate = 2 * wma_half_n - wma_n

        # Compute HMA
        data_df["HMA"] = self.weighted_moving_average(hma_intermediate,
                                                      int(math.sqrt(period)))

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
        preprocessed_data = self.add_hull_moving_average
        (preprocessed_data, hma_period)

        return preprocessed_data


if __name__ == "__main__":
    yf_downloader = DataProcessor()
    symbol = "SPY"
    start_date = "2021-01-30"
    stop_date = "2022-01-30"
    data_df = yf_downloader.download_data_df(symbol, start_date, stop_date)
    preprocessed_df = yf_downloader.preprocess_data(data_df)
