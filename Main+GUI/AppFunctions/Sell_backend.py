# Selling stocks

#importing necessary modules
import customtkinter as ctk
from PIL import Image
from Stock import Stock
import subprocess, sys
import pandas as pd
from tkinter import messagebox
from datetime import datetime

class Investment:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Sell Stock")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        self.bg_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        self.content_frame = ctk.CTkFrame(self.bg_frame, 
                                          width=1200, 
                                          height=800, 
                                          corner_radius=15, 
                                          fg_color="black")
        self.content_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        bg_image = ctk.CTkImage(Image.open(r"Images\background.jpeg"), size=(1200, 800))
        self.img_label = ctk.CTkLabel(self.content_frame, image=bg_image, text="")
        self.img_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Read details from the file
        with open('Sell.txt', 'r') as file:
            lines = file.readlines()
            symbol = lines[0].strip().lower()
            company_name = lines[1].strip()
            purchase_date = lines[2].strip()

        stk = Stock(symbol, company_name)  # Symbol and company name
        mydata = stk.get_historical_data('10y')  # Fetch data for the last 10 years

        # Correct the date format (yyyy/mm/dd)
        try:
            purchase_date_obj = datetime.strptime(purchase_date, "%Y/%m/%d")
        except ValueError as e:
            messagebox.showerror("Invalid Date Format", f"Error: {e}")
            return

        # Find the stock price on the purchase date
        purchase_data = mydata[mydata.index == purchase_date_obj.strftime('%Y-%m-%d')]

        if purchase_data.empty:
            messagebox.showerror("Date Not Found", f"No data found for the date {purchase_date}")
            subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/Sell.py"])

        purchase_price = purchase_data['Closing Price'].iloc[0]

        # Perform analysis to determine if it's a good time to sell
        current_price = float(stk.get_latest_data()['Latest Price'])
        highest_price = float(mydata['Highest Price'].max())
        closing_price = float(mydata['Closing Price'].iloc[-1])  # Last closing price
        price_std = float(mydata['Closing Price'].std())  # Standard deviation of closing prices
        price_change = float(((closing_price - purchase_price) / purchase_price) * 100)  # Price change since purchase
        profit = float(closing_price - purchase_price)

        # Generate recommendation based on stock data analysis
        if float(price_change) > 10:  # Significant profit
            if current_price >= highest_price * 0.95:  # Near historical high
                recommendation = (f"The stock has increased by {float(price_change):.2f}% (Profit: {float(profit):.2f}). "
                                  f"It's near its historical high ({float(current_price)} vs. {float(highest_price)}). "
                                  "Selling now is prudent to lock in gains.")
            else:
                recommendation = (f"The stock has increased by {float(price_change):.2f}% (Profit: {float(profit):.2f}). "
                                  "You may hold it for now, as it's not at its peak, indicating potential for further gains.")
        elif float(price_change) > 0:  # Moderate profit
            if float(price_std) > 2:  # High volatility
                recommendation = (f"The stock is moderately profitable ({float(price_change):.2f}%, Profit: {profit:.2f}), "
                                  f"but it's highly volatile (STD: {float(price_std):.2f}). Selling now might reduce risk.")
            else:
                recommendation = (f"The stock is showing moderate gains ({float(price_change):.2f}%, Profit: {profit:.2f}). "
                                  "Holding could yield better profits if market trends remain stable.")
        elif float(price_change) <= 0:  # Loss or no significant profit
            if float(current_price) < float(purchase_price) * 0.9:  # Significant loss
                recommendation = (f"The stock has decreased significantly ({float(price_change):.2f}%, Loss: {profit:.2f}). "
                                  "It might be prudent to sell and cut losses if no signs of recovery are visible.")
            else:  # Small loss
                recommendation = ("The stock is currently at a loss. Consider holding if market trends suggest recovery; "
                                  "otherwise, selling might minimize further losses.")
        else:  # Neutral case
            recommendation = ("The stock's performance has been flat. Holding could be wise if the market outlook is stable, "
                              "but selling might be prudent to free up capital.")

        # Form Frame for displaying recommendations
        self.form_frame = ctk.CTkFrame(
            self.bg_frame,
            width=1000,
            height=450,  # Increased height for better layout
            fg_color="black",
            corner_radius=15,
            border_color="white",
            border_width=3
        )
        self.form_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Title Label
        self.rec_label = ctk.CTkLabel(
            self.form_frame,
            text="Stock Selling Recommendation",
            font=('Helvetica', 30, "bold"),
            text_color="white"
        )
        self.rec_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        # Bot Image
        bot_image = ctk.CTkImage(Image.open(r"Images\Bot.jpeg"), size=(150, 100))
        self.bot_label = ctk.CTkLabel(self.form_frame, image=bot_image, text="")
        self.bot_label.place(relx=0.1, rely=0.5, anchor=ctk.CENTER)

        # Suggestion Text
        self.sug_label = ctk.CTkLabel(
            self.form_frame,
            text=recommendation,
            font=('Helvetica', 16, "bold"),
            text_color="white",
            wraplength=700,  # Ensure text wraps within the frame
            justify="center"
        )
        self.sug_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Current Price Info
        self.inf_label = ctk.CTkLabel(
            self.form_frame,
            text=f"Current Price: {current_price:.2f}",
            font=('Helvetica', 20, "bold"),
            text_color="white"
        )
        self.inf_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        # Back Button
        self.back_btn = ctk.CTkButton(
            self.form_frame, 
            text="Back to Guide", 
            width=200,
            height=40,
            font=("Helvetica", 18, "bold"),
            corner_radius=10,
            fg_color="red",
            command=self.back
        )
        self.back_btn.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)

    def back(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, 'Main+GUI/AppFunctions/StockGuide.py'])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Investment()
    app.run()
