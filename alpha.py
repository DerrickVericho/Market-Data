import requests
import pandas as pd

api_key = 'SRWEWJNP9LO1RWR6'
TIME_SERIES_INTRADAY = 'TIME_SERIES_INTRADAY'
TIME_SERIES_DAILY = 'TIME_SERIES_DAILY'
TIME_SERIES_WEEKLY = 'TIME_SERIES_WEEKLY'
TIME_SERIES_WEEKLY_ADJUSTED = 'TIME_SERIES_WEEKLY_ADJUSTED'
TIME_SERIES_MONTHLY = 'TIME_SERIES_MONTHLY'
TIME_SERIES_MONTHLY_ADJUSTED = 'TIME_SERIES_MONTHLY_ADJUSTED'


class FinancialData:
    base_url = 'https://www.alphavantage.co/query?'

    def __init__(self, api_key):
        self.api_key = api_key


    def fetch_data(self, function, **kwargs):
        params = {
            "function": function,
            "api_key": self.api_key,
            **kwargs
        }
        response = requests.get(self.base_url, params=params)
        return response.json()


class CoreStock(FinancialData):
    def __init__(self, api_key):
        super().__init__(api_key)


    def stock_df(self, ticker, function, interval = '5min', month = '2010-01', size='compact', debug=True):
        if function != TIME_SERIES_INTRADAY:
            kwargs = {"symbol": ticker, "output_size": size}
            data = super().fetch_data(function, **kwargs)
        else:
            kwargs = {"symbol": ticker, "inverval": interval, "month": month ,"output_size": size}
            data = self.fetch_data(function, **kwargs)
            
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
    df = stock_fetch.stock_df('NVDA', TIME_SERIES_INTRADAY)
    print(df.head())