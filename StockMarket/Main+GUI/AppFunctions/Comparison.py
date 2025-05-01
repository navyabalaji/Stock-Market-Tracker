#Comparison plot between 2 stocks

#Importing necessary modules
import customtkinter as ctk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
from datetime import datetime
import sqlite3
import subprocess
import sys

stocksdb=sqlite3.connect("stocks.db")
mycursor=stocksdb.cursor()

class StockComparison:
    def __init__(self):
        # Set up CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Stock Market Comparison")
        self.root.geometry("1200x800")

        with open ("TemporaryUserDetails.txt","r") as user:
            username=user.readline().strip()

        query = "SELECT StockSymbol FROM Stocks WHERE username = ?"
        mycursor.execute(query, (username,))  # Use the username from the file
        stocks = mycursor.fetchall()
        
        mystocks=[symbol for tuple in stocks for symbol in tuple]


        # Main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Input Frame
        self.input_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        self.input_frame.pack(pady=10, padx=10, fill="x")

        # Stock 1 Dropdown
        self.stock1_label = ctk.CTkLabel(self.input_frame, text="Stock 1 Symbol:", font=("Helvetica", 16))
        self.stock1_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.stock1_dropdown = ctk.CTkComboBox(
            self.input_frame, 
            values=mystocks, 
            width=250,
            font=("Helvetica", 14)
        )
        self.stock1_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.stock1_dropdown.set("Select symbol")

        # Stock 2 Dropdown
        self.stock2_label = ctk.CTkLabel(self.input_frame, text="Stock 2 Symbol:", font=("Helvetica", 16))
        self.stock2_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.stock2_dropdown = ctk.CTkComboBox(
            self.input_frame, 
            values=mystocks, 
            width=250,
            font=("Helvetica", 14)
        )
        self.stock2_dropdown.grid(row=1, column=1, padx=10, pady=10)
        self.stock2_dropdown.set("Select symbol")

        # From Date Entry
        self.from_date_label = ctk.CTkLabel(self.input_frame, text="From Date:", font=("Helvetica", 16))
        self.from_date_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.from_date_entry = ctk.CTkEntry(
            self.input_frame, 
            width=250,
            font=("Helvetica", 14)
        )
        self.from_date_entry.grid(row=2, column=1, padx=10, pady=10)
        self.from_date_entry.insert(0, "2023-01-01")

        # To Date Entry
        self.to_date_label = ctk.CTkLabel(self.input_frame, text="To Date:", font=("Helvetica", 16))
        self.to_date_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.to_date_entry = ctk.CTkEntry(
            self.input_frame, 
            width=250,
            font=("Helvetica", 14)
        )
        self.to_date_entry.grid(row=3, column=1, padx=10, pady=10)
        self.to_date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # Interval Dropdown
        self.interval_label = ctk.CTkLabel(self.input_frame, text="Interval:", font=("Helvetica", 16))
        self.interval_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.interval_dropdown = ctk.CTkComboBox(
            self.input_frame, 
            values=["1d", "1wk", "1mo"], 
            width=250,
            font=("Helvetica", 14)
        )
        self.interval_dropdown.grid(row=4, column=1, padx=10, pady=10)
        self.interval_dropdown.set("1d")

        # Fetch Button
        self.fetch_button = ctk.CTkButton(
            self.input_frame, 
            text="Fetch and Plot", 
            command=self.fetch_and_plot_data,
            fg_color="green",
            font=("Helvetica", 16, "bold"),
            width=250
        )
        self.fetch_button.grid(row=5, column=1, padx=10, pady=10)

        self.back_button = ctk.CTkButton(
            self.input_frame, 
            text="Back to dashboard", 
            fg_color="orange",
            font=("Helvetica", 16, "bold"),
            width=250,
            command=self.back
        )
        self.back_button.grid(row=5, column=2, padx=10, pady=10)

        # Plot Frame
        self.plot_frame = ctk.CTkFrame(self.main_frame)
        self.plot_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def fetch_and_plot_data(self):
        """Fetch and plot stock data"""
        # Clear previous plot
        self.ax.clear()

        try:
            # Fetch data for the first stock
            symbol1 = self.stock1_dropdown.get()
            symbol2 = self.stock2_dropdown.get()
            start_date = self.from_date_entry.get()
            end_date = self.to_date_entry.get()
            interval = self.interval_dropdown.get()

            # Download stock data
            data1 = yf.download(symbol1, start=start_date, end=end_date, interval=interval)
            data2 = yf.download(symbol2, start=start_date, end=end_date, interval=interval)

            # Plot data
            if not data1.empty:
                self.ax.plot(data1.index, data1['Close'], label=f"{symbol1} Close Price", color="blue")
            
            if not data2.empty:
                self.ax.plot(data2.index, data2['Close'], label=f"{symbol2} Close Price", color="orange")

            # Styling
            self.ax.set_title("Stock Price Comparison", fontsize=16)
            self.ax.set_xlabel("Date", fontsize=12)
            self.ax.set_ylabel("Price", fontsize=12)
            self.ax.legend()
            self.ax.grid(True, linestyle='--', alpha=0.7)

            # Rotate and align the tick labels
            self.fig.autofmt_xdate()

            # Redraw the canvas
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def back(self):
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/Dashboard.py"])

    def run(self):
        """Run the application"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = StockComparison()
    app.run()