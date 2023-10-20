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
