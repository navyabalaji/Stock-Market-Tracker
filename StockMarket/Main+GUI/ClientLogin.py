import customtkinter as ctk
from PIL import Image
import subprocess
import sys
import sqlite3
from tkinter import messagebox

# Database setup
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

class ClientLogin:
    def __init__(self):
      
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        
        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("Client Login")
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

        
        self.form_frame = ctk.CTkFrame(self.bg_frame, 
                                       width=400, 
                                       height=600,  
                                       fg_color="black",  
                                       corner_radius=15,
                                       border_color="white", 
                                       border_width=3)    
        self.form_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        
        self.title_label = ctk.CTkLabel(self.form_frame, 
                                        text="Client Login", 
                                        font=("Helvetica", 36, "bold"),
                                        text_color="white")
        self.title_label.place(relx=0.5, rely=0.1, anchor=ctk.CENTER)

    
        self.username_label = ctk.CTkLabel(self.form_frame, 
                                           text="Username", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.username_label.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)

        self.username_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           placeholder_text="Enter your username")
        self.username_entry.place(relx=0.5, rely=0.37, anchor=ctk.CENTER)

       
        self.password_label = ctk.CTkLabel(self.form_frame, 
                                           text="Password", 
                                           font=("Helvetica", 20),
                                           text_color="white")
        self.password_label.place(relx=0.5, rely=0.47, anchor=ctk.CENTER)

        self.password_entry = ctk.CTkEntry(self.form_frame, 
                                           width=300, 
                                           show="*", 
                                           placeholder_text="Enter your password")
        self.password_entry.place(relx=0.5, rely=0.54, anchor=ctk.CENTER)

        # Terms and Conditions Checkbox
        self.terms_var = ctk.BooleanVar(value=False)
        self.terms_checkbox = ctk.CTkCheckBox(
            self.form_frame,
            text="I agree to the Terms and Conditions",
            variable=self.terms_var,
            command=self.toggle_signin_button
        )
        self.terms_checkbox.place(relx=0.5, rely=0.62, anchor=ctk.CENTER)

        
        self.signin_btn = ctk.CTkButton(self.form_frame, 
                                        text="Sign In", 
                                        command=self.signin,
                                        width=250,
                                        height=40,
                                        font=("Helvetica", 18, "bold"),
                                        fg_color="green",
                                        corner_radius=10,
                                        state="disabled")  # Initially disabled
        self.signin_btn.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        
        self.signup_text = ctk.CTkLabel(self.form_frame, 
                                        text="Not a member? Sign up", 
                                        font=("Helvetica", 16),
                                        text_color="white")
        self.signup_text.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)

        
        self.signup_btn = ctk.CTkButton(self.form_frame, 
                                        text="Sign Up", 
                                        command=self.signup,
                                        width=250,
                                        height=40,
                                        fg_color="gray",
                                        hover_color="darkgray",
                                        font=("Helvetica", 18, "bold"),
                                        corner_radius=10)
        self.signup_btn.place(relx=0.5, rely=0.87, anchor=ctk.CENTER)

    def toggle_signin_button(self):
        """Enable or disable the Sign In button based on checkbox state."""
        if self.terms_var.get():
            self.signin_btn.configure(state="normal")
        else:
            self.signin_btn.configure(state="disabled")

    def signup(self):
        self.root.destroy()
        try:
            subprocess.Popen([sys.executable, "Main+GUI/ClientSignUp.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open signup page: {str(e)}")

    def signin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open("TemporaryUserDetails.txt","w") as tempdetails:
            tempdetails.write(username+'\n'+password)

      
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        try:
            cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
            users = cursor.fetchall()
            
            if users:
                messagebox.showinfo("Success!", "Logged in successfully!")
                subprocess.Popen([sys.executable, "Main+GUI/Dashboard.py"])
                self.root.destroy()
                self.clear_entries()
            else:
                messagebox.showerror("Error!", "Invalid username or password!")
                self.clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def clear_entries(self):
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ClientLogin()
    app.run()
