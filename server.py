from bot import Bot
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from threading import Thread, Event
import json
from datetime import datetime, timedelta


class AiTraderApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, resources={r"/*": {"origins": "*"}})
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
        self.next_trade = 'N/A'
        bot.set_all()
        bot.get_trade_decision()


    def continuous_trade(self,days=7):
        while not self.trade_stop_event.is_set():
            self.bot.trader()
            self.next_trade = (datetime.now() + timedelta(days)).strftime("%Y-%m-%d")
            self.trade_stop_event.wait(days * 24 * 60 * 60)

    def setup_routes(self):
        super().setup_routes()

        @self.app.route('/get_account_balance')
        def get_account_balance():
            balance = self.bot.get_account_balance()
            return jsonify(({ 'balance': balance }))
        
        @self.app.route('/get_buying_power')
        def get_buying_power():
            buying_power = self.bot.get_buying_power()
            return jsonify(({ 'buying_power': buying_power }))
        
        @self.app.route('/get_all_assets')
        def get_all_assets():
            all_assets = self.bot.get_all_assets()
            return jsonify(({ 'all_assets': all_assets }))
        
        @self.app.route('/get_target_asset')
        def get_target_asset():
            target_asset = self.bot.get_target_asset()
            return jsonify(({ 'target_asset': target_asset }))
        
        @self.app.route('/get_asset_balance')
        def get_asset_balance():
            asset_balance = self.bot.get_asset_balance()
            return jsonify(({ 'asset_balance': asset_balance }))

        @self.app.route('/get_asset_price')
        def get_asset_price():
            asset_price = self.bot.get_asset_price()
            return jsonify(({ 'asset_price': asset_price }))
        
        @self.app.route('/get_trade_decision')
        def get_trade_decision():
            trade_decision = self.bot.get_trade_decision()
            self.trade_dec = trade_decision
            print(str(trade_decision) + "55555")
            return jsonify(({ 'trade_decision': trade_decision }))
        
        @self.app.route('/auto_trade')
        def trade():
            
            self.bot.trade()
            return "Success"
        
        @self.app.route('/sell_trade')
        @cross_origin()
        def sell_trade(quantity):
            quantity = request.args.get('quantity')
            self.bot.sell_trade(asset_sell_quantity=quantity, trade_decision='sell')
            return "Success"
        
        @self.app.route('/buy_trade')
        def buy_trade(quantity):
            quantity = request.args.get('quantity')
            self.bot.buy_trade(asset_buy_quantity=quantity, trade_decision='buy')
            return "Success"
        
        @self.app.route('/stop_trade')
        def stop_trade():
            self.bot.stop_trade()
            return "Stopped"
        
        @self.app.route('/get_latest_trades')
        def get_latest_trades():
            latest_trades = self.bot.get_trade_history()
            return jsonify(({ 'latest_trades': latest_trades }))
        
        @self.app.route('/get_monthly_history')
        def get_monthly_history():
            montkly_history = self.bot.get_monthly_history()
            return jsonify(({ 'monthly_history': montkly_history }))

        
        @self.app.route('/get_quarterly_history')
        def get_quarter_history():
            quarter_history = self.bot.get_quarter_history()
            return jsonify(({ 'quarter_history': quarter_history }))
        
        @self.app.route('/start_trading')
        def start_trading(days):
            days = request.args.get('days')
            self.trade_stop_event.clear()
            t = Thread(target=self.continuous_trade, args=(days))
            t.start()
            return "Trading started"
        
        @self.app.route('/stop_trading')
        def stop_trading():
            self.trade_stop_event.set()
            return "Trading stopped"
        
        @self.app.route('/get_trade_status')
        def get_trade_status():
            return str(not self.trade_stop_event.is_set())
        
        @self.app.route('/get_total_value')
        def get_total_value():
            total_value = self.bot.get_total_value()
            return jsonify(({ 'total_value': total_value }))
        
        @self.app.route('/get_next_trade_date')
        def get_next_trade_date():
            return self.next_trade
        

if __name__ == '__main__':
    my_bot = Bot(secret_key='KcjdBN7YUwdLYxDwhmHLMGeuU44FOG67ASdMp3uE', key='PKIS1O7AVH1BVIXTP2Z0') 
    app = TradingApp(my_bot)
    app.run()

