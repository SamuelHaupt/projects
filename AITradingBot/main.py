from agent_module import PPOAgentModule
from data_processor import DataProcessor
from asset_trading_env import AssetTradingEnv
import pandas as pd
from datetime import date


def main():
    dp = DataProcessor()
    symbol = 'TQQQ'

    def trainer(df: pd.DataFrame):
        start = '2011-06-01'
        stop = '2020-01-01'

        # Reset Index to reference Date and select data from date range
        df.reset_index(inplace=True)
        training_df = df[(df['Date'] > start) & (df['Date'] <= stop)]

        #  load training environment
        training_env = AssetTradingEnv(data_df=training_df)

        # Train model
        agent = PPOAgentModule(training_env)
        agent.train(5_000)

    def tester(df: pd.DataFrame):
        start = '2020-01-02'
        stop = '2023-11-30'

        # Reset Index to reference Date and select data from date range
        df.reset_index(inplace=True)
        testing_df = df[(df['Date'] > start) & (df['Date'] <= stop)]

        # Load testing environment
        testing_env = AssetTradingEnv(data_df=testing_df)

        # Load model and agent
        print("Testing model on testing data.")
        for test in range(1):
            agent = PPOAgentModule(
                testing_env,
                model_path="models/20231206075227_ppo_trading_agent.zip")
            agent.test(testing_env, testing_df)

    while True:
        start_date = '2011-01-01'
        today = str(date.today())
        stop_date = today
        tqqq = dp.download_data_df_from_yf(
            symbol, start_date, stop_date)
        downloaded_df = dp.preprocess_data(tqqq)

        print("1. Train")
        print("2. Test")
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Please enter a valid choice.")
            continue
        print("\n")
        if choice == 1:
            trainer(downloaded_df)
            break
        elif choice == 2:
            tester(downloaded_df)
            break
        print("\n")


if __name__ == '__main__':
    main()
