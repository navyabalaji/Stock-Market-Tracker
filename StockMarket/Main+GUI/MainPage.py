import customtkinter as ctk
import subprocess
import sys
from PIL import Image

class MainPage:
    def __init__(self):
        # Set appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure main window
        self.root = ctk.CTk()
        self.root.state("zoomed")
        self.root.title("StockSage")
        self.root.geometry("2000x1000")
        self.root.resizable(True, True)

        # Background frame
        self.bg_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.bg_frame.pack(fill="both", expand=True)

        # Content frame
        self.content_frame = ctk.CTkFrame(
            self.bg_frame,
            width=1200,
            height=800,
            corner_radius=15,
            fg_color="black"
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Background image
        bg_image = ctk.CTkImage(Image.open("Images/background.jpeg"), size=(1200, 800))
        self.img_label = ctk.CTkLabel(
            self.content_frame,
            image=bg_image,
            text=""
        )
        self.img_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

        # Title label
        self.title_label = ctk.CTkLabel(
            self.content_frame,
            text="Welcome to StockSage",
            font=("Helvetica", 72, "bold"),
            text_color="white"
        )
        self.title_label.place(relx=0.54, rely=0.2, anchor=ctk.CENTER)

        # Button frame
        self.button_frame = ctk.CTkFrame(
            self.content_frame,
            width=1000,
            height=200,
            fg_color="black",
            border_width=3,
            border_color="white",
            corner_radius=10
        )
        self.button_frame.place(relx=0.54, rely=0.5, anchor=ctk.CENTER)

        # Quote label
        self.quote = ctk.CTkLabel(
            self.button_frame,
            text=(
                "“The stock market is a device for transferring money "
                "from the impatient to the patient.”"
            ),
            font=("Helvetica", 18, "bold"),
            text_color="white"
        )
        self.quote.place(relx=0.5, rely=0.2, anchor=ctk.CENTER)

        # Author label
        self.auth = ctk.CTkLabel(
            self.button_frame,
            text="~Warren Buffet",
            font=("Helvetica", 18, "bold"),
            text_color="white"
        )
        self.auth.place(relx=0.8, rely=0.4, anchor=ctk.CENTER)

        # Client Login button
        self.client_btn = ctk.CTkButton(
            self.button_frame,
            text="Client Login",
            command=self.clientlogin,
            width=250,
            height=50,
            font=("Helvetica", 20, "bold"),
            corner_radius=10,
            fg_color="green",
            hover_color="gray"
        )
        self.client_btn.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

        # Exit button
        self.exit_btn = ctk.CTkButton(
            self.bg_frame,
            text="Exit",
            command=self.root.quit,
            width=100,
            height=40,
            fg_color="red",
            hover_color="darkred",
            font=("Helvetica", 16, "bold"),
            corner_radius=10
        )
        self.exit_btn.place(relx=0.53, rely=0.94, anchor=ctk.CENTER)

    def clientlogin(self):
        """Open Client Login page."""
        try:
            subprocess.Popen([sys.executable, "Main+GUI/ClientLogin.py"])
            self.root.destroy()
        except Exception as e:
            self.show_error(f"Error opening Client Login: {e}")

    def show_error(self, message):
        """Display an error message."""
        error_window = ctk.CTkToplevel(self.root)
        error_window.title("Error")
        error_window.geometry("300x150")

        # Error message label
        error_label = ctk.CTkLabel(
            error_window,
            text=message,
            wraplength=250
        )
        error_label.pack(pady=20)

        # Close button
        close_btn = ctk.CTkButton(
            error_window,
            text="Close",
            command=error_window.destroy
        )
        close_btn.pack(pady=10)

    def run(self):
        """Run the application."""
        self.root.mainloop()


# Run the application
if __name__ == "__main__":
    app = MainPage()
    app.run()