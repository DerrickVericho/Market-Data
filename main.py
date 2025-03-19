import requests
import pandas as pd
from datetime import date

api_key = 'SRWEWJNP9LO1RWR6'
TIME_SERIES_INTRADAY = 'TIME_SERIES_INTRADAY'
TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
TIME_SERIES_WEEKLY_ADJUSTED = 'TIME_SERIES_WEEKLY_ADJUSTED'
TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'
TIME_SERIES_MONTHLY_ADJUSTED = 'TIME_SERIES_MONTHLY_ADJUSTED'


class BaseUrl:

    """
    Contains base url and api key use for all function in alpha-vantage
    """
    base_url = 'https://www.alphavantage.co/query?'
    def __init__(self, api_key):
        self.api_key = api_key
        self.today = date.today().strftime("%Y-%m-%d")

class CoreStock(BaseUrl):

    """
    For Stock session especially US Stock, 
    
    """
    def __init__(self, api_key):
        super().__init__(api_key)

    def core_stock(self, function, ticker, interval = '5min', month = '2010-01', size='compact'):
        if function != TIME_SERIES_INTRADAY:
            url = f'{self.base_url}function={function}&symbol={ticker}&outputsize={size}&apikey={api_key}'
        else:
            url = f'{self.base_url}function={function}&symbol={ticker}&interval={interval}&month={month}&outputsize={size}&apikey={api_key}'
        response = requests.get(url)
        return response.json()

    def stock_df(self, ticker, function, interval = '5min', month = '2010-01', size='compact', debug=True):
        data = self.core_stock(function, ticker, interval, month, size)
        info = list(data.keys())
        time_series = info[1]
        meta_data = info[0]
        df = pd.DataFrame(data[time_series]).T

        if debug:
            if function != TIME_SERIES_INTRADAY:
                print("Ticker         :", data[meta_data]['2. Symbol'])
                print("Last Refreshed :", data[meta_data]['3. Last Refreshed'])
            else:
                print("Ticker         :", data[meta_data]['2. Symbol'])
                print("Last Refreshed :", data[meta_data]['3. Last Refreshed'])
                print("Interval       :", data[meta_data]['4. Interval'])

        return df

    def global_market(self):
        url = 'https://www.alphavantage.co/query?function=MARKET_STATUS&apikey=' + api_key
        response =  requests.get(url)
        data =  response.json()
        df = pd.DataFrame(data['markets'])
        return df

class OptionsData(BaseUrl):

    """
    Contains Options data (US)
    """
    def __init__(self, api_key):
        super().__init__(api_key)

    def options(self, ticker, date=None):
        if date==None:
            url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}&apikey={api_key}'
        else:
            url = f'https://www.alphavantage.co/query?function=HISTORICAL_OPTIONS&symbol={ticker}&date={date}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()

        df = pd.DataFrame(data['data'])
        return df

# Soon update
'''
class AlphaIntelligence(BaseUrl):


    def __init__(self, api_key):
        super().__init__(api_key)
'''

class FundamentalData(BaseUrl):
    def __init__(self, api_key):
        super().__init__(api_key)

    def company_overview():
        return 


if __name__ == "__main__":
    api_key = 'FTCAN551TMQBI2IC'

    # Core Stock
    TIME_SERIES_INTRADAY = 'TIME_SERIES_INTRADAY'
    TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
    TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
    TIME_SERIES_WEEKLY_ADJUSTED = 'TIME_SERIES_WEEKLY_ADJUSTED'
    TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'
    TIME_SERIES_MONTHLY_ADJUSTED = 'TIME_SERIES_MONTHLY_ADJUSTED'

    stock_fetch = CoreStock(api_key)
    # df = stock_fetch.stock_df('NVDA', TIME_SERIES_INTRADAY)
    #print(df.head())

    #df = stock_fetch.global_market()
    # options_fetch = OptionsData(api_key)
    # df = options_fetch.options('IBM', '2020-03-18')
