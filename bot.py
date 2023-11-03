from sb3_contrib import RecurrentPPO
from data_processor import DataProcessor
import gymnasium as gym
import gym_trading_env
import pandas as pd
import numpy as np
from reward_function import drawdown

def get_action() -> str:
    '''
    This function gets the action from the model and returns a trade decision.

    Args: 
        None
    Returns:
        String: trade decision
    '''
    model_path = "models/20231103132728_ppo_trading_agent"
    model = RecurrentPPO.load(model_path)

    data_processor = DataProcessor()
    symbol = 'TQQQ'
    start_date = '2015-01-01'
    stop_date = '2023-10-01'
    tqqq = data_processor.download_data_df_from_yf(symbol,
                                                    start_date,
                                                    stop_date)
    tqqq_preprocessed = data_processor.preprocess_data(tqqq, 50)


    tqqq_preprocessed.dropna(inplace=True) 

    df = pd.DataFrame([], [])
    for column in tqqq_preprocessed.columns:
        df[str(column).lower()] = pd.DataFrame(tqqq_preprocessed[column].values, columns=[column])
    df["date"] = pd.DataFrame(tqqq_preprocessed["Close"].index, columns=["Date"])
    df.head()


    training_df = df[df["date"] <= "2022-12-31"]
    training_df.dropna(inplace=True)
    training_df.head()
    feature_names = training_df.columns.tolist()
    print(feature_names)
    selected_features = [
        'volume', 'daily returns', 
        'feature_hma', 'feature_velocity', 'feature_3d_shifted_velocity',
        'feature_acceleration', 'feature_3d_shifted_acceleration'
    ]
    observation = training_df[selected_features].iloc[-1].values

    testing_env = gym.make("TradingEnv",
                        df=training_df,
                        positions=[0, 1],
                        initial_position=1,
                        portfolio_initial_value=1000,
                        reward_function=drawdown)

    # get action from the model
    action, _states = model.predict(observation , deterministic=True)

    print(f"Action: {action}")
    if action == 1:
        trade_decision = 'buy'
    elif action == 0:
        trade_decision = 'sell'
    else:
        trade_decision = 'hold'
    print(f"Trade decision: {trade_decision}")
    return trade_decision
