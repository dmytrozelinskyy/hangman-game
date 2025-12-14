import customtkinter as ctk


class ErrorFrame(ctk.CTkFrame):
    def __init__(self, parent, app, message: str):
        super().__init__(parent)
        self.app = app

        ctk.CTkLabel(self, text="Error", font=("Segoe UI", 20, "bold"), text_color="red").pack(pady=20)
        ctk.CTkLabel(self, text=message, font=("Segoe UI", 16), text_color="red").pack(pady=10)

        ctk.CTkButton(self, text="Return to Main Menu", command=self.app.return_to_main_menu).pack(pady=20)
