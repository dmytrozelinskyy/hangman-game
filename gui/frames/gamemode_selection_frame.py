import customtkinter as ctk
from gui.frames.pvp_setup_frame import PvPSetupFrame
from services.word_service import get_categories


class GameModeSelectionFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Choose Game Mode",
                     font=("Segoe UI", 24, "bold")).pack(pady=40)

        ctk.CTkLabel(self, text="Select your preferred game mode:",
                     font=("Segoe UI", 16),
                     text_color="gray").pack(pady=(0, 30))

        button_config = {
            "width": 250,
            "height": 50,
            "corner_radius": 15,
            "font": ("Segoe UI", 16, "bold")
        }

        categories = get_categories()
        categories.insert(0, "Random")
        self.category_var = ctk.StringVar(value=categories[0] if categories else "")
        ctk.CTkLabel(self, text="Choose Category:").pack(pady=(10, 5))
        self.category_menu = ctk.CTkOptionMenu(self, values=categories, variable=self.category_var)
        self.category_menu.pack(pady=5)

        modes_selection = ctk.CTkFrame(self)
        modes_selection.pack(pady=20, padx=40, fill="x")

        # -- Classic Game Mode -- #
        classic_game_frame = ctk.CTkFrame(modes_selection)
        classic_game_frame.pack(pady=15)

        ctk.CTkButton(classic_game_frame, text="Classic Mode",
                      command=lambda: app.start_classic_game(self.category_menu.get()),
                      **button_config).pack(pady=10, padx=10)
        ctk.CTkLabel(classic_game_frame, text="Text-based hangman game",
                     font=("Segoe UI", 12),
                     text_color="gray").pack()

        # -- Visual Game Mode -- #
        visual_game_frame = ctk.CTkFrame(modes_selection)
        visual_game_frame.pack(pady=15)

        ctk.CTkButton(visual_game_frame, text="Visual Mode",
                      command=lambda: app.start_visual_game(self.category_menu.get()),
                      **button_config).pack(pady=10, padx=10)
        ctk.CTkLabel(visual_game_frame, text="Hangman with visual drawing",
                     font=("Segoe UI", 12),
                     text_color="gray").pack()

        # -- PvP Mode -- #
        pvp_frame = ctk.CTkFrame(modes_selection)
        pvp_frame.pack(pady=15)

        ctk.CTkButton(visual_game_frame, text="Player vs Player",
                      command=lambda: app.switch_frame(PvPSetupFrame),
                      **button_config).pack(pady=10, padx=10)
        ctk.CTkLabel(visual_game_frame, text="Add your own word for others to guess",
                     font=("Segoe UI", 12),
                     text_color="gray").pack()

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        # -- Back Button -- #
        ctk.CTkButton(button_frame, text="Back",
                      command=self.app.return_to_main_menu,
                      width=120, height=35,
                      font=("Segoe UI", 14)).pack(side="left", padx=10, pady=10)
