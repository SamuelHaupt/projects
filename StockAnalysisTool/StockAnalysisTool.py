import json
import csv

class CanonTrades(object):
    """

    """

    def __init__(self, csv_file):
        """
        Takes in no parameters.
        Pulls in stock.csv to be searched.
        """

        self._stock_data = list()

        with open(csv_file, 'r', newline='') as infile:

            for row in list(csv.reader(infile)):

                if not '-' in row[5]:

                    self._stock_data.append(row)


    def get_stock_data(self):
        """
        Returns _stock_data (list of lists).
        """

        return self._stock_data

    def get_actual_volume_size(self, abbreviated_volume, volume_size):
        """
        Takes in volume and size (strings) and converts to actual volume size.
        """

        volume = abbreviated_volume
        volume_size = volume_size.upper()

        if 'B' in volume_size:

            size = 1000000000
            volume *= size

        elif 'M' in volume_size:

            size = 1000000
            volume *= size

        elif 'K' in volume_size:

            size = 1000
            volume *= size
        
        return volume

    def get_trade_dates_with_unusual_volume_and_price_action(self, volume, price_change):
        """
        Return a list of trade dates with data to input trade.
        """

        stock_data = self.get_stock_data()
        trades = list()

        for possible_trade_day in stock_data[1:]:

            abbreviated_volume, volume_size = possible_trade_day[5].split('.')
            abbreviated_volume = int(abbreviated_volume)
            volume_size = ''.join(size for size in volume_size if not size.isdigit()).upper()
            daily_price_change = float(possible_trade_day[6].split('%')[0])/100

            daily_volume = self.get_actual_volume_size(abbreviated_volume, volume_size)

            if price_change < 0:

                if daily_volume > volume and daily_price_change < price_change:

                    trades.append(possible_trade_day)

            else:

                if daily_volume > volume and daily_price_change > price_change:

                    trades.append(possible_trade_day)

        return trades

    def get_conditioned_trades(self, volume, price_change):
        """
        Returns the following trade dates and related data based on a set criteria.

        Best results: Invested on day 4, duration of 15, prior volume days of 3, form_factor of 2 and following days volume is 3.
        """

        day_invested = 3
        duration_of_investment = 30              # includes accumulated volume days.
        prior_days_volume = 5                      
        form_factor_for_volume = 1.5
        trades = 0

        stock_data = self.get_stock_data()
        actual_trade_dates = self.get_trade_dates_with_unusual_volume_and_price_action(volume, price_change)

        wins = 0
        losses = 0
        overall_gain = 1.0

        # Shift range to the right due to header row.
        for index, trade_day in enumerate(stock_data[1:],1):

            if trade_day in actual_trade_dates:

                total_price_change = float()
                prior_volume = int()
                following_volume = int()
                
                count = 0

                # Total price change (%) is calculated for the next # days.
                for day in range(day_invested+1, duration_of_investment+1):

                    # Try/except used for edges of list.
                    try:

                        # print(stock_data[index + 1 + day][0], stock_data[index + 1 + day][6])

                        # Index is shifted to the right to account for header row.
                        # Count may need to be used to average to get daily price gain.
                        total_price_change += float(stock_data[index+day][6].split('%')[0])/100
                        count += 1

                    except:

                        continue

                count = 0

                # Total volume change for the previous five days (averaged).
                for day in range(-1, -prior_days_volume, -1):

                    try:

                        # Index is shifted to the right to account for header row.
                        # Count may need to be used to average to get daily price gain.

                        abbreviated_volume, volume_size = stock_data[index+day][5].split('.')
                        abbreviated_volume = int(abbreviated_volume)
                        volume_size = ''.join(size for size in volume_size if not size.isdigit()).upper()

                        daily_volume = self.get_actual_volume_size(abbreviated_volume, volume_size)

                        prior_volume += daily_volume
                        count += 1

                    except:

                        continue

                count = 0
                following_days_for_volume_measurement = day_invested # Accounts for market close on previous day with range stopping at previous value.

                # Total volume change for the next two days (averaged).
                for day in range(1, following_days_for_volume_measurement):

                    try:

                        # Index is shifted to the right to account for header row.
                        # Count may need to be used to average to get daily price gain.

                        abbreviated_volume, volume_size = stock_data[index+day][5].split('.')
                        abbreviated_volume = int(abbreviated_volume)
                        volume_size = ''.join(size for size in volume_size if not size.isdigit()).upper()

                        daily_volume = self.get_actual_volume_size(abbreviated_volume, volume_size)

                        following_volume += daily_volume
                        count += 1

                    except:

                        continue

                if (prior_volume//count)*form_factor_for_volume < following_volume:

                    print('Trade day: ', stock_data[index])
                    print('Percent change: ', str(round(total_price_change*100, 2))+'%')
                    print('Prior Volume: ', prior_volume//count)
                    print('Frwdd Volume: ', following_volume)
                    print()

                    if total_price_change != 0:

                        if total_price_change < -0.02:

                            overall_gain *= 0.98
                            trades += 1

                            if total_price_change > 0:

                                wins += 1

                            else:

                                losses += 1

                        else:

                            overall_gain *= total_price_change + 1
                            trades += 1

                            if total_price_change > 0:

                                wins += 1

                            else:

                                losses += 1

        print('Win %: ', str(round((wins/trades)*100, 2))+'%', '   Wins:', wins, ' Losses:', losses)
        print('Overall gain: ', str(round(overall_gain*100, 2))+'%', ' with ', trades, ' trades.')
        print('$15000k invested would equal: ', '$' + '{:,}'.format(int(150000*(overall_gain+1))))


    def __repr__(self):
        """
        Official representation of CanonTrades.
        """

        return '\n'.join(map(str, self.get_stock_data()))


def main():
    """
    Main function.
    """
    # Check the correlation of bewiching days to returns for stocks after the four quarterly days.
    trades = CanonTrades('chkp.csv')
    print()
    print()
    trades.get_conditioned_trades(200000, -0.04)
    print()
    print()


# Tests whether file is ran as script and whether the main function ought be called.
if __name__ == '__main__':

    main()




# print('Trade day: ', stock_data[index],'\n',
#       'Trade day+1: ', stock_data[index+1],'\n',
#       'Trade day+2: ', stock_data[index+2],'\n',
#       'Trade day+3: ', stock_data[index+3],'\n',
#       'Trade day+4: ', stock_data[index+4],'\n',
#       'Trade day+5: ', stock_data[index+5],'\n','\n')
