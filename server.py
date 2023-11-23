import flask
from bot import Bot


from flask import Flask

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
        self.bot.set_account()

    def setup_routes(self):
        super().setup_routes()

        @self.app.route('/get_balance')
        def get_balance():
            return str(self.bot.get_account_balance())

if __name__ == '__main__':
    my_bot = Bot(secret_key='KcjdBN7YUwdLYxDwhmHLMGeuU44FOG67ASdMp3uE', key='PKIS1O7AVH1BVIXTP2Z0') 
    app = TradingApp(my_bot)
    app.run()

