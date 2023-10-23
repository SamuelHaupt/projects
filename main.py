from data_processor import DataProcessor
import gymnasium as gym
import gym_trading_env
import pandas as pd

def main():
    data_processor = DataProcessor()
    symbol = 'TQQQ'
    start_date = '2021-01-30'
    stop_date = '2022-01-30'
    tqqq = data_processor.download_data_df_from_yf(symbol,
                                                   start_date,
                                                   stop_date)
    tqqq_preprocessed = data_processor.preprocess_data(tqqq)

    print(tqqq_preprocessed.head())

    # CREATE ENVIRONMENT
    df = pd.read_csv("data/binance-BTCUSDT-1h.csv")

    # Format table date proper format and name
    df["Date"] = pd.to_datetime(df["date_open"])
    df.dropna(inplace=True)  # Clean again !

    # Return to the first row
    df.head()

    # Create Trading Environment
    training_env = gym.make("TradingEnv",
                            name="BTCUSD",
                            df=df,
                            windows=5,
                            positions=[0, 1],  # 0(=SELL ALL), +1 (=BUY ALL)
                            initial_position=0,
                            portfolio_initial_value=1000,
                            )

    truncated = False
    observation, info = training_env.reset()
    while True and not truncated:
        position_index = training_env.action_space.sample()
        observation, reward, done, truncated, info = training_env.step(position_index)

    print("Info:", info)
    print("Observation:", observation)
    print("Portfolio Value:", info.get("portfolio_valuation"))
    training_env.close()
    print("Testing Environment Complete!")


if __name__ == '__main__':
    main()
