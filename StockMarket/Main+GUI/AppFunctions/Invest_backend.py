#Gives suggestions to the user concerning investments

#importing necessary modules
import customtkinter as ctk
from PIL import Image
from Stock import Stock
import subprocess, sys

class Investment:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Invest")
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
        with open('Invest.txt', 'r') as file:
            lines = file.readlines()
            details = [line.strip().lower() for line in lines]
        stk = Stock(details[0], details[1])  # Symbol and company name
        mydata = stk.get_historical_data('1mo')

        # Analysis logic
        highest_price = mydata['Highest Price'].max()
        closing_price = mydata['Closing Price'].iloc[-1]

        price_std = mydata['Closing Price'].std()
        price_change = ((mydata['Closing Price'].iloc[-1] - mydata['Closing Price'].iloc[0]) / 
                        (mydata['Closing Price'].iloc[0])) * 100

        # Recommendation based on analysis
        if price_change > 10:
            recommendation = "The stock has increased significantly, consider investing."
        elif price_std < 25:
            recommendation = "The stock price is stable, making it a safer investment."
        elif highest_price > closing_price * 1.2:
            recommendation = "The stock has had a significant peak, but be cautious."
        else:
            recommendation = "The stock is inconsistent, consider holding off on investment."

        # Form Frame
        self.form_frame = ctk.CTkFrame(
            self.bg_frame,
            width=900,
            height=400,  # Increased height to better accommodate content
            fg_color="black",
            corner_radius=15,
            border_color="white",
            border_width=3
        )
        self.form_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Bot Image
        bot_image = ctk.CTkImage(Image.open(r"Images\Bot.jpeg"), size=(200, 150))
        self.bot_label = ctk.CTkLabel(self.form_frame, image=bot_image, text="")
        self.bot_label.place(relx=0.12, rely=0.25, anchor=ctk.CENTER)  # Adjusted vertical position

        # Recommendation Label
        self.rec_label = ctk.CTkLabel(self.form_frame,
                                      text="Recommendation",
                                      font=('Helvetica', 36, "bold"),
                                      text_color="white")
        self.rec_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)  # Centered title

        # Suggestion Text
        self.sug_label = ctk.CTkLabel(self.form_frame,
                                      text=recommendation,
                                      font=('Helvetica', 20, "bold"),
                                      text_color="white")
        self.sug_label.place(relx=0.5, rely=0.4, anchor=ctk.CENTER)  # Positioned below the title

        # Current Price Info
        self.inf_label = ctk.CTkLabel(self.form_frame,
                                      text="Current Price: " + str(stk.get_latest_data()['Latest Price']),
                                      font=('Helvetica', 20, "bold"),
                                      text_color="white")
        self.inf_label.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)  # Positioned below suggestion

        # Back Button
        self.back_btn = ctk.CTkButton(self.form_frame, 
                                      text="Back to Guide", 
                                      width=250,
                                      height=40,
                                      font=("Helvetica", 18, "bold"),
                                      corner_radius=10,
                                      fg_color="red",
                                      command=self.back)
        self.back_btn.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)  # Positioned near the bottom

    def back(self):
        self.root.destroy()
        subprocess.Popen([sys.executable, 'Main+GUI/AppFunctions/StockGuide.py'])

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Investment()
    app.run()