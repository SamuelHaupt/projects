from sb3_contrib import RecurrentPPO
from data_processor import DataProcessor
from env import AssetTradingEnv
import pandas as pd
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from datetime import date

key = 'PK81K3G1O76EG5ITK9AQ'
secret_key = 'E9k93RSv1x8ojGmgqd43KmPKAlm44DtEVrCDikel'
trading_client = TradingClient(key, secret_key, paper=True)
account = trading_client.get_account()
buying_power = account.buying_power
print(f"Buying power: {buying_power}")


def get_action(account_balance) -> str:
    '''
    This function gets the action from the model and returns a trade decision.

    Args:
        None
    Returns:
        String: trade decision
    '''
    model_path = "models/20231110194307_ppo_trading_agent"
    model = RecurrentPPO.load(model_path)
    data_processor = DataProcessor()
    symbol = 'TQQQ'

    start_date = '2010-01-01'
    stop_date = date.today() - pd.Timedelta(days=1)
    # stop_date = '2020-01-01'
    tqqq = data_processor.download_data_df_from_yf(
        symbol, start_date, stop_date)
    trading_df = data_processor.preprocess_data(tqqq)
    trading_df.dropna(inplace=True)
    trading_env = AssetTradingEnv(
        data_df=trading_df,
        initial_balance=account_balance)

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


def trade(
        trade_decision: str, account_balance,
        tqqq_balance, tqqq_price) -> None:
    '''
    Function to perform the crypto trade
    Args:
        trade_decision (str): buy, sell, or hold
    Returns:
        None
    '''
    if trade_decision == 'buy':
        usd_trade_amount = account_balance / 2
        tqqq_buy_quantity = usd_trade_amount / tqqq_price
        market_order_data = MarketOrderRequest(
            symbol='TQQQ',
            qty=tqqq_buy_quantity,
            side=OrderSide.BUY,
            type='market',
            time_in_force=TimeInForce.DAY)

        print(f"Bought {usd_trade_amount} in TQQQ")
        trading_client.submit_order(market_order_data)

    elif trade_decision == 'sell':
        tqqq_trade_amount = tqqq_balance / 2
        market_order_data = MarketOrderRequest(
            symbol='TQQQ',
            qty=tqqq_trade_amount,
            side=OrderSide.SELL,
            type='market',
            time_in_force=TimeInForce.DAY)

        print(f"Sold {tqqq_trade_amount} in TQQQ")
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
    return float(usd_balance)


def get_assets():
    '''
    Retrives the assets from the Alpaca trading account.
    Args:
        None
    Returns:
        bitcoin_balance (dict): A dictionary with details of Bitcoin-related
        assets
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


def main():
    '''
    main function of the bot.
    Args:
        None
    Returns:
        None
    '''
    account_balance = float(account.cash)
    all_assets = get_assets()
    tqqq_asset = get_specified_asset('TQQQ', all_assets)
    tqqq_price = float(tqqq_asset.current_price)
    print(f"TQQQ Balance: {tqqq_asset.qty}")
    print(f"Account balance: {account_balance}")

    # get action
    trade_decision = get_action(account_balance)
    print(f"Trade decision: {trade_decision}")

    # trade
    trade('buy', account_balance, float(tqqq_asset.qty), tqqq_price)


if __name__ == '__main__':
    main()
