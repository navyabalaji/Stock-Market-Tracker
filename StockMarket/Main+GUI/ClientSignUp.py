import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import subprocess
import sqlite3
import sys

# Setting up the users database
mydb = sqlite3.connect('users.db')
cursor = mydb.cursor()
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
mydb.commit()

class ClientSignUp:
    def __init__(self):
       
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        
        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Client Sign Up")
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
                                        text="Sign Up", 
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

        
        self.password_label = ctk.CTkLabel(self.form_frame, 
                                           text="Password", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.password_label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)

        self.password_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           show="*", 
                                           placeholder_text="Enter your password")
        self.password_entry.place(relx=0.5, rely=0.45, anchor=ctk.CENTER)

        self.signup_btn = ctk.CTkButton(self.form_frame, 
                                        text="Sign Up", 
                                        command=self.signup,
                                        width=250,
                                        height=40,
                                        font=("Helvetica", 18, "bold"),
                                        corner_radius=10,
                                        fg_color="green")
        self.signup_btn.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)

    
        self.login_btn = ctk.CTkButton(self.form_frame, 
                                       text="Back to Login", 
                                       command=self.back_to_login,
                                       width=250,
                                       height=40,
                                       fg_color="orange",
                                       hover_color="darkgray",
                                       font=("Helvetica", 18, "bold"),
                                       corner_radius=10)
        self.login_btn.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)

    def signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            mydb.commit()
            messagebox.showinfo("Success!", "User registered successfully. Please login again")
            self.back_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def back_to_login(self):
        try:
            subprocess.Popen([sys.executable, "Main+GUI/ClientLogin.py"])
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not open login page: {str(e)}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ClientSignUp()
    app.run()
