import numpy as np
from sb3_contrib import RecurrentPPO
from reward_function import drawdown
from agent_module import PPOAgentModule
from data_processor import DataProcessor
import gymnasium as gym
import gym_trading_env
from stable_baselines3.common.vec_env import DummyVecEnv
import pandas as pd


def main():
    data_processor = DataProcessor()
    symbol = 'TQQQ'
    start_date = '2019-01-01'
    stop_date = '2023-10-01'
    tqqq = data_processor.download_data_df_from_yf(symbol,
                                                   start_date,
                                                   stop_date)
    tqqq_preprocessed = data_processor.preprocess_data(tqqq)

    # Format table date proper format and name
    tqqq_preprocessed.dropna(inplace=True)  # Clean again !

    # Format to gym-trader-env format
    df = pd.DataFrame([], [])
    for column in tqqq_preprocessed.columns:
        df[str(column).lower()] = pd.DataFrame(tqqq_preprocessed[column].values, columns=[column])
    df["date"] = pd.DataFrame(tqqq_preprocessed["close"].index, columns=["Date"])
    df.head()

    # Setup training data
    training_df = df[df["date"] <= "2021-12-31"]
    training_df = training_df.dropna()
    training_df.head()

    # Setup testing data
    testing_df = df[df["date"] > "2021-12-31"]
    testing_df = testing_df.dropna()
    testing_df.head()



    def trainer():
        #  load training environment
        training_env = gym.make("TradingEnv",
                        df=training_df,
                        positions=[0, 1],
                        initial_position=1,
                        portfolio_initial_value=1000,
                        reward_function=drawdown)
        # Train model
        agent = PPOAgentModule(training_env)
        agent.train(10000)



    def tester():
        # Load testing environment
        testing_env = gym.make("TradingEnv",
                            df=testing_df,
                            positions=[0, 1],
                            initial_position=1,
                            portfolio_initial_value=1000,
                            reward_function=drawdown)
    
        # Load model and agent
        agent = PPOAgentModule(testing_env, model_path="models/20231103173638_ppo_trading_agent")
        print(agent)
        agent.test(testing_env, testing_df)
    
    while True:
        print("1. Train")
        print("2. Test")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid choice.")
            continue
        print("\n\n")
        if choice == 1:
            trainer()
            break
        elif choice == 2:
            tester()
            break
        print("\n\n")


if __name__ == '__main__':
    main()


