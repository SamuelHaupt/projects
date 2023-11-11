from sb3_contrib import RecurrentPPO
from data_processor import DataProcessor
from env import AssetTradingEnv
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from datetime import date


trading_client = TradingClient('PK81K3G1O76EG5ITK9AQ', 'E9k93RSv1x8ojGmgqd43KmPKAlm44DtEVrCDikel', paper=True)
account = trading_client.get_account()


def main():
    '''
    main function of the bot.
    Args:
        None
    Returns:
        None
    '''
    all_assets = get_assets()
    tqqq_asset = get_specified_asset('TQQQ', all_assets)
    print(f"TQQQ Balance: {tqqq_asset.qty}")

    usd_balance = get_usd_balance()
    print(f"USD Balance: {usd_balance }")

    # get action
    trade_decision = get_action()
    print(f"Trade decision: {trade_decision}")

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
    account_balance = get_usd_balance()
    account_balance = float(account_balance)
    model_path = "models/20231110194307_ppo_trading_agent"
    model = RecurrentPPO.load(model_path)

    data_processor = DataProcessor()
    symbol = 'TQQQ'
    # date format YYYY-MM-DD
    start_date = '2019-01-01'
    stop_date = date.today() - pd.Timedelta(days=1)
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

    trading_env = AssetTradingEnv(data_df=trading_df, initial_balance=account_balance)
    observation = trading_env._get_obs()
    # print(observation)

    # get action from the model
    action, lstm_states = model.predict(observation)

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


def get_usd_balance():
    '''
    Retrieves the USD balance from the Alpaca trading account.
    Args:
        None
    Returns:
        usd_balance (float): The amount of USD available in the account
    '''
    usd_balance = account.cash
    return usd_balance


def get_assets():
    '''
    Retrives the assets from the Alpaca trading account.
    Args:
        None
    Returns:
        bitcoin_balance (dict): A dictionary with details of Bitcoin-related assets
    '''
    return trading_client.get_all_positions()

def get_specified_asset(asset_symbol, assets):
    '''
    Retrieves the specified asset from the Alpaca trading account.
    Args:
        asset_symbol (str): The symbol of the asset to retrieve
    Returns:
        asset (dict): A dictionary with details of the specified asset
    '''
    for asset in assets:
        if asset.symbol == asset_symbol:
            return asset
    print(f"Asset {asset_symbol} not found")
    return None



if __name__ == '__main__':
    main()