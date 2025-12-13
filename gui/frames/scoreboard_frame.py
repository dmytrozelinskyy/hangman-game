import customtkinter as ctk
from services.scores_service import *


class ScoreboardFrame(ctk.CTkFrame):
    def __init__(self, master, app)\
            :
        super().__init__(master)
        self.app = app

        ctk.CTkLabel(self, text="Scoreboard",
                     font=("Segoe UI", 20, "bold")).pack(pady=20)

        scores = get_top_scores(15)

        if not scores:
            ctk.CTkLabel(self, text="No scores available.",
                         font=("Segoe UI", 16),
                         text_color="gray").pack(pady=50)
        else:
            # -- Create scrollable frame for scores -- #
            scrollable_frame = ctk.CTkScrollableFrame(self, width=600, height=400)
            scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

            header_frame = ctk.CTkFrame(scrollable_frame)
            header_frame.pack(fill="x", pady=(0, 10), padx=10)

            ctk.CTkLabel(header_frame, text="Rank",
                         font=("Segoe UI", 14, "bold"), width=80).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(header_frame, text="Player",
                         font=("Segoe UI", 14, "bold"), width=250).pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(header_frame, text="Score",
                         font=("Segoe UI", 14, "bold"), width=100).pack(side="left", padx=10, pady=10)

            # -- Score entries -- #
            for i, (username, score) in enumerate(scores, 1):
                score_frame = ctk.CTkFrame(scrollable_frame)
                score_frame.pack(fill="x", pady=2, padx=10)

                # -- Highlight current user -- #
                if self.app.logged_in_user and username == self.app.logged_in_user.username:
                    score_frame.configure(fg_color=("gray70", "gray30"))

                rank_text = f"{i}"
                if i == 1:
                    rank_text = "🥇 1"
                elif i == 2:
                    rank_text = "🥈 2"
                elif i == 3:
                    rank_text = "🥉 3"

                ctk.CTkLabel(score_frame, text=rank_text,
                             font=("Segoe UI", 12, "bold"), width=80).pack(side="left", padx=10, pady=8)

                ctk.CTkLabel(score_frame, text=username,
                             font=("Segoe UI", 12), width=250).pack(side="left", padx=10, pady=8)

                ctk.CTkLabel(score_frame, text=str(score),
                             font=("Segoe UI", 12, "bold"), width=100).pack(side="left", padx=10, pady=8)

        # User rank info
        if self.app.logged_in_user:
            user_rank = get_user_rank(self.app.logged_in_user.username)
            if user_rank > 0:
                rank_text = f"Your current rank: #{user_rank}"
                if user_rank <= 15:
                    rank_text += " (shown above)"

                ctk.CTkLabel(self, text=rank_text,
                             font=("Segoe UI", 14, "bold"),
                             text_color="blue").pack(pady=10)

        # -- Refresh/Back Buttons -- #
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Refresh",
                      command=self.refresh_scores,
                      width=120, height=35,
                      font=("Segoe UI", 14, "bold")).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(button_frame, text="Back",
                      command=self.app.return_to_main_menu,
                      width=120, height=35,
                      font=("Segoe UI", 14)).pack(side="left", padx=10)

    def refresh_scores(self):
        self.app.switch_frame(ScoreboardFrame)
