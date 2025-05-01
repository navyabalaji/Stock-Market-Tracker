import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import sys
import subprocess
import requests
import webbrowser
import threading

class Dashboard:

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.geometry("1200x800")
        self.root.title("Dashboard")

        self.bg_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        self.content_frame = ctk.CTkFrame(self.bg_frame,
                                          width=1200,
                                          height=800,
                                          corner_radius=15,
                                          fg_color="black")
        self.content_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        bg_image = ctk.CTkImage(Image.open(r"Images\background.jpeg"),
                                size=(1200, 800))
        self.img_label = ctk.CTkLabel(self.content_frame,
                                      image=bg_image,
                                      text="")
        self.img_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        self.navbar_frame = ctk.CTkFrame(self.content_frame,
                                         height=60,
                                         fg_color="black")
        self.navbar_frame.place(relx=0.5, rely=0.12, anchor=ctk.CENTER, relwidth=1)

        self.mystock_btn = ctk.CTkButton(self.navbar_frame,
                                         text="My Stocks",
                                         width=200,
                                         height=40,
                                         font=("Helvetica", 16, "bold"),
                                         corner_radius=10,
                                         fg_color="black",
                                         command=self.mystk)
        self.mystock_btn.pack(side="left", padx=10)

        self.add_stock_btn = ctk.CTkButton(self.navbar_frame,
                                           text="Add Stock",
                                           width=200,
                                           height=40,
                                           font=("Helvetica", 16, "bold"),
                                           corner_radius=10,
                                           fg_color="black",
                                           command=self.addstock)
        self.add_stock_btn.pack(side="left", padx=10)

        self.delete_stock_btn = ctk.CTkButton(self.navbar_frame,
                                              text="Delete Stock",
                                              width=200,
                                              height=40,
                                              font=("Helvetica", 16, "bold"),
                                              corner_radius=10,
                                              fg_color="black",
                                              command=self.deletestock)
        self.delete_stock_btn.pack(side="left", padx=10)

        self.guide_btn = ctk.CTkButton(self.navbar_frame,
                                       text="Your Trade Guide",
                                       width=200,
                                       height=40,
                                       font=("Helvetica", 16, "bold"),
                                       corner_radius=10,
                                       fg_color="black",
                                       command=self.guide)
        self.guide_btn.pack(side="left", padx=10)

        self.guide_btn = ctk.CTkButton(self.navbar_frame,
                                       text="Compare Stocks",
                                       width=200,
                                       height=40,
                                       font=("Helvetica", 16, "bold"),
                                       corner_radius=10,
                                       fg_color="black",
                                       command=self.cmpare)
        self.guide_btn.pack(side="left", padx=10)

        self.exit_btn = ctk.CTkButton(self.navbar_frame,
                                      text="Exit->",
                                      width=50,
                                      height=20,
                                      font=("Helvetica", 16, "bold"),
                                      corner_radius=10,
                                      fg_color="red",
                                      command=self.exit)
        self.exit_btn.pack(side="right", padx=20)

        # Scrollable Frame for News
        self.news_frame = ctk.CTkScrollableFrame(
            self.content_frame,
            width=500,
            height=400,
            fg_color="black",
            corner_radius=10,
            border_color="white",
            border_width=3)
        self.news_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Title for the news section
        self.news_title = ctk.CTkLabel(
            self.news_frame,
            text="Top Stories",
            font=("Helvetica", 24, "bold"),
            fg_color="black",
            text_color="white")
        self.news_title.pack(pady=10)

        # Loading indicator
        self.loading_label = ctk.CTkLabel(
            self.news_frame,
            text="Loading news...",
            font=("Helvetica", 14),
            text_color="white")
        self.loading_label.pack(pady=10)

        # Start fetching news in a separate thread
        threading.Thread(target=self.fetch_and_display_news).start()

    def fetch_and_display_news(self):
        """Fetch news from NewsAPI and display it in the news frame."""
        api_key = "7b578eb7e1b748b7b8d9d19200b731b8"
        url = f"https://newsapi.org/v2/everything?q=BSE+SENSEX&apiKey={api_key}"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            for i, article in enumerate(articles[:10]):  # Top 5 news
                title = article['title']
                source = article['source']['name']
                link = article['url']

                # Create a frame for each article
                article_frame = ctk.CTkFrame(self.news_frame, fg_color="black", corner_radius=10)
                article_frame.pack(pady=5, fill="x")

                # Title of the news article
                news_title_label = ctk.CTkLabel(
                    article_frame,
                    text=title,
                    font=("Helvetica", 18, "bold"),
                    wraplength=280,
                    text_color="white",
                    justify="left")
                news_title_label.pack(anchor="w", pady=5)

                # Source of the news
                news_source_label = ctk.CTkLabel(
                    article_frame,
                    text=f"Source: {source}",
                    font=("Helvetica", 12),
                    text_color="gray",
                    justify="left")
                news_source_label.pack(anchor="w", pady=5)

                # Button to open the news link
                news_link_btn = ctk.CTkButton(
                    article_frame,
                    text="Read More",
                    font=("Helvetica", 12, "bold"),
                    fg_color="blue",
                    hover_color="darkblue",
                    corner_radius=5,
                    command=lambda link=link: self.open_link(link))
                news_link_btn.pack(anchor="w", pady=5)
        else:
            # Handle failure to fetch news
            error_label = ctk.CTkLabel(
                self.news_frame,
                text="Failed to fetch news.",
                font=("Helvetica", 14, "bold"),
                text_color="red")
            error_label.pack(pady=10)

        # Remove loading indicator
        self.loading_label.destroy()

    def open_link(self, link):
        """Open a link in the default web browser."""
        webbrowser.open(link)

    def mystk(self):
        """Display saved stocks."""
        self.root.destroy()
        subprocess.Popen([sys.executable, "Main+GUI/AppFunctions/MyStocks.py"])

    def cmpare(self):
        """
        Comparing 2 stocks
        """
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/Comparison.py"])

    def addstock(self):
        """Add stocks to the database."""
        self.root.destroy()
        subprocess.Popen([sys.executable, "Main+GUI/AppFunctions/AddStock.py"])

    def deletestock(self):
        """Delete stocks from the database."""
        self.root.destroy()
        subprocess.Popen([sys.executable, "Main+GUI/AppFunctions/DeleteStock.py"])

    def guide(self):
        """Provide trading guidance."""
        self.root.destroy()
        subprocess.Popen([sys.executable, "Main+GUI/AppFunctions/StockGuide.py"])

    def exit(self):
        """Return to the main page."""
        self.root.destroy()
        subprocess.Popen([sys.executable, 'Main+GUI/MainPage.py'])

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Dashboard()
    app.run()