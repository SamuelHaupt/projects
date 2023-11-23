from bot import Bot
from flask import Flask
from threading import Thread, Event
import json


class AiTraderApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return "Ai Trader App"

    def run(self):
        self.app.run(debug=True)


class TradingApp(AiTraderApp):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.trade_stop_event = Event()

    def continuous_trade(self,days=7):
        while not self.trade_stop_event.is_set():
            self.bot.trader()
            self.trade_stop_event.wait(days * 24 * 60 * 60)

    def setup_routes(self):
        super().setup_routes()

        @self.app.route('/get_balance')
        def get_balance():
            return str(self.bot.get_account_balance())
        
        @self.app.route('/get_buying_power')
        def get_buying_power():
            return str(self.bot.get_buying_power())
        
        @self.app.route('/get_all_assets')
        def get_all_assets():
            return str(self.bot.get_all_assets())
        
        @self.app.route('/get_target_asset')
        def get_target_asset():
            return str(self.bot.get_target_asset())
        
        @self.app.route('/get_asset_balance')
        def get_asset_balance():
            return str(self.bot.get_asset_balance())
        
        @self.app.route('/get_asset_price')
        def get_asset_price():
            return str(self.bot.get_asset_price())
        
        @self.app.route('/get_trade_decision')
        def get_trade_decision():
            return str(self.bot.get_trade_decision())
        
        @self.app.route('/auto_trade')
        def trade():
            self.bot.trade()
            return "Trade Successful"
        
        @self.app.route('/sell_trade/<int:quantity>')
        def sell_trade(quantity):
            self.bot.sell_trade(asset_sell_quantity=quantity, trade_decision='sell')
            return "Sell Successful"
        
        @self.app.route('/buy_trade/<int:quantity>')
        def buy_trade(quantity):
            self.bot.buy_trade(asset_buy_quantity=quantity, trade_decision='buy')
            return "Buy Successful"
        
        @self.app.route('/stop_trade')
        def stop_trade():
            self.bot.stop_trade()
            return "Trade Stopped"
        
        @self.app.route('/get_trade_status')
        def get_trade_status():
            return str(self.bot.get_trade_status())
        
        @self.app.route('/get_trade_history')
        def get_trade_history():
            return str(self.bot.get_trade_history())
        
        @self.app.route('/get_trade_history')
        def get_trade_history():
            return str(self.bot.get_trade_history())
        
        @self.app.route('/get_monthly_history')
        def get_monthly_history():
            return str(self.bot.get_monthly_history())
        
        @self.app.route('/get_quarter_history')
        def get_quarter_history():
            return str(self.bot.get_quarter_history())
        
        @app.route('/start_trading/<int:days>')
        def start_trading(days):
            self.trade_stop_event.clear()
            t = Thread(target=self.continuous_trade, args=(days))
            t.start()
            return "Trading started"
        
        @app.route('/stop_trading')
        def stop_trading():
            self.trade_stop_event.set()
            return "Trading stopped"
        
        @app.route('/get_trading_status')
        def get_trading_status():
            return str(not self.trade_stop_event.is_set())
        

if __name__ == '__main__':
    my_bot = Bot(secret_key='', key='') 
    app = TradingApp(my_bot)
    app.run()

