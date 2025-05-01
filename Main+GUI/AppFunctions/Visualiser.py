import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Cursor
from Stock import Stock
import subprocess 
import sys
from Datafetcher import DataFetcher
import pandas as pd

class Visualise:
    def __init__(self, root):
        """
        Initialize the Stock Visualization Application
        
        :param root: The main CustomTkinter window
        """
        # Configure the main window
        root.title("Stock Visualization")
        root.geometry("1300x900")  # Slightly larger to accommodate new elements

        # Read stock details
        with open('plot.txt', 'r') as f:
            lines = f.readlines()
            details = [line.strip() for line in lines]
        
        self.symbol = details[0]
        self.name = details[1]

        # Store stock data for different periods
        self.stock_data = {}
        self.periods = ['1mo', '3mo', '6mo', '1y', '10y']

        # Fetch stock data for all periods
        self.fetch_stock_data()

        # Create control frame
        self.create_control_frame(root)

        # Initial plot setup
        self.current_period = '3mo'
        self.current_plot_type = 'Candlestick'
        
        # Create initial plot
        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=ctk.BOTH, expand=True, padx=20, pady=10)

        # Create plot
        self.create_plot()

        # Create frame for current price
        self.create_current_price_frame(root,'1mo')

    def fetch_stock_data(self):
        """
        Fetch stock data for different periods
        """
        stk = Stock(self.symbol, self.name)

        for period in self.periods:
            try:
                data = stk.get_historical_data(period)
                self.stock_data[period] = data
            except Exception as e:
                print(f"Error fetching stock data for {period}: {e}")
                self.stock_data[period] = None

    def create_control_frame(self, root):
        """
        Create control frame with dropdown menus
        
        :param root: The main CustomTkinter window
        """
        control_frame = ctk.CTkFrame(root, fg_color="black")
        control_frame.pack(fill='x', padx=20, pady=10)

        # Period Dropdown
        self.period_label = ctk.CTkLabel(control_frame, text="Time Period:")
        self.period_label.pack(side='left', padx=(0, 10))

        self.period_dropdown = ctk.CTkOptionMenu(
            control_frame, 
            values=self.periods,
            command=self.on_period_change
        )
        self.period_dropdown.pack(side='left', padx=(0, 20))
        self.period_dropdown.set('3mo')  # Default selection

        # Plot Type Dropdown
        self.plot_type_label = ctk.CTkLabel(control_frame, text="Plot Type:")
        self.plot_type_label.pack(side='left', padx=(20, 10))

        self.plot_type_dropdown = ctk.CTkOptionMenu(
            control_frame, 
            values=[
                'Candlestick', 
                'Volume', 
                'Closing Price', 
                'Opening Price', 
                'High-Low Range'
            ],
            command=self.on_plot_type_change
        )
        self.plot_type_dropdown.pack(side='left')
        self.plot_type_dropdown.set('Candlestick')  # Default selection

    def on_period_change(self, new_period):
        """
        Handle period dropdown change
        
        :param new_period: Selected time period
        """
        self.current_period = new_period
        self.create_plot()

    def on_plot_type_change(self, new_plot_type):
        """
        Handle plot type dropdown change
        
        :param new_plot_type: Selected plot type
        """
        self.current_plot_type = new_plot_type
        self.create_plot()

    def create_plot(self):
        """
        Create plot based on current period and plot type
        """
        # Clear previous plot
        self.ax.clear()

        # Get current stock data
        data = self.stock_data.get(self.current_period)
        
        if data is None:
            self.ax.text(0.5, 0.5, "No data available", 
                         horizontalalignment='center', 
                         verticalalignment='center')
            self.canvas.draw()
            return

        # Plot based on selected type
        if self.current_plot_type == 'Candlestick':
            self.plot_candlesticks(data)
        elif self.current_plot_type == 'Volume':
            self.plot_volume(data)
        elif self.current_plot_type == 'Closing Price':
            self.plot_line(data, 'Closing Price')
        elif self.current_plot_type == 'Opening Price':
            self.plot_line(data, 'Opening Price')
        elif self.current_plot_type == 'High-Low Range':
            self.plot_high_low_range(data)

        # Configure plot
        self.ax.set_title(f"{self.name} Stock - {self.current_plot_type} ({self.current_period})")
        self.ax.set_xlabel("Date")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Redraw canvas
        self.canvas.draw()

    def plot_candlesticks(self, data):
        """
        Plot candlestick chart
        
        :param data: Stock data DataFrame
        """
        opens = data['Opening Price']
        highs = data['Highest Price']
        lows = data['Lowest Price']
        closes = data['Closing Price']
        dates = data.index

        for i in range(len(dates)):
            if closes.iloc[i] >= opens.iloc[i]:
                color = 'g'  # Green for price increase
                height = closes.iloc[i] - opens.iloc[i]
                bottom = opens.iloc[i]
            else:
                color = 'r'  # Red for price decrease
                height = opens.iloc[i] - closes.iloc[i]
                bottom = closes.iloc[i]

            # Plot candle body
            self.ax.bar(dates[i], height, bottom=bottom, width=0.7, 
                        color=color, alpha=0.7)
            
            # Plot high-low lines
            self.ax.vlines(dates[i], lows.iloc[i], highs.iloc[i], color='black', linewidth=1)

    def plot_volume(self, data):
        """
        Plot trading volume
        
        :param data: Stock data DataFrame
        """
        # Check the available columns
        print("Available columns:", list(data.columns))
        
        # Try different potential column names for volume
        volume_columns = ['Volume', 'Trading Volume', 'trade_volume', 'volume']
        
        for col in volume_columns:
            if col in data.columns:
                self.ax.bar(data.index, data[col], color='blue', alpha=0.6)
                self.ax.set_ylabel("Trading Volume")
                return
        
        # If no volume column found
        self.ax.text(0.5, 0.5, "Volume data not available", 
                     horizontalalignment='center', 
                     verticalalignment='center')

    def plot_line(self, data, column):
        """
        Plot line graph for a specific column
        
        :param data: Stock data DataFrame
        :param column: Column to plot
        """
        self.ax.plot(data.index, data[column], color='blue')
        self.ax.set_ylabel(column)

    def plot_high_low_range(self, data):
        """
        Plot high-low range
        
        :param data: Stock data DataFrame
        """
        self.ax.fill_between(
            data.index, 
            data['Lowest Price'], 
            data['Highest Price'], 
            alpha=0.3, 
            color='green'
        )
        self.ax.set_ylabel("Price Range")

    # The rest of the methods remain the same as in the original code
    def create_current_price_frame(self, root, period='1mo'):
        """
        Create a frame to display the current stock price and other details
        
        :param root: The main CustomTkinter window
        """
        
        with open('plot.txt', 'r') as f:
            lines = f.readlines()
            details = [line.strip() for line in lines]

        df=DataFetcher(details[0])
        key_info=df.get_stock_data()

        current_price = self.stock_data[period]['Closing Price'].iloc[-1] if self.stock_data is not None else "N/A"

        frame=ctk.CTkFrame(root,
                      fg_color="white",
                      width=370,
                      height=100,
                      border_width=3,
                      border_color="black"
                      )
        frame.place(relx=0.1, rely=0.75, anchor="sw")

        current_price_label = ctk.CTkLabel(
            frame, 
            text=f"Current Price: ₹{current_price:.2f}", 
            text_color="black",
            font=("Helvetica", 14,"bold")
        )
        current_price_label.place(relx=0.48, rely=0.3, anchor=ctk.CENTER)

        sector_label=ctk.CTkLabel(frame,
                                  text="Sector:"+' '+key_info['Sector'],
                                  text_color="black",
                                  font=("Helvetica",14,"bold"))
        sector_label.place(relx=0.48, rely=0.5, anchor=ctk.CENTER)

        industry_label=ctk.CTkLabel(frame,
                                  text="Industry:"+' '+key_info['Industry'],
                                  text_color="black",
                                  font=("Helvetica",14,"bold"))
        industry_label.place(relx=0.5, rely=0.72, anchor=ctk.CENTER)

        self.back_button=ctk.CTkButton(root,
                                       text="Back to MyStocks",
                                       fg_color="orange",
                                       width=80,
                                       height=20,
                                       font=("Helvetica",18,"bold"),
                                       command=lambda: self.back(root))
        self.back_button.place(relx=0.9,rely=0.05, anchor="se")
    
    def back(self,root):
        root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/MyStocks.py"])

def main():
    # Set appearance and color theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create main window
    root = ctk.CTk()
    
    # Create app instance
    app = Visualise(root)
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()