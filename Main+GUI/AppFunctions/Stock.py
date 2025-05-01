## Here We will create a class named stock

#importing necessary modules
from Datafetcher import DataFetcher
import json

class Stock:

    def __init__(self,symbol,companyname):
        self.symbol=symbol
        self.companyname=companyname
        self.stock_data=DataFetcher(symbol)

    
    def get_historical_data(self,period):
        """
        Extracting the historical data of the concerned stock
        returns a Pandas data frame with the data
        """

        hist_data=self.stock_data.get_historical_data(period)
        return hist_data
    
    def get_latest_data(self):
        """
        Extracting the latest data of the concerned stock
        returns a dictionary with the data - namely symbol,latest price and latest date as key
        """

        latest_data=self.stock_data.get_latest_price()
        return latest_data
    
    def calculate_price_change(self,period):
        """
        Percentage change in the price is calculated
        Returns the percentage change
        """
        past_data=self.get_historical_data(period)
        latest_data=self.get_latest_data()
        current_price=float(latest_data['Latest Price'])
        previous_price=float(past_data['Closing Price'].iloc[-2])
        percent_change=((current_price-previous_price)/current_price)*100
        return str((percent_change))+'%'

# mystock=Stock('TCS.NS','Tata Consultancy Services Ltd')
# print(mystock.calculate_price_change('1mo'))