import pandas as pd


class YFDownloader():

    def add_daily_returns(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Adds daily returns to the dataframe.

        Args:
            data_df (pd.DataFrame): DataFrame to which the daily returns will
            be added.

        Returns:
            pd.DataFrame: Dataframe with the daily returns column added.
        """
        data_df['Daily Returns'] = data_df['Close'].pct_change()
        return data_df

    def preprocess_data(self, data_df: pd.DataFrame) -> pd.DataFrame:
        """Applies various preprocessing steps to the data.

        Args:
            data_df (pd.DataFrame): DataFrame to preprocess.

        Returns:
            pd.DataFrame: Preprocessed dataframe.
        """
        # Clean data
        cleaned_data = self.clean_data(data_df)

        # Add daily returns
        preprocessed_data = self.add_daily_returns(cleaned_data)

        return preprocessed_data


if __name__ == "__main__":
    yf_downloader = YFDownloader()
    symbol = 'SPY'
    start_date = '2021-01-30'
    stop_date = '2022-01-30'
    data_df = yf_downloader.download_data_df(symbol, start_date, stop_date)
    preprocessed_df = yf_downloader.preprocess_data(data_df)
