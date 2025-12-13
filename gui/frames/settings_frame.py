import customtkinter as ctk
from services.user_service import *


class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.game_controller = app.game_controller

        ctk.CTkLabel(self, text="Settings",
                     font=("Segoe UI", 24, "bold")).pack(pady=20)

        scrollable_frame = ctk.CTkScrollableFrame(self, width=500, height=450)
        scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # -- Appearance Settings -- #
        appearance_frame = ctk.CTkFrame(scrollable_frame)
        appearance_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(appearance_frame, text="Appearance Settings",
                     font=("Segoe UI", 18, "bold")).pack(pady=10)

        # -- Theme Mode -- #
        ctk.CTkLabel(appearance_frame, text="Appearance Mode:",
                     font=("Segoe UI", 14)).pack(pady=(10, 2))
        self.mode_option = ctk.CTkOptionMenu(
            appearance_frame,
            width=200,
            values=["Light", "Dark", "System"],
            command=self.app.change_mode
        )
        self.mode_option.set(ctk.get_appearance_mode())
        self.mode_option.pack(pady=5)

        # -- Color Theme -- #
        ctk.CTkLabel(appearance_frame, text="Color Theme:",
                     font=("Segoe UI", 14)).pack(pady=(15, 2))
        self.color_option = ctk.CTkOptionMenu(
            appearance_frame, values=["blue", "dark-blue", "green"],
            command=self.app.change_theme, width=200
        )
        self.color_option.set("green")
        self.color_option.pack(pady=5)

        # -- Game Content Settings -- #
        content_frame = ctk.CTkFrame(scrollable_frame)
        content_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(content_frame, text="Game Content",
                     font=("Segoe UI", 18, "bold")).pack(pady=10)

        # -- Add New Word Section -- #
        ctk.CTkLabel(content_frame, text="Add New Word:",
                     font=("Segoe UI", 14, "bold")).pack(pady=(15, 5))

        self.new_word = ctk.CTkEntry(content_frame, placeholder_text="Enter word", width=250)
        self.new_word.pack(pady=5)

        self.new_word_cat = ctk.CTkEntry(content_frame, placeholder_text="Enter category", width=250)
        self.new_word_cat.pack(pady=5)

        ctk.CTkButton(content_frame, text="Add Word", command=self.add_word, width=150).pack(pady=5)

        # -- Add New Category Section -- #
        ctk.CTkLabel(content_frame, text="Add New Category:",
                     font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))

        self.new_cat = ctk.CTkEntry(content_frame, placeholder_text="Enter category name", width=250)
        self.new_cat.pack(pady=5)

        ctk.CTkButton(content_frame, text="Add Category", command=self.add_category, width=150).pack(pady=5)

        # -- Reset Password Section -- #
        ctk.CTkLabel(content_frame, text="Reset User Password:",
                     font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))

        self.reset_user = ctk.CTkEntry(content_frame, placeholder_text="Enter username", width=250)
        self.reset_user.pack(pady=5)

        self.reset_email = ctk.CTkEntry(content_frame, placeholder_text="Enter registered email", width=250)
        self.reset_email.pack(pady=5)

        ctk.CTkButton(content_frame, text="Reset Password", command=self.reset_password, width=150).pack(pady=5)

        # -- Status Message -- #
        self.status_label = ctk.CTkLabel(content_frame, text="", text_color="green")
        self.status_label.pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Back",
                      command=self.app.return_to_main_menu,
                      width=120, height=35,
                      font=("Segoe UI", 14)).pack(side="left", padx=10, pady=10)

    # -- Add New Word to Database -- #
    def add_word(self):
        word = self.new_word.get().strip().lower()
        category = self.new_word_cat.get().strip().lower()

        if not word or not category:
            self.status_label.configure(text="Both word and category are required.", text_color="red")
            return

        if len(word) < 2:
            self.status_label.configure(text="Word must be at least 2 characters long.", text_lor="red")
            return

        if not word.isalpha():
            self.status_label.configure(text="Word must contain only letters.", text_color="red")
            return

        success = self.app.add_new_word(word, category)

        if success:
            self.status_label.configure(text=f"Word '{word}' added successfully!", text_color="green")
            self.new_word.delete(0, ctk.END)
            self.new_word_cat.delete(0, ctk.END)
        else:
            self.status_label.configure(text="Word already exists or category not found.", text_color="red")

    # -- Add New Category to Database -- #
    def add_category(self):
        category = self.new_cat.get().strip().lower()

        if not category:
            self.status_label.configure(text="Category name is required.", text_color="red")
            return

        if len(category) < 2:
            self.status_label.configure(text="Category name must be at least 2 characters long.", text_color="red")
            return

        success = self.app.add_new_category(category)

        if success:
            self.status_label.configure(text=f"Category '{category}' added successfully!", text_color="green")
            self.new_cat.delete(0, ctk.END)
        else:
            self.status_label.configure(text="Category already exists.", text_color="red")

    def reset_password(self):
        username = self.reset_user.get().strip()
        email = self.reset_email.get().strip()

        if not username or not email:
            self.status_label.configure(text="Username and email required.", text_color="red")
            return

        user = get_user_by_username(username)
        if not user or user.email.lower() != email.lower():
            self.status_label.configure(text="Invalid user or email.", text_color="red")
            return

        new_password = reset_password(username)
        if new_password:
            from utils.email_utils import send_reset_password_email
            sent = send_reset_password_email(email, username, new_password)
            self.status_label.configure(text="Password reset email sent.", text_color="green")
        else:
            self.status_label.configure(text="Password reset failed.", text_color="red")
