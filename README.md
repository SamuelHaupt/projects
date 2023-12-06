# CS467_F2023_CryptoTradingBot

### main.py is the file to run when training and testing the bot.
There are 6 variables to adjust to run main.py 

1. symbol = 'TQQQ' : line 10
   ```py
    dp = DataProcessor()
    symbol = 'TQQQ'
   ```

-In 'trainer()'
2. start = '2011-06-01' : line 13
3. stop = '2020-01-01' : line 14
4. agent.train(1_000_000) : line 25
    ```py
    def trainer(df: pd.DataFrame):
        start = '2011-06-01'
        stop = '2020-01-01'
        ...
        # Train model
        agent = PPOAgentModule(training_env)
        agent.train(1_000_000)
    ```

-In 'tester()'
5. start = '2011-06-01' : line 28
6. stop = '2020-01-01' : line 29
```py
def tester(df: pd.DataFrame):
    start = '2020-01-02'
    stop = '2023-11-30'
```

These variables are use to adjust the parameters of the model. Once the model has been trained, it will be saved in the models folder for use. Copy the model from the console and paste the model filename on line 43 after the "models/xxxx.zip" The model will be ready for testing. 

```py
 # Load model and agent
    print("Testing model on testing data.")
    for test in range(20):
        agent = PPOAgentModule(
            testing_env,
            model_path="models/20231115162135_ppo_trading_agent.zip")
        agent.test(testing_env, testing_df)
```


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

