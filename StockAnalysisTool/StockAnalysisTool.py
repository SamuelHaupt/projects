import investpy
from datetime import date, timedelta


class StockTable(object):
    """
    Stock contains performance data: price, percent change, volume, numerical change based on a
    duration between two dates.
    """

    def __init__(self, stock_symbol, country='united states', date_from=None, date_to=None):
        """
        Takes in stock_symbol and country (strings). Date_from (string, integer, or defaulted to NoneType) and
        date_to (string or defaulted to NoneType) required format is '%d/%m/%Y'. investpy will throw an error if
        not.
        """
        
        self._stock_symbol = stock_symbol
        self._country = country
        self.set_date_to(date_to) # Reordered to cover defaulted procedures within set_date_from() method.
        self.set_date_from(date_from)
        self._investing_website_stock_data = list()
        self._stock_price_volume_pct_gains_table = list()

        self.setup_stock_table()

    def setup_stock_table(self):
        """
        After initialization of the stock, Stock is converted from pandas.DataFrame into lists with added performance data
        that can be later coded into CSV file format. Performance data includes the addition of price and volume percentage
        gain and loss and volume difference day-to-day.
        """

        stock_symbol = self.get_stock_symbol()
        country = self.get_country()
        date_from = self.get_date_from()
        date_to = self.get_date_to()
        investing_website_stock_data = self.get_investing_website_stock_data()
        stock_price_volume_pct_gains_table = self.get_stock_price_volume_pct_gains_table()

        try:
            investing_website_stock_data = investpy.stocks.get_stock_historical_data(stock_symbol, country, date_from, date_to)
            self.set_investing_website_stock_data(investing_website_stock_data)
        except:
            stock_not_available = None
            return self.set_investing_website_stock_data(stock_not_available)

        trading_date = investing_website_stock_data.reset_index()['Date']
        price_close = investing_website_stock_data['Close'].fillna(0)
        price_pct_change = investing_website_stock_data['Close'].pct_change().fillna(0)
        share_volume = investing_website_stock_data['Volume'].fillna(0)
        share_volume_change = investing_website_stock_data['Volume'].diff().fillna(0)
        share_volume_pct_change = investing_website_stock_data['Volume'].pct_change().fillna(0)
        table_enhanced = list(map(lambda a, b, c, d, e, f: [a, b, round(c, 2), d, int(e), round(f, 2)],\
                         trading_date, price_close, price_pct_change, share_volume, share_volume_change, share_volume_pct_change))
        
        self.set_stock_price_volume_pct_gains_table(table_enhanced)

    def get_stock_symbol(self):
        """
        Returns _stock_symbol.
        """

        return self._stock_symbol.upper()
    
    def get_country(self):
        """
        Returns _country
        """

        return self._country

    def get_date_from(self):
        """
        Returns _date_from
        """

        return self._date_from


    def set_date_from(self, date_from):
        """
        Takes in date_from (string, integer, or NoneType).
        Sets _date_from based on conditions of the parameter.
        NoneType defaults _date_from to a two year look back period and uses set_date_to() to set to today's date.
        Integer is the number of months for look back period and uses set_date_to() to set to today's date.
        String is the actual date for look back period to begin. No changes are forced on _date_to
        """

        # Two year look back period from today is forced if date_from is NoneType.
        if date_from is None:
            date_from = date.today() - timedelta(days=365*2)
            self._date_from = str(date_from.strftime('%d/%m/%Y'))
            self.set_date_to(None)

        # If date_from is an integer and not in string format, date_from is considered to be a duration in months of 31
        # days. Date_to is forced into today's date with correct format.
        elif isinstance(date_from, int):
            date_from = date.today() - timedelta(days=date_from*31)
            self._date_from = str(date_from.strftime('%d/%m/%Y'))
            self.set_date_to(None)

        else:
            self._date_from = date_from

    def get_date_to(self):
        """
        Returns _date_to
        """

        return self._date_to

    def set_date_to(self, date_to):
        """
        Takes in date_from (string or NoneType).
        Sets _date_from based on conditions of the parameter.
        NoneType defaults to today's date.
        String is the actual date for look back period to end.
        """

        # Today's date is used if NoneType is supplied.    
        if date_to is None:
            self._date_to = date.today().strftime('%d/%m/%Y')

        else:
            self._date_to = date_to

    def get_investing_website_stock_data(self):
        """
        Returns Investing.com's stock data from _investing_website_stock_data.
        """

        return self._investing_website_stock_data

    def set_investing_website_stock_data(self, investing_website_stock_data):
        """
        Takes in investing_website_stock_data (list of lists or string) and sets variable.
        String will provide a stock symbol and indicate 
        """

        if investing_website_stock_data is None:
            investing_website_stock_data = print('{} is not available.'.format(self.get_stock_symbol()))
        
        self._investing_website_stock_data = investing_website_stock_data

    def get_stock_price_volume_pct_gains_table(self):
        """
        Returns _stock_price_volume_pct_gains_table.
        """

        return self._stock_price_volume_pct_gains_table

    def set_stock_price_volume_pct_gains_table(self, stock_price_volume_pct_gains_table):
        """
        Takes stock_price_volume_pct_gains_table (list of lists) and sets _stock_price_volume_pct_gains_table to the table.
        """

        self._stock_price_volume_pct_gains_table = stock_price_volume_pct_gains_table

    def __repr__(self):
        """
        Prints to console stock price/volume/gains table.
        """

        stock_price_volume_pct_gains_table = self.get_stock_price_volume_pct_gains_table()
        return '\n'.join(map(str, stock_price_volume_pct_gains_table))