from sb3_contrib import RecurrentPPO
from data_processor import DataProcessor
from asset_trading_env import AssetTradingEnv
import pandas as pd
import alpaca_trade_api as tradeapi
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import date, datetime
from time import sleep
from pytz import timezone

key = ''
secret_key = ''


class Bot:
    def __init__(self, secret_key, key, paper_trade=True,
                 model_path="models/20231110194307_ppo_trading_agent"):
        # Bot variables
        self.symbol = 'TQQQ'
        self.model_path = model_path

        # Account variables
        self.paper_trade = paper_trade
        self.trading_client = TradingClient(key, secret_key, paper=paper_trade)
        self.rest_client = tradeapi.REST(key, secret_key, 
                                         base_url='https://paper-api.alpaca.markets')
        self.stock_historical_data_client = StockHistoricalDataClient(
            key, secret_key)
        self.account = self.trading_client.get_account()
        self.target_asset = None
        self.tqqq_balance = None
        self.account_balance = 0
        self.buying_power = 0
        self.all_assets = None
        self.asset_price = None

        self.trade_decision = None
        self.trade_history = {}
        self.asset_monthly_history = {}
        self.asset_quarter_history = {}
        self.cont_trade = False


    ########################################################
    # SETTERS
    def set_account(self) -> None:
        '''
        Function sets the account.
        '''
        self.account = self.trading_client.get_account()

    def set_buying_power(self) -> float:
        '''
        Function sets the buying power.
        '''
        self.buying_power = float(self.account.buying_power)

    def set_all_assets(self) -> list:
        '''
        Function gets all assets from portfolio.
        '''
        self.all_assets = self.trading_client.get_all_positions()

    def set_target_asset(self) -> None:
        '''
        Function sets the target asset.
        '''
        for asset in self.all_assets:
            if asset.symbol == self.symbol:
                self.target_asset = asset

    def set_asset_balance(self) -> float:
        '''
        Function gets the balance of a specific asset.
        '''
        if self.target_asset is None:
            return 0
        return float(self.target_asset.qty)

    def set_asset_price(self) -> float:
        '''
        This function gets the current price of TQQQ.
        Args:
            None
        Returns:
            Float: current price of TQQQ
        '''
        last_trade = self.rest_client.get_latest_trade(self.symbol)
        self.asset_price = float(last_trade.price)

    def set_account_balance(self) -> float:
        '''
        Function gets the account balance.
        '''
        self.account_balance = float(self.account.cash)

    def set_asset_monthly_history(self) -> None:
        '''
        Function gets the monthly history of the asset.
        '''
        self.asset_monthly_history = {}
        end_date = datetime.now(timezone('UTC')) - pd.Timedelta(days=1)
        start_date = end_date - pd.Timedelta(days=30)
        request_params = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame.Day,
            start=start_date,
            end=end_date
        )
        bars = self.stock_historical_data_client.get_stock_bars(request_params)
        for bar in bars:
            self.asset_monthly_history[bar.timestamp] = bar.close

    def set_asset_quarter_history(self) -> None:
        '''
        Function gets the monthly history of the asset.
        '''
        self.asset_monthly_history = {}
        end_date = datetime.now(timezone('UTC')) - pd.Timedelta(days=1)
        start_date = end_date - pd.Timedelta(days=90)
        request_params = StockBarsRequest(
            symbol_or_symbols=self.symbol,
            timeframe=TimeFrame.Day,
            start=start_date,
            end=end_date
        )
        bars = self.stock_historical_data_client.get_stock_bars(request_params)
        for bar in bars:
            self.asset_quarter_history[bar.timestamp] = bar.close

    def set_all(self) -> None:
        '''
        Function sets all account variables.
        '''
        self.set_buying_power()
        self.set_all_assets()
        self.set_asset_price()
        if len(self.all_assets) == 0:
            self.target_asset = None
            self.tqqq_balance = 0
        else:
            self.set_target_asset()
            self.set_asset_balance()
        self.set_account_balance()
        self.set_asset_monthly_history()
        self.set_asset_quarter_history()
    

    ########################################################
    # GETTERS
    def get_account_balance(self) -> float:
        '''
        Function gets the account balance.
        '''
        return self.account_balance

    def get_buying_power(self) -> float:
        '''
        Function gets the buying power.
        '''
        return self.buying_power

    def get_all_assets(self) -> list:
        '''
        Function gets all assets from portfolio.
        '''
        return self.all_assets

    def get_target_asset(self) -> None:
        '''
        Function gets the target asset.
        '''
        return self.target_asset

    def get_asset_balance(self) -> float:
        '''
        Function gets the balance of a specific asset.
        '''
        if self.target_asset is None:
            return 0
        return self.tqqq_balance

    def get_asset_price(self) -> float:
        '''
        This function gets the current price of TQQQ.
        '''
        return self.asset_price

    def get_trade_decision(self) -> str:
        '''
        Function gets the trade decision.
        '''
        return self.trade_decision
    
    def get_monthly_history(self) -> list:
        '''
        Function gets the monthly history of the asset.
        '''
        return self.asset_monthly_history
    
    def get_quarter_history(self) -> list:
        '''
        Function gets the monthly history of the asset.
        '''
        return self.asset_quarter_history
    
    def get_trade_history(self) -> dict:
        '''
        Function gets the trade history.
        '''
        return self.trade_history
    
    def get_total_value(self) -> float:
        '''
        Function gets the total value of the account.
        '''
        return self.account_balance + self.tqqq_balance * self.asset_price
    
    

    ########################################################
    def set_trade_decision(self) -> str:
        '''
        This function gets the action from the model and returns a trade
        decision.
        Args:
            None
        Returns:
            String: trade decision
        '''
        model = RecurrentPPO.load(self.model_path)
        data_processor = DataProcessor()

        start_date = date.today() - pd.Timedelta(days=1000)
        stop_date = date.today() - pd.Timedelta(days=1)

        tqqq = data_processor.download_data_df_from_yf(
            self.symbol, start_date, stop_date)
        trading_df = data_processor.preprocess_data(tqqq)
        trading_df.dropna(inplace=True)
        trading_env = AssetTradingEnv(
            data_df=trading_df,
            initial_balance=self.account_balance)

        observation = trading_env._get_obs()

        # get action from the model
        action, lstm_states = model.predict(observation)

        print(f"Action: {action}")
        if action == 1:
            self.trade_decision = 'buy'
        elif action == 0:
            self.trade_decision = 'sell'
        else:
            self.trade_decision = 'hold'
        print(f"Trade decision: {self.trade_decision}")

    def trade(self, asset_buy_quantity=None, asset_sell_quantity=None,
              trade_dec=None) -> None:
        '''
        Function to perform the trade
        '''
        if trade_dec is None:
            trade_dec = self.get_trade_decision()

        if trade_dec == 'buy':
            if asset_buy_quantity is None:
                asset_buy_quantity = (
                    self.account_balance / 2) / self.asset_price
            elif asset_buy_quantity > (
                    self.account_balance) / self.asset_price:
                print("Not enough money to buy that much")
                return
            market_order_data = MarketOrderRequest(
                symbol=self.symbol,
                qty=asset_buy_quantity,
                side=OrderSide.BUY,
                type='market',
                time_in_force=TimeInForce.DAY
            )
            self.trading_client.submit_order(market_order_data)
            print(f"Bought {asset_buy_quantity} in {self.symbol}")
            self.trade_history[str(date.today())+'buy'] = asset_buy_quantity

        elif trade_dec == 'sell':
            if self.tqqq_balance is None:
                return
            if asset_sell_quantity is None:
                asset_sell_quantity = self.tqqq_balance / 2
            elif asset_sell_quantity > self.tqqq_balance:
                print("Not enough assets to sell that much")
                return
            market_order_data = MarketOrderRequest(
                symbol=self.symbol,
                qty=asset_sell_quantity,
                side=OrderSide.SELL,
                type='market',
                time_in_force=TimeInForce.DAY
            )
            self.trading_client.submit_order(market_order_data)
            print(f"Sold {asset_sell_quantity} in {self.symbol}")
            self.trade_history[str(date.today())+'sell'] = asset_sell_quantity

        else:
            print('Holding position')
            self.trade_history[str(date.today())+'hold'] = 0

    def trader(self) -> None:
        '''
        Function that sets up a single trade.
        '''
        self.set_all()
        self.get_trade_decision()
        self.trade()

    def continuous_trade_test(self, days=7) -> None:
        '''
        Function to perform multiple trades
        '''
        while not self.stop_event.is_set():
            self.trader()
            self.stop_event.wait(days * 24 * 60 * 60)


def main():
    '''
    main function of the bot.
    Args:
        None
    Returns:
        None
    '''
    bot = Bot(secret_key, key)
    bot.trader()


if __name__ == '__main__':
    main()
