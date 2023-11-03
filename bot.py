from sb3_contrib import RecurrentPPO
from data_processor import DataProcessor
import gymnasium as gym
import pandas as pd
from reward_function import drawdown
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.enums import OrderSide, TimeInForce

trading_client = TradingClient('api-key', 'secret-key', paper=True)
account = trading_client.get_account()


def main():
    '''
    main function of the bot.
    Args:
        None
    Returns:
        None
    '''
    # get assets
    assets = get_assets()
    print(f"Assets: {assets}")

    # get action
    trade_decision = get_action()

    # trade
    trade(trade_decision)


def get_assets():
    '''
    This function gets all the assets from the Alpaca API.
    Args:
        None
    Returns:
        assets (list): list of assets
    '''
    search_params = GetAssetsRequest(asset_class=AssetClass.CRYPTO)
    assets = trading_client.get_all_assets(search_params)
    return assets


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
    tqqq = data_processor.download_data_df_from_yf(
        symbol, start_date, stop_date)
    tqqq_preprocessed = data_processor.preprocess_data(tqqq, 50)

    tqqq_preprocessed.dropna(inplace=True)

    df = pd.DataFrame([], [])
    for column in tqqq_preprocessed.columns:
        df[str(column).lower()] = pd.DataFrame(
            tqqq_preprocessed[column].values, columns=[column])
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
    action, _states = model.predict(observation, deterministic=True)

    print(f"Action: {action}")
    if action == 1:
        trade_decision = 'buy'
    elif action == 0:
        trade_decision = 'sell'
    else:
        trade_decision = 'hold'
    print(f"Trade decision: {trade_decision}")
    return trade_decision


def trade(trade_decision: str) -> None:
    '''
    Function to perform the crypto trade
    Args:
        trade_decision (str): buy, sell, or hold
    Returns:
        None
    '''
    if trade_decision == 'buy':
        trading_client.submit_order(
            symbol='TQQQ',
            qty=0.5,
            side=OrderSide.BUY,
            type='market',
            time_in_force=TimeInForce.DAY
        )
    elif trade_decision == 'sell':
        trading_client.submit_order(
            symbol='TQQQ',
            qty=0.5,
            side=OrderSide.SELL,
            type='market',
            time_in_force=TimeInForce.DAY
        )
    else:
        print('Holding position')
