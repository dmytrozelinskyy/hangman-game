import customtkinter as ctk
import tkinter as tk


class VisualGameFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.controller = app.game_controller

        self.word_label = ctk.CTkLabel(self, font=("Helvetica", 24))
        self.word_label.pack(pady=20)

        self.canvas = tk.Canvas(self, width=200, height=250, bg="white")
        self.canvas.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="", font=("Segoe UI", 14))
        self.status_label.pack(pady=10)

        self.entry = ctk.CTkEntry(self, font=("Helvetica", 16))
        self.entry.pack()

        ctk.CTkButton(self, text="Guess", command=self.check_guess).pack(pady=10)
        ctk.CTkButton(self, text="Return to Main Menu", command=self.app.return_to_main_menu).pack(pady=10)

        try:
            self.update_word_display()
            self.draw_hangman()
        except Exception as e:
            self.app.show_error(str(e))

    def update_word_display(self):
        self.word_label.configure(text=self.controller.get_display_word())

    def draw_hangman(self):
        self.canvas.delete("all")
        wrong = 6 - self.controller.attempts

        self.canvas.create_line(20, 230, 180, 230)
        self.canvas.create_line(50, 230, 50, 20)
        self.canvas.create_line(50, 20, 130, 20)
        self.canvas.create_line(130, 20, 130, 40)

        # Body parts based on wrong guesses
        if wrong >= 1:
            self.canvas.create_oval(110, 40, 150, 80)  # head
        if wrong >= 2:
            self.canvas.create_line(130, 80, 130, 140)  # body
        if wrong >= 3:
            self.canvas.create_line(130, 100, 100, 120)  # left arm
        if wrong >= 4:
            self.canvas.create_line(130, 100, 160, 120)  # right arm
        if wrong >= 5:
            self.canvas.create_line(130, 140, 100, 180)  # left leg
        if wrong >= 6:
            self.canvas.create_line(130, 140, 160, 180)  # right leg

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
                self.status_label.configure(text=f"You won! Word: {self.controller.word}",
                                            font=("Segoe UI", 24, "bold"))
                self.app.after(2000, self.app.return_to_main_menu)
            case _:
                self.status_label.configure(text="")

        self.update_word_display()
        self.draw_hangman()

        if self.controller.is_game_over() and result != "win":
            self.entry.delete(0, ctk.END)
            self.status_label.configure(text=f"You lost! Word was: {self.controller.word}", font=("Segoe UI", 24, "bold"))
            self.app.after(2000, self.app.return_to_main_menu)
