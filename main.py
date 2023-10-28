import numpy as np
from stable_baselines3 import PPO
import reward_function
from agent_module import PPOAgentModule
from data_processor import DataProcessor
import gymnasium as gym
import gym_trading_env
from stable_baselines3.common.vec_env import DummyVecEnv


import pandas as pd


def main():
    data_processor = DataProcessor()
    symbol = 'TQQQ'
    start_date = '2015-01-01'
    stop_date = '2023-10-01'
    tqqq = data_processor.download_data_df_from_yf(symbol,
                                                   start_date,
                                                   stop_date)
    tqqq_preprocessed = data_processor.preprocess_data(tqqq, 50)

    # Format table date proper format and name
    tqqq_preprocessed.dropna(inplace=True)  # Clean again !

    # Format to gym-trader-env format
    df = pd.DataFrame([], [])
    for column in tqqq_preprocessed.columns:
        df[str(column).lower()] = pd.DataFrame(tqqq_preprocessed[column].values, columns=[column])
    df["date"] = pd.DataFrame(tqqq_preprocessed["Close"].index, columns=["Date"])
    df.head()

    # Setup training data
    training_df = df[df["date"] <= "2022-12-31"]
    training_df.dropna(inplace=True)
    training_df.head()

    # Setup testing data
    testing_df = df[df["date"] > "2022-12-31"]
    testing_df.dropna(inplace=True)
    testing_df.head()

    # Load training environment
    training_env = gym.make("TradingEnv",
                            df=training_df,
                            positions=[0, 1],
                            initial_position=1,
                            portfolio_initial_value=1000,
                            reward_function=reward_function.reward_function_drawdown)

    # agent = PPOAgentModule(training_env)
    # agent.train(10000)

    # Load Model
    agent = PPO.load("models/20231028161306_ppo_trading_agent.zip")
    print(agent)

    # Load testing environment
    testing_env = gym.make("TradingEnv",
                           df=testing_df,
                           positions=[0, 1],
                           initial_position=1,
                           portfolio_initial_value=1000,
                           reward_function=reward_function.reward_function_drawdown)

    observation, info = testing_env.reset()
    print("# Testing model on testing data...")
    for _ in range(len(testing_df)):
        position_index, _states = agent.predict(observation)
        observation, reward, done, truncated, info = testing_env.step(position_index)
        if done or truncated:
            break


if __name__ == '__main__':
    main()
