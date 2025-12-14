import customtkinter as ctk
import re
from utils.email_utils import *


class RegistrationFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.entries = {}

        ctk.CTkLabel(self, text="Register New Account",
                     font=("Segoe UI", 24, "bold")).pack(pady=20)

        scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=400)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        fields = [
            ("Name", "Enter your first name"),
            ("Surname", "Enter your last name"),
            ("Age", "Enter your age"),
            ("Email", "Enter your email address"),
            ("Username", "Choose a username"),
            ("Password", "Choose a password")
        ]

        for field_name, placeholder in fields:
            ctk.CTkLabel(scrollable_frame, text=f"{field_name}:",
                         font=("Segoe UI", 14)).pack(pady=(15, 5))

            entry = ctk.CTkEntry(scrollable_frame, width=350, height=35,
                                 placeholder_text=placeholder,
                                 show="*" if field_name == "Password" else "")
            entry.pack(pady=5)
            self.entries[field_name.lower()] = entry

        self.message_label = ctk.CTkLabel(scrollable_frame, text="", text_color="red")
        self.message_label.pack(pady=15)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Register",
                      command=self.register_user,
                      width=120, height=35,
                      font=("Segoe UI", 14, "bold")).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Back",
                      command=self.app.return_to_main_menu,
                      width=120, height=35,
                      font=("Segoe UI", 14)).pack(side="left", padx=10)

    def register_user(self):
        name = self.entries["name"].get().strip()
        surname = self.entries["surname"].get().strip()
        age_str = self.entries["age"].get().strip()
        email = self.entries["email"].get().strip()
        username = self.entries["username"].get().strip()
        password = self.entries["password"].get()

        if not all([name, surname, age_str, email, username, password]):
            self.message_label.configure(text="All fields are required.", text_color="red")
            return

        # -- Validate age -- #
        try:
            age = int(age_str)
            if age < 1 or age > 120:
                raise ValueError
        except ValueError:
            self.message_label.configure(text="Please enter a valid age (1-120).", text_color="red")
            return

        # -- Validate username -- #
        if len(username) < 3:
            self.message_label.configure(text="Username must be at least 3 characters long.", text_color="red")
            return

        # -- Validate password -- #
        if len(password) < 6:
            self.message_label.configure(text="Password must be at least 6 characters long.", text_color="red")
            return

        success = self.app.register_user(name, surname, age, email, username, password)
        if success:
            self.message_label.configure(text="Registration successful! Welcome email sent.", text_color="green")
            self.app.login_user(username, password)

            for entry in self.entries.values():
                entry.delete(0, ctk.END)
            self.app.after(2000, self.app.return_to_main_menu)
        else:
            self.message_label.configure(text="Username or email already exists.", text_color="red")
