import customtkinter as ctk
from services.word_service import *
from services.user_service import *
from gui.frames.main_menu_frame import MainMenuFrame
from gui.frames.error_frame import ErrorFrame
from gui.frames.classic_game_frame import ClassicGameFrame
from gui.frames.visual_game_frame import VisualGameFrame
from controllers.game_controller import GameController
from utils.email_utils import send_welcome_email


class HangmanWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("900x700")
        self.resizable(True, True)

        # -- Set Appearance and Theme -- #
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")

        # -- Initialize App Font -- #
        self.app_font = ctk.CTkFont(family="Segoe UI", size=16)

        # -- Initialize Game Components -- #
        self.game_controller = GameController()
        self.logged_in_user = None

        # -- Create Main Container -- #
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.current_frame = None

        self.intialize_db()
        self.return_to_main_menu()

    def switch_frame(self, frame_class, **kwargs):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame_class(self.container, self, **kwargs)
        self.current_frame.pack(fill="both", expand=True)

    def return_to_main_menu(self):
        self.switch_frame(MainMenuFrame)

    def register_user(self, name, surname, age, email, username, password):
        success = create_user(name, surname, age, email, username, password)
        if success:
            try:
                send_welcome_email(email, username)
            except Exception as e:
                print(f"Failed to send welcome email: {e}")
        return success

    def login_user(self, username, password):
        user = get_user_by_credentials(username, password)
        if user:
            self.logged_in_user = user
            self.game_controller.username = user.username
            return True
        return False

    def logout_user(self):
        self.logged_in_user = None
        self.game_controller.username = None
        self.game_controller.reset_game()

    def add_new_word(self, word, category):
        return add_word(word, category)

    def add_new_category(self, category):
        return add_category(category)

    def intialize_db(self):
        with SessionLocal() as session:
            if session.query(Category).count() > 0:
                return

        # -- Add Default Categories and Words -- #
        default_data = {
            "food": ["apple", "banana", "orange", "pizza", "hotdog", "hamburger", "fries", "candy", "croissant"],
            "transport": ["car", "plane", "train", "bicycle", "motorcycle", "boat"],
            "toys": ["cube", "monopoly", "ball", "robot", "car", "puzzle"],
            "animals": ["elephant", "lion", "whale", "parrot", "dog", "cat", "penguin", "kangaroo", "butterfly", "shark", "tiger"],
            "technology": ["computer", "smartphone", "internet", "software", "hardware", "database"]
        }

        for category_name, words in default_data.items():
            self.add_new_category(category_name)
            for word in words:
                self.add_new_word(word, category_name)

    def show_error(self, msg):
        self.switch_frame(ErrorFrame, message=msg)

    def change_mode(self, mode):
        ctk.set_appearance_mode(mode.lower())

    def change_theme(self, theme):
        ctk.set_default_color_theme(theme)

    def update_font_size(self, value):
        self.app_font.configure(size=int(value))
        if self.current_frame:
            current_frame_class = type(self.current_frame)
            self.switch_frame(current_frame_class)

    def assign_word(self, word):
        self.game_controller.word = word

    def assign_attempts(self, att: int):
        self.game_controller.attempts = att
        self.game_controller.max_attempts = att

    def enable_pvp(self):
        self.game_controller.is_pvp = True

    def start_classic_game(self, category):
        self.game_controller.start_new_game(category=category)
        self.switch_frame(ClassicGameFrame)

    def start_visual_game(self, category):
        self.game_controller.start_new_game(category=category)
        self.switch_frame(VisualGameFrame)
