from bot import Bot
import sys
import io
from contextlib import contextmanager
import time
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS, cross_origin
from threading import Thread, Event
import json
from datetime import datetime, timedelta

class AiTraderApp:
    def __init__(self):
        self.app = Flask(__name__, static_folder='build', static_url_path='')
        CORS(self.app)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/', defaults={'path': ''})
        @self.app.route('/<path:path>')
        def index(path):
            return send_from_directory(self.app.static_folder, 'index.html')

    def run(self):
        self.app.run(debug=True)

class OutputCapture:
    def __init__(self):
        self.contents = ''

    def write(self, st):
        self.contents += st

    def flush(self):
        pass

output_capture = OutputCapture()
sys.stdout = output_capture

class TradingApp(AiTraderApp):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.trade_stop_event = Event()
        self.trading_state = False
        self.next_trade = 'N/A'
        self.trade_dec = self.bot.get_trade_decision()
        self.bot.set_all()
        self.set_all_thread = Thread(target=self.run_set_all_periodically)
        self.set_all_thread.start()

    def run_set_all_periodically(self):
        while True:
            self.bot.set_all()
            time.sleep(43200)

    def get_trade_decision(self):
        return self.trade_dec
    
    def set_trade_decision(self):
        trade_decision = self.bot.get_trade_decision()
        self.trade_dec = trade_decision

    def continuous_trade(self,days=7):
        while not self.trade_stop_event.is_set():
            self.bot.trader()
            days = float(days)
            self.trading_state = True
            self.next_trade = (datetime.now() + timedelta(days)).strftime("%Y-%m-%d")
            print('next trade:' + self.next_trade)
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
            buying_power = int(buying_power)
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
            asset_balance = round(float(asset_balance), 2)
            return jsonify(({ 'asset_balance': asset_balance }))

        @self.app.route('/get_asset_price')
        def get_asset_price():
            asset_price = self.bot.get_asset_price()
            return jsonify(({ 'asset_price': asset_price }))
        
        @self.app.route('/get_trade_decision')
        def get_trade_decision():
            trade_decision = self.get_trade_decision()
            return jsonify(({ 'trade_decision': trade_decision }))
        
        @self.app.route('/auto_trade')
        def trade():
            self.bot.trade(trade_dec=self.trade_dec)
            response = jsonify({'status': 'Success'})
            return response
        
        @self.app.route('/sell_trade', methods=['POST'])
        def sell_trade():
            data = request.json
            quantity = data['amount']
            quantity = float(quantity)
            if self.bot.trade(asset_sell_quantity=quantity, trade_dec='sell') == 0:
                response = jsonify({'message': 'Insufficient Asset', 'status': 'Success'})
                return response
            response = jsonify({'message': 'Sold {} TQQQ'.format(quantity), 'status': 'Success'})
            return response
        
        @self.app.route('/buy_trade', methods=['POST'])
        def buy_trade():
            data = request.json
            quantity = data['amount']
            quantity = float(quantity)
            if self.bot.trade(asset_buy_quantity=quantity, trade_dec='buy') == 0:
                response = jsonify({'message': 'Insufficient Funds', 'status': 'Success'})
                return response
            response = jsonify({'message': 'Bought {} TQQQ'.format(quantity), 'status': 'Success'})
            return response


        @self.app.route('/stop_trade')
        def stop_trade():
            self.bot.stop_trade()
            response = jsonify({'status': 'Success'})
            return response
        
        @self.app.route('/get_latest_trades')
        def get_latest_trades():
            latest_trades = self.bot.get_trade_history()
            return jsonify(({ 'latest_trades': latest_trades }))
        
        @self.app.route('/get_monthly_history')
        def get_monthly_history():
            self.bot.set_asset_monthly_history()
            monthly_history = self.bot.get_monthly_history()
            return jsonify(({ 'monthly_history': monthly_history }))

        
        @self.app.route('/get_quarterly_history')
        def get_quarter_history():
            self.bot.set_asset_quarter_history()
            quarter_history = self.bot.get_quarter_history()
            return jsonify(({ 'quarter_history': quarter_history }))
        
        @self.app.route('/start_trading', methods=['POST'])
        def start_trading():
            print(self.trade_stop_event.is_set())
            data = request.json
            days = data['days']
            self.trade_stop_event.clear()
            t = Thread(target=self.continuous_trade, args=(days,))
            t.start()
            print(self.trade_stop_event.is_set())
            response = jsonify({'status': 'Success'})
            return response
        
        @self.app.route('/stop_trading')
        def stop_trading():
            self.trade_stop_event.set()
            self.trading_state = False
            response = jsonify({'status': 'Success',})
            return response
        
        @self.app.route('/get_trade_status')
        def get_trade_status():
            status = self.trading_state
            response = jsonify({'status': 'Active' if status else 'Stopped'})
            return response
        
        @self.app.route('/get_total_value')
        def get_total_value():
            total_value = self.bot.get_total_value()
            total_value = round(float(total_value), 2)
            return jsonify(({ 'total_value': total_value }))
        
        @self.app.route('/get_next_trade_date')
        def get_next_trade_date():
            response = jsonify({'next_trade': self.next_trade})
            return response
        
        @self.app.route('/run_trainer', methods=['POST'])
        def run_trainer():
            data = request.json
            start_date = data['start']
            stop_date = data['end']

            # new thread so server doesnt slow down
            def run_trainer_in_thread():
                self.bot.trainer(start=start_date, stop=stop_date)

            thread = Thread(target=run_trainer_in_thread)
            thread.start()

            response = jsonify({'status': 'Success'})
            return response
  
        @self.app.route('/get_console_output')
        def get_console_output():
            return jsonify({"output": output_capture.contents})
        

if __name__ == '__main__':
    my_bot = Bot(secret_key='', key='') 
    app = TradingApp(my_bot)
    app.run()

