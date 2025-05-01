#Selling stocks


#importing necessary modules
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import subprocess
import sqlite3
import sys

class SellStocks:
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

        
        self.form_frame = ctk.CTkFrame(self.content_frame, 
                                       width=400, 
                                       height=600, 
                                       fg_color="black",
                                       corner_radius=15,
                                       border_color='white',
                                       border_width=3)
        self.form_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

       
        self.title_label = ctk.CTkLabel(self.form_frame, 
                                        text="Details", 
                                        font=("Helvetica", 36, "bold"),
                                        text_color="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)  

        
        self.symbol_label = ctk.CTkLabel(self.form_frame, 
                                           text="Symbol", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.symbol_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)

        self.symbol_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           placeholder_text="Enter symbol of stock you wish to sell")
        self.symbol_entry.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        
        self.cmpname_label = ctk.CTkLabel(self.form_frame, 
                                           text="Company Name", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.cmpname_label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)

        self.cmpname_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           placeholder_text="Enter the company name")
        self.cmpname_entry.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        self.date_label = ctk.CTkLabel(self.form_frame, 
                                           text="Date (yyyy/mm/dd)", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.date_label.place(relx=0.5, rely=0.55, anchor=ctk.CENTER)
        self.date_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300,
                                           placeholder_text="Enter date on which stocks were bought")
        self.date_entry.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

        self.enter_btn = ctk.CTkButton(self.form_frame, 
                                        text="Enter", 
                                        width=250,
                                        height=40,
                                        font=("Helvetica", 18, "bold"),
                                        corner_radius=10,
                                        fg_color="green",
                                        command=self.sell_guide)
        self.enter_btn.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

        self.back_btn = ctk.CTkButton(self.form_frame, 
                                        text="Back to Guide", 
                                        width=250,
                                        height=40,
                                        font=("Helvetica", 18, "bold"),
                                        corner_radius=10,
                                        fg_color="red",
                                        command=self.back)
        self.back_btn.place(relx=0.5, rely=0.85, anchor=ctk.CENTER)
    
    def sell_guide(self):
        """
        Gives suggestions concerning selling
        """
        self.details = [self.symbol_entry.get(), self.cmpname_entry.get()]
        with open("Sell.txt","w") as file:
            file.write(((self.symbol_entry.get()).strip()).upper()+'.NS'+'\n'+self.cmpname_entry.get()+'\n'+self.date_entry.get())
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/Sell_backend.py"])

    def back(self):
        """
        Helping user navigate back to the guide
        """
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/AppFunctions/StockGuide.py"])

    
    def run(self):
        self.root.mainloop()

if __name__=="__main__":
    app=SellStocks()
    app.run()