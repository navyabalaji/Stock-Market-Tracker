import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sqlite3
import subprocess,sys

class MyStocks:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.stocksdb = sqlite3.connect("stocks.db")
        self.mycursor = self.stocksdb.cursor()  # Storing cursor as an instance variable

        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("MyStocks")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Background Frame
        self.bg_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Content Frame
        self.content_frame = ctk.CTkFrame(self.bg_frame, 
                                          width=1200, 
                                          height=800, 
                                          corner_radius=15, 
                                          fg_color="black")
        self.content_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Background Image
        bg_image = ctk.CTkImage(Image.open(r"Images\background.jpeg"), size=(1200, 800))
        self.img_label = ctk.CTkLabel(self.content_frame, image=bg_image, text="")
        self.img_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.back_btn=ctk.CTkButton(self.bg_frame,
                                    text="Back to dashboard",
                                    fg_color="orange",
                                    font=("Helvetica",18,"bold"),
                                    width=20,
                                    height=20,
                                    command=self.back)
        self.back_btn.place(relx=0.57, rely=0.96, anchor="se")

        # Scrollable Frame for Stocks (Left Side)
        self.mystk_frame = ctk.CTkScrollableFrame(
            self.bg_frame, 
            width=400, 
            height=500, 
            fg_color="black",
            border_color="white",  
            border_width=3,        
            corner_radius=10       
        )
        self.mystk_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Title Label in Stocks Frame
        self.title_label = ctk.CTkLabel(self.mystk_frame,
                                        text="My Stocks",
                                        font=("Helvetica", 28, "bold"),
                                        text_color="white"
                                        )
        self.title_label.pack(pady=(10, 20))

        # Load stocks and display them as buttons
        self.load_stocks()

    def load_stocks(self):
        """
        Fetch stocks from the database and display them as buttons inside the scrollable frame.
        """
        try:
            # Read the username from a temporary file
            with open("TemporaryUserDetails.txt", "r") as tempfile:
                lines = tempfile.readlines()
                details = [line.strip() for line in lines]

            # Fetch stocks from the database
            query = "SELECT StockSymbol, CompanyName FROM Stocks WHERE username = ?"
            self.mycursor.execute(query, (details[0],))  # Use the username from the file
            stocks = self.mycursor.fetchall()
            print(stocks)

            if not stocks:
                no_stocks_label = ctk.CTkLabel(
                    self.mystk_frame,
                    text="No stocks found.",
                    font=("Helvetica", 16, "italic"),
                    text_color="gray"
                )
                no_stocks_label.pack(pady=(20, 0))
                return

            # Create a button for each stock symbol
            for stock in stocks:
                stock_symbol = stock[0]  # Extract stock symbol
                stock_cmpname = stock[1]  # Extract stock company

                # Use default arguments in lambda to "freeze" the values
                stock_button = ctk.CTkButton(
                    self.mystk_frame,
                    text=stock_symbol,
                    width=100,
                    height=50,
                    font=("Helvetica", 16),
                    fg_color="blue",
                    command=lambda symbol=stock_symbol, cmpname=stock_cmpname: self.on_stock_click(symbol, cmpname)  # Lambda for button click
                )
                stock_button.pack(pady=10, padx=10, fill="x")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    def on_stock_click(self, stock_symbol, stock_cmpname):
        """
        Handle the stock button click event.
        """
        with open("plot.txt", "w") as f:
            f.write(stock_symbol + '\n' + stock_cmpname)
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/Visualiser.py"])

    def back(self):
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/Dashboard.py"])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MyStocks()
    app.run()