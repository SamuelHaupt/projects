# CS467_F2023_CryptoTradingBot

### Use data_processor.py:

1. Initialize DataProcessor.
2. Use instantiated DataProcessor and call `download_data_df_from_yf()` with symbol, start_date, and end_date. Symbol correlates to stock symbol, such as `TQQQ`. Start and end dates should be in the format "YY-MM-DD". The downloaded data is returned from the call.
    + Although periods and time_shifts are not passed to the DataProcessor at initialization, periods and time_shifts are set at compile time to [16, 32, 64] and [2, 4, 6, 8, 10], respectively. A filter smooths based on the periods and velocity, acceleration, and average true range are then shifted by the time shifts. All of these state vectors are fed to the environment and agent.
3. Preprocess data by calling `preprocess_data()`. Pass the data received from the downloader. Preprocessed data will be returned from the function.
    + Preprocessor adds Hull Moving Average, velocity, acceleration, average true range, and time shifts. Additionally, `NaN` rows are removed.

```py
data_processor = DataProcessor()
symbol = "TQQQ"
start_date = "2021-01-30"
stop_date = "2022-01-30"
periods = [16, 32, 64]
time_shifts = [2, 4, 6, 8, 10]
data_df = data_processor.download_data_df_from_yf(
    symbol, start_date, stop_date)
preprocessed_df = data_processor.preprocess_data(data_df)
```

### Use asset_trading_env.py:

1. After downloading and preprocessing the data, pass the data to the environment and initialize.
    + Initial balance and render mode are both defaulted values. Set them differently if desired. However, setting render_mode to anything else other than 'human' will not change the functionality of render.
2. Use reset to set the environment to the initial values before the agent begins its training.
3. Use `env.step()` to step through an entire episode. An episode will match the length of the rows of data in `preprocessed_df`. Therefore, ensure to set a loop to match the maximum episode length. `env.step()` requires an action of `0` or `1`. We provided a randomized selection to simulate the agent. When an agent is added, `action` will be returned from the `agent.predict()`.


```py
balance = 100_000.00
mode = 'human'
env = AssetTradingEnv(preprocessed_df, initial_balance=balance, render_mode=mode)
obs, info = env.reset()
random.seed(1)
for _ in range(len(preprocessed_df)):
    action = random.action([0, 1])
    print()
    print(f"Action: {action}")
    observation, reward, terminated, truncated, info = env.step(action)
    for key, value in info.items():
        print(key, ": ", value)
```

