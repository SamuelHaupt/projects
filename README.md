# CS467_F2023_CryptoTradingBot

### Use data_processor.py

1. Initialize DataProcessor.
2. Use instantiated DataProcessor and call `download_data_df_from_yf()` with symbol, start_date, and end_date. Symbol correlates to stock symbol, such as `TQQQ`. Start and end dates should be in the format "YY-MM-DD". The downloaded data is returned from the call.
3. Preprocess data by calling `preprocess_data()`. Pass the data received from the downloader. Preprocessed data will be returned from the function.
    + Preprocessor adds Hull Moving Average, velocity, acceleration, average true range, and time shifts. Additionally, `NaN` rows are removed.

```py
data_processor = DataProcessor()
symbol = "TQQQ"
start_date = "2021-01-30"
stop_date = "2022-01-30"
data_df = data_processor.download_data_df_from_yf(
    symbol, start_date, stop_date)
preprocessed_df = data_processor.preprocess_data(data_df)
```

