import customtkinter as ctk


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Login", font=("Segoe UI", 20, "bold")).pack(pady=30)

        ctk.CTkLabel(self, text="Username:", font=("Segoe UI", 14)).pack(pady=(20, 5))
        self.username_entry = ctk.CTkEntry(self, width=300, height=35, placeholder_text="Enter your username")
        self.username_entry.pack(pady=5)

        ctk.CTkLabel(self, text="Password:", font=("Segoe UI", 14)).pack(pady=(15, 5))
        self.password_entry = ctk.CTkEntry(self, width=300, height=35, placeholder_text="Enter your password", show="*")
        self.password_entry.pack(pady=5)

        self.message_label = ctk.CTkLabel(self, text="", text_color="red")
        self.message_label.pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Login",
                      command=self.login_user,
                      width=120, height=35,
                      font=("Segoe UI", 14, "bold")).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Back",
                      command=self.app.return_to_main_menu,
                      width=120, height=35,
                      font=("Segoe UI", 14)).pack(side="left", padx=10)

    def login_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.message_label.configure(text="Please enter both username and password.",
                                         text_color="red")
            return

        if self.app.login_user(username, password):
            self.message_label.configure(text="Login successful.", text_color="green")
            self.app.after(1000, self.app.return_to_main_menu)
        else:
            self.message_label.configure(text="Invalid username or password.", text_color="red")
            self.password_entry.delete(0, ctk.END)
