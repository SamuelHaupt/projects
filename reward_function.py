import pandas as pd
import numpy as np
from gym_trading_env.utils.history import History

import risk_management
from risk_management import RiskData


# class Rewards():
# causes gym env to fail when imported to main as a class
    
def drawdown(history: History, win_size: int = 144) -> float:
    """
    Function for calculating drawdown

    Args:
        History 
        Window Size

    Returns:
        risk weighted positive profit - risk weighted drawdown
    """
    # 0 to 1 to adjust risk tolerance
    profit_reward_weight = 0.5

    # pull data from history
    data_close = np.array(history['data_close'][-win_size:], dtype=np.float64)
    pos = np.array(history['position'][-win_size:], dtype=np.float64)

    # calculate log returns for the rolling window 
    log_data = np.log(data_close)
    log_return = np.where(pos[1:] == 1, np.diff(log_data), 0)

    # Calculate drawdown for the rolling window
    portfolio_value = np.exp(log_return).cumprod()
    peak_value = np.maximum.accumulate(portfolio_value)
    drawdown = 1.0 - (portfolio_value / peak_value)

    # Calculate the mean drawdown
    mean_drawdown = np.mean(drawdown)

    # Calculate positive profit as the total profit in the window
    positive_profit = np.sum(np.where(log_return > 0, log_return, 0))

    # Combine drawdown and positive profit in the reward
    reward = (profit_reward_weight * positive_profit) - ((1 - profit_reward_weight) * mean_drawdown)

    return reward


def sortino(history: History, win_size: int = 144) -> float:
    """
    Function for calculating sortino ratio

    Args:
        History 
        Window Size

    Returns:
        Sortino ratio
    """
    # adjust based on some baseline
    risk_free_rate = 0.0

    # pull data from history
    data_close = np.array(history['data_close'][-win_size:], dtype=np.float64)
    pos = np.array(history['position'][-win_size:], dtype=np.float64)

    # calculate log returns for the rolling window 
    log_data = np.log(data_close)
    log_return = np.where(pos[1:] == 1, np.diff(log_data), 0)

    # Calculate average profit in the window
    average_profit = np.mean(np.where(log_return > 0, log_return, 0))

    # Calculate average loss in the window
    average_loss = np.mean(np.where(log_return < risk_free_rate, log_return^2, 0))

    reward = average_profit/(average_loss)^0.5 # Are we wanting to use exponnet here? Might be a bitwise OR

    return reward

def simple_reward(history: History):
    """
    Reward Function

    Args:
        History 
        Window Size

    Returns:
        Returns simple log returns
    """
    reward = np.log(history["portfolio_valuation", -1] / history["portfolio_valuation", -2])
    return reward

def smart_reward(history: History):
    """
    Reward Function

    Args:
        History 
        Window Size

    Returns:
        Retruns reward based on a rolling range. Reward is positive when the agent has bought and price breaks out of the range.
        If last action was buy and price stays flat or breaks below the low range, a negative reward is given

    """
    # pass if there are not enough steps worth of data
    if history['step', -1] == 0:
        reward = 0
        return reward
    else:
        reward = history['reward', -2]

        # adjust range based on number of days to include in trialing average
        data_close = history['data_close']
        # Calculate the 10-day rolling average
        if len(data_close) >= 10:
            trailing_avg = np.mean(data_close[-10:])
            std_dev = np.std(data_close[-10:])
        else:
            # Handle cases where there are not enough data points for a 10-day average
            trailing_avg = np.mean(data_close)
            std_dev = np.std(data_close)

        # these should be replaced with ATR and some other bounding calculation once those get added to the history object
        upper_range = trailing_avg + std_dev
        lower_range = trailing_avg - std_dev

        # diagnostic logging print statements
        #print("trailing avg:", trailing_avg)
        #print("dailey close:", history['data_close', -1])
        #print("close:", history['data_close'])
        #print("high:", upper_range)
        #print("low:", lower_range)

        # if previous action was to buy and price breaks out, increase reward
        if history['position', -1] == 1 and history['data_close', -1] > upper_range:
            reward += 1
        # if previous action was to buy and price dumps, decrease reward
        elif history['position', -1] == 1 and history['data_close', -1] < lower_range:
            reward -= 1
        # if previous action was to sell and price breaks out, decrease reward
        elif history['position', -1] == 0 and history['data_close', -1] > upper_range:
            reward -= 1
        # if previous action was to sell and price dumps, increase reward
        elif history['position', -1] == 0 and history['data_close', -1] < lower_range:
            reward -= 1

        # need to add case where price stays flat for some amount of time and agent is buying

    return reward


def rsi_reward(history, window_size=14):
    """
    Reward function based on the RSI (Relative Strength Index)

    Args:
        history: A dictionary with 'data_close' as a key and list of prices as values
        window_size: The window size to calculate RSI (default is 14 periods)

    Returns:
        Reward based on the RSI levels, as a floating-point number.
    """

    def calculate_rsi(prices, window=window_size):
        deltas = np.diff(prices)
        seed = deltas[:window+1]
        up = seed[seed >= 0].sum()/window
        down = -seed[seed < 0].sum()/window
        rs = up/down
        rsi = np.zeros_like(prices)
        rsi[:window] = 100. - 100./(1. + rs)

        for i in range(window, len(prices)):
            delta = deltas[i - 1]  # because the diff is 1 shorter
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta

            up = (up*(window-1) + upval)/window
            down = (down*(window-1) + downval)/window

            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)

        return rsi

    # Retrieve the close price data from the history object
    prices = np.array(history['data_close'])

    # Calculate the RSI values
    rsi_values = calculate_rsi(prices)

    # Get the latest RSI value
    current_rsi = rsi_values[-1]

    # Define thresholds for RSI that indicate overbought and oversold conditions
    overbought_threshold = 70
    oversold_threshold = 30

    # Initialize the reward as a float
    reward = 0.0

    # If the RSI is oversold, it might be a good buying opportunity (positive reward)
    if current_rsi < oversold_threshold:
        reward += (oversold_threshold - current_rsi) / oversold_threshold
    # If the RSI is overbought, it might be a good selling opportunity (negative reward)
    elif current_rsi > overbought_threshold:
        reward -= (current_rsi - overbought_threshold) / (100 - overbought_threshold)

    return reward


def risk_management_reward(history: History, win_size: int = 30) -> float:
    # Reward function -1 to 1
    risk_data = RiskData()

    # Use history run risk analysis
    for i in range(len(history)):
        risk_data.update_risk_data(history[i])

    # Run risk analysis
    if risk_management.run_risk_analysis(history[-1], risk_data):
        # Risk Triggered
        return -1

    else:
        return 0
