# Guides the user on investing or selling stocks

# Importing necessary modules
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import subprocess
import sys


class StockGuide:
    def __init__(self):
        # Setting appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Creating the main window
        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Your Trade Guide")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Background Frame
        self.bg_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Content Frame
        self.content_frame = ctk.CTkFrame(
            self.bg_frame,
            width=1200,
            height=800,
            corner_radius=15,
            fg_color="black"
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Adding background image
        bg_image = ctk.CTkImage(Image.open(r"Images\background.jpeg"), size=(1200, 800))
        self.img_label = ctk.CTkLabel(self.content_frame, image=bg_image, text="")
        self.img_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Form Frame
        self.form_frame = ctk.CTkFrame(
            self.bg_frame,
            width=900,
            height=600,
            fg_color="black",
            corner_radius=15,
            border_color="white",
            border_width=3
        )
        self.form_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Bot Image
        bot_image = ctk.CTkImage(Image.open(r"Images\Bot.jpeg"), size=(200, 150))
        self.bot_label = ctk.CTkLabel(self.form_frame, image=bot_image, text="")
        self.bot_label.place(relx=0.5, rely=0.24, anchor=ctk.CENTER)

        # Title Label
        self.title_label = ctk.CTkLabel(
            self.form_frame,
            text="What would you like to do today?",
            font=("Helvetica", 36, "bold"),
            text_color="white"
        )
        self.title_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

        # Bot Introduction
        self.intro_label1 = ctk.CTkLabel(
            self.form_frame,
            text="Hello! I'm your StockBuddy, here to analyze market trends",
            font=("Helvetica", 18),
            text_color="white"
        )
        self.intro_label1.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)

        self.intro_label2 = ctk.CTkLabel(
            self.form_frame,
            text="and guide you on whether to invest in or sell a stock, making your trading decisions smarter and easier!",
            font=("Helvetica", 18),
            text_color="white"
        )
        self.intro_label2.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.invest_button=ctk.CTkButton(self.form_frame,
                                         text="Invest",
                                         font=('Helvetica',18,"bold"),
                                         fg_color="green",
                                         width=250,
                                         height=40,
                                         corner_radius=10,
                                         command=self.invest)
        self.invest_button.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        self.sell_button=ctk.CTkButton(self.form_frame,
                                         text="Sell",
                                         font=('Helvetica',18,"bold"),
                                         fg_color="green",
                                         width=250,
                                         height=40,
                                         corner_radius=10,
                                         command=self.sell)
        self.sell_button.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        self.invest_button=ctk.CTkButton(self.form_frame,
                                         text="Back to dashboard",
                                         font=('Helvetica',18,"bold"),
                                         fg_color="red",
                                         width=250,
                                         height=40,
                                         corner_radius=10,
                                         command=self.back,
                                         )
        self.invest_button.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)
    
    def sell(self):
        """
        Guiding the user whether he can sell a particular stock or not
        """
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/Sell.py"])

    def invest(self):
        """
        Guiding the user whether he can invest in a particular stock or not
        """
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/Invest.py"])


    def back(self):
        """
        Navigating the user back to the dashboard
        """
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/Dashboard.py"])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = StockGuide()
    app.run()