import customtkinter as ctk
import re
from gui.frames.classic_game_frame import ClassicGameFrame

class PvPSetupFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Player vs Player Setup",
                     font=("Segoe UI", 24, "bold")).pack(pady=30)

        instructions = ctk.CTkFrame(self)
        instructions.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(instructions, text="Instructions:",
                     font=("Segoe UI", 16, "bold")).pack(pady=(10, 5))

        instruction_text = """
        1. Enter a word or phrase for someone else to guess
        2. Optionally add a hint to help the guesser
        3. Click 'Create Game' to start
        4. Share the game with someone to let them guess!

        Rules:
        • Only letters and spaces are allowed
        • Word must be at least 3 characters long
        • No numbers or special characters
        """

        ctk.CTkLabel(instructions, text=instruction_text,
                     font=("Segoe UI", 12), justify="left").pack(pady=5, padx=20)

        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=20, padx=40, fill="x")

        ctk.CTkLabel(input_frame, text="Enter your word or phrase:",
                     font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))

        self.word_entry = ctk.CTkEntry(input_frame, width=300, height=40,
                                       placeholder_text="Enter word here...",
                                       font=("Segoe UI", 14))
        self.word_entry.pack(pady=5)

        # Difficulty selection
        ctk.CTkLabel(input_frame, text="Select difficulty:",
                     font=("Segoe UI", 14, "bold")).pack(pady=(20, 5))

        self.difficulty_var = ctk.StringVar(value="Normal")
        difficulty_frame = ctk.CTkFrame(input_frame)
        difficulty_frame.pack(pady=5)

        difficulties = [("Easy (8 attempts)", "Easy"),
                        ("Normal (6 attempts)", "Normal"),
                        ("Hard (4 attempts)", "Hard")]

        for text, value in difficulties:
            ctk.CTkRadioButton(difficulty_frame, text=text, variable=self.difficulty_var,
                               value=value, font=("Segoe UI", 12)).pack(side="left", padx=20)

        self.message_label = ctk.CTkLabel(input_frame, text="", font=("Segoe UI", 12))
        self.message_label.pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Create Game",
                      command=self.create_game, width=150, height=40,
                      font=("Segoe UI", 14, "bold")).pack(side="left", padx=10)

        ctk.CTkButton(button_frame, text="Back",
                      command=self.app.return_to_main_menu, width=150, height=40,
                      font=("Segoe UI", 14)).pack(side="left", padx=10)

    def validate_word(self, word):
        if not word:
            return False, "Please enter a word."

        if len(word.strip()) < 3:
            return False, "Word must be at least 3 characters long."

        if not re.match("^[a-zA-Z ]+$", word):
            return False, "Word can only contain letters and spaces."

        if not any(c.isalpha() for c in word):
            return False, "Word must contain at least one letter."

        return True, "Valid word."

    def create_game(self):
        word = self.word_entry.get().strip()
        difficulty = self.difficulty_var.get()

        is_valid, message = self.validate_word(word)
        if not is_valid:
            self.message_label.configure(text=message, text_color="red")
            return

        attempts_map = {"Easy": 8, "Normal": 6, "Hard": 4}
        max_attempts = attempts_map.get(difficulty, 6)

        self.app.assign_word(word)
        self.app.assign_attempts(max_attempts)
        self.app.enable_pvp()

        self.message_label.configure(text="Game created successfully!", text_color="green")

        self.app.switch_frame(ClassicGameFrame)
