import investpy
from datetime import date, timedelta
from operator import itemgetter
import csv
import random
from pprint import pprint
from copy import copy, deepcopy


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


class StockAnalysisTool(StockTable):
    """
    Analysizes many stocks to determine price action move gains based on specific 
    """

    def __init__(self, stock_symbol, country='united states', date_from=None, date_to=None, price_action_move_filter=None, volume_change_filter=None):
        """
        Initializes all available stocks within USA.
        """
        super().__init__(stock_symbol, country, date_from, date_to)
        self._price_action_move_filter = price_action_move_filter
        self._volume_change_filter = volume_change_filter
        self._stock_performance_for_up_to_five_day_trades_list = None
        self._total_stock_performance_for_trade_duration_after_specified_days_list = None

        self.setup_stock_anaylsis_tool()

    def setup_stock_anaylsis_tool(self):
        """
        Setup StockTable to include Boolean based on price_action_move_filter and volume_change_filter.
        """

        price_action_move_filter = self.get_price_action_move_filter()
        volume_change_filter = self.get_volume_change_filter()

        self.set_price_volume_action_table(price_action_move_filter, volume_change_filter)

    def get_price_action_move_filter(self):
        """
        Returns _price_action_move_filter.
        """

        return self._price_action_move_filter

    def set_price_action_move_filter(self, price_action_move_filter):
        """
        Takes in price_action_move_filter (NoneType or negative percentage in decimal form) and sets
        variable.
        """

        self._price_action_move_filter = price_action_move_filter

    def get_volume_change_filter(self):
        """
        Returns _volume_change_filter.
        """

        return self._volume_change_filter

    def set_volume_change_filter(self, volume_change_filter):
        """
        Takes in volume_change_filter (Boolean) as True or None and sets
        variable.
        """

        self._volume_change_filter = volume_change_filter

    def get_stock_performance_for_up_to_five_day_trades_list(self):
        """
        Returns _stock_performance_for_up_to_five_day_trades_list.
        """

        return self._stock_performance_for_up_to_five_day_trades_list

    def set_stock_performance_for_up_to_five_day_trades_list(self, stock_performance_for_up_to_five_day_trades_list):
        """
        Takes in listed results for get_stock_performance_for_up_to_five_day_trades() and set variable.
        """

        self._stock_performance_for_up_to_five_day_trades_list = stock_performance_for_up_to_five_day_trades_list

    def get_total_stock_performance_for_trade_duration_after_specified_days_list(self):
        """
        Returns _total_stock_performance_for_trade_duration_after_specified_days_list.
        """

        return self._total_stock_performance_for_trade_duration_after_specified_days_list

    def append_total_stock_performance_for_trade_duration_after_specified_days_list(self, total_stock_performance_for_trade_duration_after_specified_days_list):
        """
        Takes in listed results for get_stock_performance_for_up_to_five_day_trades() and appends to variable.
        """

        if self._total_stock_performance_for_trade_duration_after_specified_days_list is None:
            self._total_stock_performance_for_trade_duration_after_specified_days_list = list()

        self._total_stock_performance_for_trade_duration_after_specified_days_list.append(total_stock_performance_for_trade_duration_after_specified_days_list)

    def set_price_volume_action_table(self, price_action_move_filter=None, volume_change_filter=None):
        """
        Takes in price_action_move_filter (integer) and volume_change_filter (Boolean).
        Price_action_move_filter is a negative percent in decimal form below which stock percentage changes are measured.
        Volumne_change_filer allows for volume change to be checked along with price action move, but only if
        price_action_move_filter is not NoneType.
        """

        self.set_price_action_move_filter(price_action_move_filter)
        self.set_volume_change_filter(volume_change_filter)

        stock_price_volume_pct_gains_table = self.get_stock_price_volume_pct_gains_table()
        total_trading_days = len(stock_price_volume_pct_gains_table)
        price_action_move_list = list()
        volume_action_move_list = list()

        if price_action_move_filter is not None:
            price_action_move_list = [True if trading_day[2] <= price_action_move_filter else False for trading_day in stock_price_volume_pct_gains_table]
            
            if volume_change_filter is True:
                for index in range(total_trading_days):

                    try:
                        volume_change = stock_price_volume_pct_gains_table[index+1][4]
                        if price_action_move_list[index] is True and volume_change < 0:
                            volume_action_move_list.append(True)

                        else:
                            volume_action_move_list.append(False)

                    except:
                        volume_action_move_list.append(False)

        if not price_action_move_list or isinstance(price_action_move_filter, bool):
            price_action_move_list = [None for index in range(total_trading_days)]
        if not volume_action_move_list:
            volume_action_move_list = [None for index in range(total_trading_days)]

        for index, trading_day in enumerate(stock_price_volume_pct_gains_table):
            trading_day.append(price_action_move_list[index])
            trading_day.append(volume_action_move_list[index])

        return stock_price_volume_pct_gains_table

    def calculate_gains(self, start_pct_gains, second_percentage):
        """
        Takes in start_pct_gains and second_percentage (floats) in decimal form.
        Returns sum of total percentage gained.

        Uses formula:
        total_change = a+b + a*b # from [(value*(1 + a)*(1+b) - value)/(value)]

        Important references:
        [Percentage changes](https://towardsdatascience.com/most-people-screw-up-multiple-percent-changes-heres-how-to-do-get-them-right-b86bd6ef4b72)
        """

        a = start_pct_gains
        b = second_percentage
        total_change = a+b + a*b

        return total_change

    def set_total_stock_performance_five_days_following_percentage_drop(self):
        """
        Takes in no parameters.
        Produces stock performance results based on whether price_action_move column is true
        or price_action_move and volume_action_move columns are True.
        Uses set_stock_performance_for_up_to_five_day_trades() method to set results to private variable.
        
        Results:
         #0 (string)    #1 (list of len(5); float in dec form)   #2 (float in dec form) 
        [trade_pattern, combined_trades_five_day_pct_gains_list, total_stock_pct_gains,\
         #3 (int)      #4 (int) 
         trades_count, total_days_for_lookback_count,\
         #5 (list of len(5); int)      #6 (int)          #7 (int)           #8 (float in dec form)
         summed_trade_days_count_list, trade_wins_count, trade_loses_count, trade_wins_count/trades_count,\
         #9 (float in dec form)                   #10 (float in dec form)
         winning_trades_pct_gain_per_trades_count, winning_trades_pct_gain_per_total_days_five_day_trades,\
         #11 (float in dec form)
         total_stock_gains_per_total_days_for_lookback_period]
        """

        if isinstance(self.get_price_action_move_filter(), bool) or self.get_price_action_move_filter() is None:
            return 'Unable to process. Run set_price_volume_action_table() with at least price action move filter.'

        stock_price_volume_pct_gains_table = self.get_stock_price_volume_pct_gains_table()
        stock_symbol = self.get_stock_symbol()
        volume_change_filter = self.get_volume_change_filter()

        combined_trades_five_day_pct_gains_list = [0.00, 0.00, 0.00, 0.00, 0.00]
        total_stock_pct_gains = 0.0

        trades_count = 0
        trade_wins_count = 0
        trade_loses_count = 0
        actual_trade_day_index = 0

        total_days_one_day_trades = 0
        total_days_two_day_trades = 0
        total_days_three_day_trades = 0
        total_days_four_day_trades = 0
        total_days_five_day_trades = 0

        for index_stock_table, trade_day in enumerate(stock_price_volume_pct_gains_table):
            pct_drop_requested = trade_day[6]
            volume_negative_requested = trade_day[7]
            single_trade_five_day_gains_list = [0.00, 0.00, 0.00, 0.00, 0.00]
            total_stock_pct_gains = self.calculate_gains(total_stock_pct_gains,trade_day[2])
            
            if not volume_change_filter:
                conduct_trade = pct_drop_requested is True and actual_trade_day_index == index_stock_table
            else:
                conduct_trade = pct_drop_requested is True and volume_negative_requested is True and actual_trade_day_index == index_stock_table
                       
            day_to_measure = 0

            if conduct_trade:
                trades_count += 1
                stop_out_trade = False
                while_index = 0

                while stop_out_trade is False and while_index < 5:
                    day_to_measure = while_index + 1
                    if while_index == 0:
                        start_pct_gains = 0
                    else:
                        start_pct_gains = single_trade_five_day_gains_list[while_index-1]

                    try:
                        stock_price_volume_pct_gains_table[index_stock_table+day_to_measure+1]
                    except:
                        stop_out_trade = True

                    second_pct = stock_price_volume_pct_gains_table[index_stock_table+day_to_measure][2]
                    pct_change = self.calculate_gains(start_pct_gains, second_pct)

                    if pct_change <= -0.02:
                        single_trade_five_day_gains_list[while_index] = -0.02
                        stop_out_trade = True
                        trade_loses_count += 1

                    else:
                        single_trade_five_day_gains_list[while_index] = pct_change

                    while_index += 1

                    if while_index == 1:
                        total_days_one_day_trades += 1
                    elif while_index == 2:
                        total_days_two_day_trades += 1
                    elif while_index == 3:
                        total_days_three_day_trades += 1
                    elif while_index == 4:
                        total_days_four_day_trades += 1
                    elif while_index == 5:
                        total_days_five_day_trades += 1
                        if not stop_out_trade:
                            trade_wins_count += 1

                for index in range(5):
                    total_calculated_percent = combined_trades_five_day_pct_gains_list[index]
                    pct_change = single_trade_five_day_gains_list[index]
                    updated_change = self.calculate_gains(total_calculated_percent,pct_change)
                    combined_trades_five_day_pct_gains_list[index] = updated_change

            trade_day.extend(single_trade_five_day_gains_list)
        
            if day_to_measure != 0:
                actual_trade_day_index += 1+day_to_measure
            elif actual_trade_day_index == index_stock_table:
                actual_trade_day_index += 1

            # if index_stock_table == 3000:
            #     break

        if sum(combined_trades_five_day_pct_gains_list) == 0:
            print('No trades executed for {}.'.format(stock_symbol))
            return

        trade_days_count = [total_days_one_day_trades, total_days_two_day_trades, total_days_three_day_trades, total_days_four_day_trades, total_days_five_day_trades]
        total_days_five_day_trades = sum(trade_days_count[0:5])
        total_days_four_day_trades = sum(trade_days_count[0:4])
        total_days_three_day_trades = sum(trade_days_count[0:3])
        total_days_two_day_trades = sum(trade_days_count[0:2])
        total_days_one_day_trades = sum(trade_days_count[0:1])
        summed_trade_days_count_list = [total_days_one_day_trades, total_days_two_day_trades, total_days_three_day_trades, total_days_four_day_trades, total_days_five_day_trades]
        total_days_for_lookback_count = actual_trade_day_index

        # Winning trades are the trades held for five days with a gain greater than -0.02.
        five_day_pct_gains = combined_trades_five_day_pct_gains_list[-1]
        winning_trades_pct_gain_per_trades_count = five_day_pct_gains/trades_count
        winning_trades_pct_gain_per_total_days_five_day_trades = five_day_pct_gains/total_days_five_day_trades
        total_stock_gains_per_total_days_for_lookback_period = total_stock_pct_gains/total_days_for_lookback_count
        trade_pattern = '{}&{}'.format(1, 5)

                   #0 (string)    #1 (list of len(5); float in dec form)   #2 (float in dec form) 
        results = [trade_pattern, combined_trades_five_day_pct_gains_list, total_stock_pct_gains,\
                   #3 (int)      #4 (int) 
                   trades_count, total_days_for_lookback_count,\
                   #5 (list of len(5); int)      #6 (int)          #7 (int)           #8 (float in dec form)
                   summed_trade_days_count_list, trade_wins_count, trade_loses_count, trade_wins_count/trades_count,\
                   #9 (float in dec form)                   #10 (float in dec form)
                   winning_trades_pct_gain_per_trades_count, winning_trades_pct_gain_per_total_days_five_day_trades,\
                   #11 (float in dec form)
                   total_stock_gains_per_total_days_for_lookback_period]

        self.set_stock_performance_for_up_to_five_day_trades_list(results)
        # return results

    def set_total_stock_performance_for_trade_duration_after_specified_days(self, start_day, trade_duration):
        """
        Takes in start_day and trade_duration (integers).
        Produces stock performance results based on whether price_action_move column is true
        or price_action_move and volume_action_move columns are True.
        ######Uses set_stock_performance_for_up_to_five_day_trades() method to set results to private variable.
        
        Results:
         #0 (float in dec form)      #1 (float in dec form) 
        [combined_trades_pct_gains, total_stock_pct_gains,\

         #2 (int)      #3 (int) 
         trades_count, total_days_for_lookback_count,\

         #4 (int)                #5 (int)          #6 (int)           #7 (float in dec form)
         total_trade_days_count, trade_wins_count, trade_loses_count, trade_wins_count/trades_count,\

         #8 (float in dec form)                   #9 (float in dec form)
         winning_trades_pct_gain_per_trades_count, winning_trades_pct_gain_per_total_days_traded,\

         #10 (float in dec form)
         total_stock_gains_per_total_days_for_lookback_period]
        """

        if isinstance(self.get_price_action_move_filter(), bool) or self.get_price_action_move_filter() is None:
            return 'Unable to process. Run set_price_volume_action_table() with at least price action move filter.'

        # Use when adding to StockTable. Use only if managed further down within other classes.
        # elif self.get_stock_performance_for_up_to_five_day_trades() is None:
        #     return 'Unable to process. Run set_total_stock_performance_five_days_following_percentage_drop().'

        stock_price_volume_pct_gains_table = self.get_stock_price_volume_pct_gains_table()
        stock_symbol = self.get_stock_symbol()
        volume_change_filter = self.get_volume_change_filter()

        combined_trades_pct_gains = 0.0
        total_stock_pct_gains = 0.0

        trades_count = 0
        trade_wins_count = 0
        trade_loses_count = 0
        total_trade_days_count = 0
        actual_trade_day_index = 0
        
        for index_stock_table, trade_day in enumerate(stock_price_volume_pct_gains_table):
            pct_drop_requested = trade_day[6]
            volume_negative_requested = trade_day[7]
            single_trade_pct_gains = 0.0
            total_stock_pct_gains = self.calculate_gains(total_stock_pct_gains,trade_day[2])
            
            if not volume_change_filter:
                conduct_trade = pct_drop_requested is True and actual_trade_day_index == index_stock_table
            else:
                conduct_trade = pct_drop_requested is True and volume_negative_requested is True and actual_trade_day_index == index_stock_table
                       
            day_to_measure = 0

            if conduct_trade:
                trades_count += 1
                stop_out_trade = False
                while_index = 0

                while stop_out_trade is False and while_index < trade_duration:
                    total_trade_days_count += 1
                    day_to_measure = while_index
                    
                    try:
                        stock_price_volume_pct_gains_table[index_stock_table+start_day+day_to_measure]
                    except:
                        stop_out_trade = True
                    
                    # Add if stop_out_trade is False to fix index Error.
                    if stop_out_trade is False:
                        start_pct_gains = single_trade_pct_gains
                        second_pct = stock_price_volume_pct_gains_table[index_stock_table+start_day+day_to_measure][2]
                        pct_change = self.calculate_gains(start_pct_gains, second_pct)

                        # # NO STOP LOSS
                        # single_trade_pct_gains = pct_change

                        # STOP LOSS
                        if pct_change <= -0.02:
                            single_trade_pct_gains = self.calculate_gains(start_pct_gains, -0.02)
                            stop_out_trade = True
                            trade_loses_count += 1
                        else:
                            single_trade_pct_gains = pct_change

                        while_index += 1

                        # If trade survives past the 4th day, then trade is a win.
                        if while_index == 5:
                            if not stop_out_trade:
                                trade_wins_count += 1

                combined_trades_pct_gains = self.calculate_gains(combined_trades_pct_gains, single_trade_pct_gains)

            # Adds to StockTable. Use only if managed further down within other classes.
            # trade_day.extend([single_trade_pct_gains])
        
            if day_to_measure != 0:
                actual_trade_day_index += 1+day_to_measure
            elif actual_trade_day_index == index_stock_table:
                actual_trade_day_index += 1

        if combined_trades_pct_gains == 0:
            # pri nt('No trades executed for {}.'.format(stock_symbol))
            return

        total_days_for_lookback_count = actual_trade_day_index

        # Winning trades are the trades held for five days with a gain greater than -0.02.
        winning_trades_pct_gain_per_trades_count = combined_trades_pct_gains/trades_count
        winning_trades_pct_gain_per_total_days_traded = combined_trades_pct_gains/total_trade_days_count
        total_stock_gains_per_total_days_for_lookback_period = total_stock_pct_gains/total_days_for_lookback_count
        trade_pattern = [start_day, trade_duration]
        ###### Winning trades pct gain is not consistent. Fix definition.
                   #0 (list)    #1 (float in dec form)      #2 (float in dec form) 
        results = [trade_pattern, combined_trades_pct_gains, total_stock_pct_gains,\
                   #3 (int)      #4 (int) 
                   trades_count, total_days_for_lookback_count,\
                   #5 (int)                #6 (int)          #7 (int)           #8 (float in dec form)
                   total_trade_days_count, trade_wins_count, trade_loses_count, trade_wins_count/trades_count,\
                   #9 (float in dec form)                   #10 (float in dec form)
                   winning_trades_pct_gain_per_trades_count, winning_trades_pct_gain_per_total_days_traded,\
                   #11 (float in dec form)
                   total_stock_gains_per_total_days_for_lookback_period]

        self.append_total_stock_performance_for_trade_duration_after_specified_days_list(results)

    def sort_total_stock_performance_for_trade_duration_after_specified_days_return_pattern(self, sort_item_index):
        """
        """

        list_to_sort = self.get_total_stock_performance_for_trade_duration_after_specified_days_list()
        if list_to_sort is None:
            pass
        else:
            sorted_list = sorted(list_to_sort, key=itemgetter(sort_item_index), reverse=True)[:1]
            highest_three_patterns = list()
            for index in sorted_list:
                highest_three_patterns.append(index[0])
        
            return (highest_three_patterns[0][0], highest_three_patterns[0][1])

    def sort_total_stock_performance_for_trade_duration_after_specified_days_return_pct_per_trade_day(self, sort_item_index):
        """
        """

        list_to_sort = self.get_total_stock_performance_for_trade_duration_after_specified_days_list()
        if list_to_sort is None:
            pass
        else:
            highest_pct_gained_per_trade_day = sorted(list_to_sort, key=itemgetter(sort_item_index), reverse=True)[10:11][0]
            
        
            return (highest_pct_gained_per_trade_day[0], highest_pct_gained_per_trade_day[10]) 

    def write_findings_to_csv(self):
        """
        Takes in list of findings and writes findings to CSV file.
        """

        findings_list = list()
        stock_performance_for_up_to_five_day_trades_list = self.get_stock_performance_for_up_to_five_day_trades_list()
        total_stock_performance_for_trade_duration_after_specified_days_list = self.get_total_stock_performance_for_trade_duration_after_specified_days_list()
        if stock_performance_for_up_to_five_day_trades_list is not None:
            findings_list.append(stock_performance_for_up_to_five_day_trades_list)
        
        if total_stock_performance_for_trade_duration_after_specified_days_list is not None:
            for trade_pattern in total_stock_performance_for_trade_duration_after_specified_days_list:
                findings_list.append(trade_pattern)

        with open('StockAnalysisTool.csv', 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(findings_list)

    def __str__(self):
        """
        Prints comprehensive analysis results.
        """

        stock_symbol = self.get_stock_symbol()
        date_from, date_to = self.get_date_from(), self.get_date_to()

        stock_performance_for_up_to_five_day_trades_list = self.get_stock_performance_for_up_to_five_day_trades_list()
        if stock_performance_for_up_to_five_day_trades_list is not None:

            trade_pattern = stock_performance_for_up_to_five_day_trades_list[0]
            trades_count = stock_performance_for_up_to_five_day_trades_list[3]

            combined_trades_five_day_pct_gains_list = stock_performance_for_up_to_five_day_trades_list[1]
            one_day_pct_gains, two_day_pct_gains, three_day_pct_gains, four_day_pct_gains, five_day_pct_gains = combined_trades_five_day_pct_gains_list

            summed_trade_days_count_list = stock_performance_for_up_to_five_day_trades_list[5]
            total_days_one_day_trades, total_days_two_day_trades, total_days_three_day_trades, total_days_four_day_trades, total_days_five_day_trades = summed_trade_days_count_list
            
            total_stock_pct_gains = stock_performance_for_up_to_five_day_trades_list[2]
            total_days_for_lookback_count = stock_performance_for_up_to_five_day_trades_list[4]

            print()
            print('For stock symbol: ', stock_symbol)
            print('For trade pattern: ', trade_pattern)
            print('Trade lookback window is from {} to {}'.format(date_from, date_to))
            print()
            print('For a total', trades_count, 'trades, your investment would yield:')
            print('Holding for 1 days resulted in: ', ' '.join(['{:,}'.format(int(one_day_pct_gains*100)),'%']), ' with total invested days: ', total_days_one_day_trades)
            print('Holding for 2 days resulted in: ', ' '.join(['{:,}'.format(int(two_day_pct_gains*100)),'%']), ' with total invested days: ', total_days_two_day_trades)
            print('Holding for 3 days resulted in: ', ' '.join(['{:,}'.format(int(three_day_pct_gains*100)),'%']), ' with total invested days: ', total_days_three_day_trades)
            print('Holding for 4 days resulted in: ', ' '.join(['{:,}'.format(int(four_day_pct_gains*100)),'%']), ' with total invested days: ', total_days_four_day_trades)
            print('Holding for 5 days resulted in: ', ' '.join(['{:,}'.format(int(five_day_pct_gains*100)),'%']), ' with total invested days: ', total_days_five_day_trades)
            print()
            print('Total Stock Change: ', ' '.join(['{:,}'.format(int(total_stock_pct_gains*100)),'%']), ' with total invested days: ', total_days_for_lookback_count)
            print()
            print('Investing $100k will generate', ''.join(['$', '{:,}'.format(int((five_day_pct_gains+1)*100000))]), 'for a 5 day holding scenario.')
            print('versus generating', ''.join(['$', '{:,}'.format(int((total_stock_pct_gains+1)*100000))]), 'for an entire duration scenario.')
            print()
            print('Total percentage gained per roundtrip traded: ', ' '.join(['{:,}'.format(round(five_day_pct_gains*100/trades_count,2)),'%']),'per roundtrip traded.')
            print('Total percentage gained per day held: ', ' '.join(['{:,}'.format(round(five_day_pct_gains*100/total_days_five_day_trades,2)),'%']),'per day held.')
            print('Fully invested total percentage gained per day held: ', ' '.join(['{:,}'.format(round(total_stock_pct_gains*100/total_days_for_lookback_count,2)),'%']),'per day held.')
            print()

        total_stock_performance_for_trade_duration_after_specified_days_list = self.get_total_stock_performance_for_trade_duration_after_specified_days_list()
        if total_stock_performance_for_trade_duration_after_specified_days_list is not None:
            for trade_pattern in total_stock_performance_for_trade_duration_after_specified_days_list:

                trade_pattern_start_day, trade_pattern_duration_days = trade_pattern[0]
                trades_count = trade_pattern[3]

                combined_trades_pct_gains = trade_pattern[1]
                total_trade_days_count = trade_pattern[5]
                
                total_stock_pct_gains = trade_pattern[2]
                total_days_for_lookback_count = trade_pattern[4]

                print()
                print('For stock symbol: ', stock_symbol)
                print('For trade pattern: ', '{}&{}'.format(trade_pattern_start_day, trade_pattern_duration_days))
                print('Trade lookback window is from {} to {}'.format(date_from, date_to))
                print()
                print('For a total', trades_count, 'trades, your investment would yield:')
                print('Starting day {} and holding for {} days resulted in: '.format(trade_pattern_start_day, trade_pattern_duration_days),\
                      ' '.join(['{:,}'.format(int(combined_trades_pct_gains*100)),'%']), ' with total invested days: ', total_trade_days_count)
                print()
                print('Total Stock Change: ', ' '.join(['{:,}'.format(int(total_stock_pct_gains*100)),'%']), ' with total invested days: ', total_days_for_lookback_count)
                print()
                print('Investing $100k will generate', ''.join(['$', '{:,}.'.format(int((combined_trades_pct_gains+1)*100000))]))
                print('versus generating', ''.join(['$', '{:,}'.format(int((total_stock_pct_gains+1)*100000))]), 'for an entire duration scenario.')
                print()
                print('Total percentage gained per roundtrip traded: ', ' '.join(['{:,}'.format(round(combined_trades_pct_gains*100/trades_count,2)),'%']),'per roundtrip traded.')
                print('Total percentage gained per day held: ', ' '.join(['{:,}'.format(round(combined_trades_pct_gains*100/total_trade_days_count,2)),'%']),'per day held.')
                print('Fully invested total percentage gained per day held: ', ' '.join(['{:,}'.format(round(total_stock_pct_gains*100/total_days_for_lookback_count,2)),'%']),'per day held.')
                print()

        return str()

def main():
    """
    Main function.
    """
    # stock = StockTable('aapl', 'united states', '01/01/2020', '03/01/2021') ## Not needed, but shows functionality.
    stock = StockAnalysisTool('aapl', date_from='01/01/2020', date_to=None, price_action_move_filter=-0.05, volume_change_filter=None)
    stock.set_total_stock_performance_five_days_following_percentage_drop()
    print(stock)


# Tests whether file is ran as script and whether the main function ought be called.
if __name__ == '__main__':

    main()