import customtkinter as ctk
from services.user_service import *
from utils.email_utils import send_reset_password_email


class ForgotPasswordFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Reset Password", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Registered Email")
        self.email_entry.pack(pady=10)

        ctk.CTkButton(self, text="Send Reset Email", command=self.reset_password).pack(pady=15)
        ctk.CTkButton(self, text="Back", command=self.app.return_to_main_menu).pack(pady=5)

    def reset_password(self):
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()

        user = get_user_by_username(username)
        if not user or user.email.lower() != email.lower():
            self.app.show_error("Invalid username or email.")
            return

        new_password = reset_password(username)
        if not new_password:
            self.app.show_error("Password reset failed.")
            return

        if send_reset_password_email(email, username, new_password):
            self.app.show_info("Reset email sent.")
        else:
            self.app.show_error("Email sending failed.")
