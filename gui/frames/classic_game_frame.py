import customtkinter as ctk


class ClassicGameFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.controller = app.game_controller

        self.word_label = ctk.CTkLabel(self, font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 14))
        self.status_label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, font=("Helvetica", 16))
        self.entry.pack()

        ctk.CTkButton(self, text="Guess", command=self.check_guess).pack(pady=10)
        ctk.CTkButton(self, text="Return to Main Menu", command=self.app.return_to_main_menu).pack(pady=10)

        try:
            self.update_word_display()
        except Exception as e:
            self.app.show_error(str(e))

    def update_word_display(self):
        self.word_label.configure(text=self.controller.get_display_word())

    def check_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, ctk.END)

        if not guess or not guess.isalpha() or len(guess) != 1:
            self.status_label.configure(text="Enter a single letter.")
            return

        result = self.controller.guess_letter(guess)

        match result:
            case "already":
                self.status_label.configure(text="Already guessed.")
            case "wrong":
                self.status_label.configure(text=f"Wrong! Attempts left: {self.controller.attempts}")
            case "correct":
                self.status_label.configure(text="Correct!")
            case "win":
                self.status_label.configure(text=f"You won! Word: {self.controller.word}", font=("Segoe UI", 24, "bold"))
                self.app.after(2000, self.app.return_to_main_menu)
            case _:
                self.status_label.configure(text="")

        self.update_word_display()

        if self.controller.is_game_over() and result != "win":
            self.status_label.configure(text=f"You lost! Word was: {self.controller.word}", font=("Segoe UI", 24, "bold"))
            self.app.after(3000, self.app.return_to_main_menu())

