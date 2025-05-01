##Deleting the stock the user has added 

#Importing the necessary modules
import customtkinter as ctk
from tkinter import messagebox
import sys
import subprocess
import sqlite3
from PIL import Image

mydb=sqlite3.connect('stocks.db')
cursor=mydb.cursor()

usersdb=sqlite3.connect('users.db')
usercursor=usersdb.cursor()

class DeleteStock:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root=ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Delete stock")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        self.bg_frame=ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both",expand=True)

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
                                        text="Delete Stock", 
                                        font=("Helvetica", 36, "bold"),
                                        text_color="white")
        self.title_label.place(relx=0.5, rely=0.05, anchor=ctk.CENTER)  

        
        self.username_label = ctk.CTkLabel(self.form_frame, 
                                           text="Username", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.username_label.place(relx=0.5, rely=0.15, anchor=ctk.CENTER)
        self.username_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           placeholder_text="Enter your username")
        self.username_entry.place(relx=0.5, rely=0.25, anchor=ctk.CENTER)

        
        self.symbol_label = ctk.CTkLabel(self.form_frame, 
                                           text="Stock Symbol", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.symbol_label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)
        self.symbol_entry = ctk.CTkEntry(self.form_frame, 
                                        width=300, 
                                        placeholder_text="Enter symbol of the stock")
        self.symbol_entry.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        self.delete_button=ctk.CTkButton(self.form_frame,
                                         text="Delete stock",
                                         width=250,
                                         height=40,
                                         font=("Helvetica", 18, "bold"),
                                         corner_radius=10,
                                         fg_color="red",
                                         command=self.delete)
        self.delete_button.place(relx=0.5,rely=0.55,anchor=ctk.CENTER)

        self.back_button=ctk.CTkButton(self.form_frame,
                                       text="Back to dashboard",
                                       width=250,
                                       height=40,
                                       font=("Helvetica",18,"bold"),
                                       corner_radius=10,
                                       fg_color="orange",
                                       command=self.back)
        self.back_button.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)

    def back(self):
        """
        Navigating back to the dashboard
        """
        self.root.destroy()
        subprocess.Popen([sys.executable,"Main+GUI/Dashboard.py"])

    def delete(self):
        """
        Deleting the data from the database
        """
        username=(self.username_entry.get()).strip()
        symbol=((self.symbol_entry.get()).strip()).upper()+'.NS'
        
        if not username or not symbol:
            messagebox.showwarning("Warning","Please fill in both the fields")
            return
        
        # Check if username exists
        usercursor.execute("SELECT username FROM users WHERE username=?", (username,))
        if not usercursor.fetchone():
            messagebox.showerror("Error", "Username doesn't exist")
            return
        
        # Check if this specific stock has been added or not
        cursor.execute("SELECT *FROM Stocks WHERE Username=? AND StockSymbol=?", (username, symbol))
        existing_record = cursor.fetchone()
        if not existing_record:
            messagebox.showerror("Error", "Stock hasn't been added")
            return
    
         #Delete the stock
        cursor.execute("DELETE FROM stocks WHERE Username=? AND StockSymbol=?",(username,symbol))
        mydb.commit()
        messagebox.showinfo("Success", "Stock deleted successfully!")

    def run(self):
        self.root.mainloop()

if __name__=="__main__":
    app=DeleteStock()
    app.run()