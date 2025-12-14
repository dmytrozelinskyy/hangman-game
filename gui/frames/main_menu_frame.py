import customtkinter as ctk
from gui.frames.login_frame import LoginFrame
from gui.frames.registration_frame import RegistrationFrame
from gui.frames.settings_frame import SettingsFrame
from gui.frames.scoreboard_frame import ScoreboardFrame
from gui.frames.gamemode_selection_frame import GameModeSelectionFrame


class MainMenuFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        # -- Title Label -- #
        ctk.CTkLabel(self, text="Hangman Game",
                     font=("Segoe UI", 24, "bold")).pack(pady=30)

        # -- User Status Label -- #
        if self.app.logged_in_user:
            status_text = f"Welcome, {self.app.logged_in_user.username}!"
            status_color = "green"
        else:
            status_text = "You should log in to play."
            status_color = "orange"

        ctk.CTkLabel(self, text=status_text,
                     font=("Segoe UI", 20, "bold"), text_color=status_color).pack(pady=(0, 20))

        # -- Custom Main Menu Button Style -- #
        button_config = {
            "width": 200,
            "height": 40,
            "corner_radius": 10,
            "font": ("Segoe UI", 14, "bold")
        }

        # -- Create Main Menu Buttons -- #
        if not self.app.logged_in_user:
            self.create_mm_button("Register", lambda: app.switch_frame(RegistrationFrame), **button_config)
            self.create_mm_button("Login", lambda: app.switch_frame(LoginFrame), **button_config)
        else:
            self.create_mm_button("Start Game", self.game_start_event, **button_config)
            self.create_mm_button("Logout", self.logout_event, **button_config)

        self.create_mm_button("Settings", lambda: app.switch_frame(SettingsFrame), **button_config)
        self.create_mm_button("Scoreboard", lambda: app.switch_frame(ScoreboardFrame), **button_config)
        self.create_mm_button("Exit", lambda: app.quit(), **button_config)

    # -- Create Button with Custom Style Function -- #
    def create_mm_button(self, text, command, **kwargs):
        ctk.CTkButton(self, text=text, command=command, **kwargs).pack(pady=10)

    def game_start_event(self):
        if not self.app.logged_in_user:
            self.app.show_error("You must be logged in to start a game.")
        else:
            self.app.switch_frame(GameModeSelectionFrame)

    def logout_event(self):
        self.app.logout_user()
        self.app.return_to_main_menu()
