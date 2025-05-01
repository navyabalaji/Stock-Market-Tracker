import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sys
import sqlite3
import subprocess
import yfinance as yf
import logging

# Configure logging
logging.basicConfig(filename='stock_tracker.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class AddStock:
    def __init__(self):
        # Set up appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize databases with error handling
        try:
            self.mydb = sqlite3.connect('stocks.db')
            self.cursor = self.mydb.cursor()
            self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Stocks(
                Username TEXT,
                CompanyName TEXT,
                StockSymbol TEXT,
                UNIQUE(Username, StockSymbol)  
            )
            ''')
            self.mydb.commit()

            self.userdb = sqlite3.connect('users.db')
            self.usercursor = self.userdb.cursor()
            self.userdb.commit()
        except sqlite3.Error as e:
            logging.error(f"Database connection error: {e}")
            messagebox.showerror("Database Error", "Failed to connect to databases")
            sys.exit(1)

        # Create main window
        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Add Stock")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Create background frame
        self.bg_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Create content frame
        self.content_frame = ctk.CTkFrame(self.bg_frame, 
                                          width=1200, 
                                          height=800, 
                                          corner_radius=15, 
                                          fg_color="black")
        self.content_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Set background image with error handling
        try:
            bg_image = ctk.CTkImage(Image.open(r"Images\background.jpeg"), size=(1200, 800))
            self.img_label = ctk.CTkLabel(self.content_frame, image=bg_image, text="")
            self.img_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        except FileNotFoundError:
            logging.warning("Background image not found")

        # Create form frame
        self.form_frame = ctk.CTkFrame(self.content_frame, 
                                       width=400, 
                                       height=600, 
                                       fg_color="black",
                                       corner_radius=15,
                                       border_color='white',
                                       border_width=3)
        self.form_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Create UI elements
        self._create_ui_elements()

    def _create_ui_elements(self):
        """Create all UI elements for the form"""
        # Title
        self.title_label = ctk.CTkLabel(self.form_frame, 
                                        text="Add Stock", 
                                        font=("Helvetica", 36, "bold"),
                                        text_color="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)  

        # Username input
        self.username_label = ctk.CTkLabel(self.form_frame, 
                                           text="Username", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.username_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)
        self.username_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           placeholder_text="Enter your username")
        self.username_entry.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        # Stock Symbol input
        self.symbol_label = ctk.CTkLabel(self.form_frame, 
                                         text="Stock Symbol", 
                                         font=("Helvetica", 20),
                                         text_color="white")
        self.symbol_label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        self.symbol_entry = ctk.CTkEntry(self.form_frame, 
                                         width=300, 
                                         placeholder_text="Enter symbol of the stock")
        self.symbol_entry.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        # Company Name input
        self.cmpname_label = ctk.CTkLabel(self.form_frame,
                                          text="Company Name",
                                          font=("Helvetica", 20),
                                          text_color="white")
        self.cmpname_label.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)
        self.cmpname_entry = ctk.CTkEntry(self.form_frame,
                                          placeholder_text="Enter the company name",
                                          width=300)
        self.cmpname_entry.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

        # Add Stock button
        self.signup_btn = ctk.CTkButton(self.form_frame, 
                                        text="Add stock", 
                                        width=250,
                                        height=40,
                                        font=("Helvetica", 18, "bold"),
                                        corner_radius=10,
                                        fg_color="green",
                                        command=self.add)
        self.signup_btn.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

        # Back to Dashboard button
        self.back_btn = ctk.CTkButton(self.form_frame, 
                                      text="Back to dashboard", 
                                      width=250,
                                      height=40,
                                      font=("Helvetica", 18, "bold"),
                                      corner_radius=10,
                                      fg_color="red",
                                      command=self.back)
        self.back_btn.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)

    def back(self):
        """
        Navigating back to the dashboard
        """
        try:
            self.root.destroy()
            subprocess.Popen([sys.executable, "Main+GUI/Dashboard.py"])
        except Exception as e:
            logging.error(f"Error navigating to dashboard: {e}")
            messagebox.showerror("Navigation Error", "Could not open dashboard")

    def add(self):
        """
        Adding the data into the stocks database with comprehensive error handling
        """
        try:
            # Validate and clean inputs
            username = (self.username_entry.get()).strip()
            symbol = ((self.symbol_entry.get()).strip()).upper() + '.NS'
            companyname = ((self.cmpname_entry.get())).upper().strip()

            # Input validation
            if not all([username, symbol, companyname]):
                messagebox.showwarning("Warning", "Please fill in all the fields")
                return
    
            # Check if username exists
            self.usercursor.execute("SELECT username FROM users WHERE username=?", (username,))
            if not self.usercursor.fetchone():
                messagebox.showerror("Error", "Username doesn't exist")
                return
    
            # Check if this specific stock is already added by this user
            self.cursor.execute("SELECT * FROM Stocks WHERE Username=? AND (CompanyName=? OR StockSymbol=?)", 
                                (username, companyname, symbol))
            if self.cursor.fetchone():
                messagebox.showerror("Error", "You have already added this stock")
                return

            # Verify stock information
            try:
                stock = yf.Ticker(symbol)
                # Ensure the stock info is available
                stock_info = stock.info
                
                # Additional validation for Indian stocks
                if stock_info.get('country') != 'India':
                    messagebox.showinfo("Error", "Not an Indian Stock")
                    return

                # Insert stock into database
                self.cursor.execute("INSERT INTO Stocks (Username, CompanyName, StockSymbol) VALUES (?, ?, ?)", 
                                    (username, companyname, symbol))
                self.mydb.commit()
                
                # Log successful stock addition
                logging.info(f"Stock added: {companyname} ({symbol}) for user {username}")
                messagebox.showinfo("Success", "Stock added successfully!")

            except Exception as stock_error:
                logging.error(f"Stock verification error: {stock_error}")
                messagebox.showerror("Stock Error", "Could not verify stock information")

        except Exception as e:
            logging.error(f"Unexpected error in add method: {e}")
            messagebox.showerror("Unexpected Error", "An unexpected error occurred")

    def run(self):
        """
        Run the application with error handling
        """
        try:
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Application runtime error: {e}")
        finally:
            # Ensure database connections are closed
            self.mydb.close()
            self.userdb.close()

if __name__ == "__main__":
    app = AddStock()
    app.run()