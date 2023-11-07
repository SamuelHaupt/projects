from sb3_contrib import RecurrentPPO
from data_processor import DataProcessor
import gymnasium as gym
import pandas as pd
from reward_function import drawdown
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

trading_client = TradingClient('placeholder', 'placeholder', paper=True)
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
    print(f"Trade decision: {trade_decision}")

    # # # trade
    # trade(trade_decision)


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
    model_path = "models/20231105145531_ppo_trading_agent"
    model = RecurrentPPO.load(model_path)

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
    trading_df = df[df["date"] <= "2021-12-31"]
    trading_df = trading_df.dropna()
    trading_df.head()
    
    feature_names = trading_df.columns.tolist()
    print(feature_names)
    selected_features = [
'close' , 'volume','feature_v_16p', 'feature_v_16p_2s', 'feature_v_16p_4s', 'feature_v_16p_6s', 'feature_v_16p_8s', 
'feature_v_16p_10s', 'feature_a_16p', 'feature_a_16p_2s', 'feature_a_16p_4s', 'feature_a_16p_6s', 'feature_a_16p_8s', 'feature_a_16p_10s', 
'feature_v_32p', 'feature_v_32p_2s', 'feature_v_32p_4s', 'feature_v_32p_6s', 'feature_v_32p_8s', 'feature_v_32p_10s', 'feature_a_32p', 
'feature_a_32p_2s', 'feature_a_32p_4s', 'feature_a_32p_6s', 'feature_a_32p_8s', 'feature_a_32p_10s', 'feature_v_64p', 'feature_v_64p_2s', 
'feature_v_64p_4s', 'feature_v_64p_6s', 'feature_v_64p_8s', 'feature_v_64p_10s', 'feature_a_64p', 'feature_a_64p_2s', 'feature_a_64p_4s', 
'feature_a_64p_6s', 'feature_a_64p_8s', 'feature_a_64p_10s', 'feature_atr_14p', 'feature_atr_14p_2ts', 'feature_atr_14p_4ts', 'feature_atr_14p_6ts', 
'feature_atr_14p_8ts', 'feature_atr_14p_10ts'
    ]
    
    observation = trading_df[selected_features].iloc[-1].values
    print("\n\nBefore removing the timestamp, observation cant be made: ",observation)
    # observation[-1] = 0
    # print("\n\nAfter removing the timestamp (it works after removing it): ",observation)
    observation = pd.to_numeric(observation, errors='coerce')


    testing_env = gym.make("TradingEnv",
                        df=trading_df,
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
        market_order_data = MarketOrderRequest(
            symbol='TQQQ',
            qty=0.5,
            side=OrderSide.BUY,
            type='market',
            time_in_force=TimeInForce.DAY)

        trading_client.submit_order(market_order_data)

    elif trade_decision == 'sell':
        market_order_data = MarketOrderRequest(
            symbol='TQQQ',
            qty=0.5,
            side=OrderSide.SELL,
            type='market',
            time_in_force=TimeInForce.DAY)
        
        trading_client.submit_order(market_order_data)

    else:
        print('Holding position')

if __name__ == '__main__':
    main()