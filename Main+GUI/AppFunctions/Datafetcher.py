## Fetching stock data from Yahoo Finance

#Importing necessary modules
import yfinance as yf
import pandas as pd
import numpy as np

class DataFetcher:
    def __init__(self, symbol):
        self.symbol = symbol
        self.stock = yf.Ticker(symbol)

    def get_historical_data(self, period='1y'):
        """
        Fetch historical stock data with advanced formatting
        
        param period: Time period for historical data 
                       Options: '1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'
        Return: Formatted DataFrame with historical stock data
        default period is set to 1 year
        """
        try:
            # Fetch historical data
            historical_data = self.stock.history(period=period)
            
            # Check if data is empty
            if historical_data.empty:
                print(f"No historical data found for {self.symbol}")
                return None
            
            # Advanced Formatting
            formatted_data = self._format_historical_data(historical_data)
            
            return formatted_data
        
        except Exception as e:
            print(f"Error fetching historical data for {self.symbol}: {e}")
            return None

    def _format_historical_data(self, historical_data):
        """
        Internal method to format historical data
        
        param historical_data: Raw historical stock data
        Return: Formatted DataFrame
        """
        # Rename columns for clarity
        column_mapping = {
            'Open': 'Opening Price',
            'High': 'Highest Price',
            'Low': 'Lowest Price', 
            'Close': 'Closing Price',
            'Volume': 'Trading Volume'
        }
        historical_data.rename(columns=column_mapping, inplace=True)
        
        # Format index to date
        historical_data.index = historical_data.index.strftime('%Y-%m-%d')
        
        # Round numerical columns
        numeric_columns = [
            'Opening Price', 
            'Highest Price', 
            'Lowest Price', 
            'Closing Price'
        ]
        
        for col in numeric_columns:
            historical_data[col] = historical_data[col].round(2)
        
        # Format Trading Volume
        historical_data['Trading Volume'] = historical_data['Trading Volume'].apply(lambda x: f'{x:,}')
        
        return historical_data

    def get_latest_price(self):
        """
        Extract the latest stock price with advanced formatting
        
        Return: Dictionary with latest price details
        """
        try:
            # Fetch 1-month historical data
            historical_data = self.get_historical_data(period='1mo')
            
            if historical_data is not None and not historical_data.empty:
             # Get latest closing price and date
                latest_price = historical_data['Closing Price'].iloc[-1]
                latest_date = historical_data.index[-1]
                
                return {
                    'Symbol': self.symbol,
                    'Latest Price': f"{latest_price:.2f}", 
                    'Latest Date': latest_date
                }
            
            return None
        
        except Exception as e:
            print(f"Error fetching current price for {self.symbol}: {e}")
            return None

    def get_stock_data(self):
        """
        Retrieve comprehensive stock information
        
        Return: Formatted dictionary with stock details
        """
        try:
            stock_info = self.stock.info
            
            # Filter and format key stock information
            key_info = {
                'Company Name': stock_info.get('longName', 'N/A'),
                'Sector': stock_info.get('sector', 'N/A'),
                'Industry': stock_info.get('industry', 'N/A'),
            }
            
            return key_info
        
        except Exception as e:
            print(f"Error fetching stock info for {self.symbol}: {e}")
            return 