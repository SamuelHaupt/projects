# AI Trading Bot

We built a robot to trade high volatility assets, especially 3x ETFs, using reinforcement learning algorithms that aims to maximize returns while minimizing risk to initial capital. We focused our efforts on recurrent Proximal Policy Optimization (PPO) where the agent updates policies throughout its training.

## Installation:

Instructions are for linux/unix based systems.

1. Clone repo
2. Install dependencies: `pip install -r requirements.txt`
3. Test if intallation was successful:
    + Run python by inputting: `python` or `python3` (on a MacBook Pro).
      If needed (some Windows users have issues with not all packages installing through requirements.txt)
    + Import yfinance: `import yfinance`.
    + Import Stable Baseline3: `import sb3_contrib`.
    + If you receive an error when importing `sb3_contrib`, then you need to fix errors related to the installation of all dependencies in `requirements.txt`.

## Use `main.py` for main entry-point to application:

Start with `main.py`. There are only six variables to adjust, if desired. However, none need to be adjusted in order to run our project.

> You can select other stock symbols if you wish to run our application on other assets. However, we built our application to use `TQQQ`, which is a 3x version of QQQ, which takes the top 100 assets in the Nasdaq.

Here are the locations which you can modify, if desired:

```py
...
10: symbol = 'TQQQ'
...
13: start = '2011-06-01'
14: stop = '2020-01-01'
...
25: agent.train(5_000)
...
28: start = '2020-01-02'
29: stop = '2023-11-30'
```

When running the application from the main entry point, you will be provided with two options to select: "1" (train) or "2" (test). The difference between these two is train doesn't require a pre-loaded model, whereas test does. Select "1" to start. This will train the model over 1 million iterations, which will take up to 10 hours. Shorten this to 40 thousand steps (or less) to finish the training in under 20 minutes. After the model finishes training, the agent will save the model in a zip file, for example, `models/20231206075227_ppo_trading_agent.zip`. Change the file path and name to the freshly zipped model as indicated below:

```py
43: model_path='models/20231206075227_ppo_trading_agent.zip'
```

> Important Note: Make sure to include `models/` in the file path for `model_path`. Otherwise, the application will not see the saved model.

Next, select "2" to test the model to determine the success of the trained model.

### Example outputs for each choice

+ Choice 1 - Train:

```py
 Using device: cpu
 Training.
 Start Time: 2023-12-06 07:51:54.753794
 |  Market Return:  2401.18% |   Portfolio Return:   334.70% |  Reward: -2784.921916381719
 |  Market Return:  2401.18% |   Portfolio Return:   374.91% |  Reward: -2722.249590576272
 End Time: 2023-12-06 07:52:27.954726
 Training complete.
 Model saved at path: models/20231206075227_ppo_trading_agent
```

+ Choice 2 - Test:

```py
Testing model on testing data.
|  Market Return:   102.07% |   Portfolio Return:   -25.22% |  Reward: -8128.764280654095
...
```

## Stand-alone access to other modules

The above description provides enough detail to how to run the application. The following instructions are detailed information on how to run each module separately from the main entry-point.

### Use `data_processor.py` to download asset data other than `TQQQ`:

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

### Use `asset_trading_env.py` to build a custom asset trading environment:

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

### Use `server.py` and `bot.py` to deploy the Alpaca trading user interface:

1. Create an account at [Alpaca](https://alpaca.markets/).
2. Replace the `key` and `secretkey` in both `server.py` and `bot.py` with values given by Alpaca.
3. Run the server a terminal: `python3 server.py`.
4. Run the bot in a separate terminal: `python3 bot.py` 
5. Click on or copy and paste local website address from the output of `server.py` terminal to a web browser.
6. Select options to buy and sell with Alpaca.

+ `server.py`:

```py
my_bot = Bot(secret_key='REPLACE_ME', key='REPLACE_ME') 
app = TradingApp(my_bot)
app.run()
```

+ `bot.py`:

```py
key = 'REPLACE_ME'
secret_key = 'REPLACE_ME'
bot = Bot(secret_key, key)
bot.trader()
bot.trade(asset_buy_quantity=None, trade_dec='buy')
```

![UI](https://i.imgur.com/e5zIdhw.png)
Image 1: Alpaca User Interface. Select single or continuous to automate trading. Using the manual functionality to suggest to the neural network when to buy and sell. 

### Using `backtesting.py` to test strategies against model:

```py
import talib
import datetime
from backtesting import Backtest, Strategy 
from backtesting.lib import crossover
import pandas as pd
import yfinance as yf
import math
import numpy as np
```

```py
def download_and_add_atr(symbol, start_date, end_date, periods, time_shifts):
    # Download data
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
```

Similar to the bot itself, the backtests need to download and preprocess data. The bot strips some columns that the backtesting library requires so I couldn’t use the bot’s preprocessor, but used the same steps. Download from yfinance, dropna’s add some new columns as indicators.

```py
# Define parameters

# different symbols to test back tests with
#symbol = "TQQQ"
#symbol = "GOOG"
# symbol = "^GSPC"
# symbol = "MSFT"
# symbol = "BTC_USD"
symbol = 'BTC-USD'

# Can use different start and stop dates
# start_date = "2018-01-30"
#start_date = "2021-01-30"
#end_date = "2022-01-30"
#end_date = "2021-11-09"
start_date = "2022-01-30"
end_date = "2022-12-31"
```

Here are some quick ways to change between different assets and time periods

```py
class ATRStrategy(Strategy):
    atr_period = 14  # Period for ATR calculation

    def init(self):
        # Extract high, low, and close as numpy arrays
        high = np.array(self.data.High)
        low = np.array(self.data.Low)
        close = np.array(self.data.Close)

        # Calculate ATR using TA-Lib
        self.atr = self.I(talib.ATR, high, low, close, timeperiod=self.atr_period)

    def next(self):
        if not self.position and self.data.Close[-1] > self.data.Close[-2] + self.atr[-1]:
            self.buy()
        elif self.position and self.data.Close[-1] < self.data.Close[-2] - self.atr[-1]:
            self.position.close()
```

A smaller example strategy. Uses TA-Lib to calculate Average True Range, buys or sells based on that range.

```py
bt = Backtest(data_df, ATRStrategy, cash=100000)
stats = bt.run()
print(stats)
bt.plot(filename=filename)
```
