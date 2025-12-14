import logging
from services.user_service import get_user_by_credentials, update_score
from services.word_service import get_random_word

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GameController:
    def __init__(self):
        self.username = None
        self.word = ""
        self.guessed = set()
        self.attempts = 6
        self.max_attempts = 6
        self.is_pvp = False

    # -- User Login Function -- #
    def login(self, username: str, password: str):
        user = get_user_by_credentials(username, password)
        if not user:
            logger.warning("Login was not successful for user: %s", username)
            raise ValueError("Invalid username or password.")
        self.username = user.username
        logger.info("User %s logged in successfully.", self.username)
        return user

    # -- Start New Game Function -- #
    def start_new_game(self, category: str = None) -> str:
        if not self.is_pvp:
            word = get_random_word(category)
            print(word)
            if not word:
                raise ValueError(f"No words found for category '{category}'.")
            self.word = word.lower()
            self.guessed = set()
            self.attempts = 6
            logger.info("New game started for user '%s' with word: %s", self.username, self.word)
        return self.get_display_word()

    # -- Guess Letter Function -- #
    def guess_letter(self, letter: str) -> str:
        if not letter.isalpha() or len(letter) != 1:
            raise ValueError("Please guess a single alphabetical character.")
        letter = letter.lower()
        if letter in self.guessed:
            return "already"

        self.guessed.add(letter)

        if letter not in self.word:
            self.attempts -= 1
            logger.info("Incorrect guess: '%s'. Attempts left: %d", letter, self.attempts)
            if self.attempts <= 0:
                return "lose"
            return "wrong"
        else:
            logger.info("Correct guess: %s", letter)
            if all(c in self.guessed for c in self.word):
                update_score(self.username, increment=1)
                logger.info("User '%s' won the game.", self.username)
                return "win"
            return "correct"

    # -- Get Display Word -- #
    def get_display_word(self):
        return ' '.join([c if c in self.guessed else '_' for c in self.word])

    # -- Game Over Check -- #
    def is_game_over(self):
        return self.attempts <= 0 or all(c in self.guessed for c in self.word if c.isalpha())

    # -- Game Won Check -- #
    def is_game_won(self):
        return all(c in self.guessed for c in self.word if c.isalpha())

    # -- Get Game State -- #
    def get_game_state(self) -> dict:
        return {
            "word_display": self.get_display_word(),
            "attempts_left": self.attempts,
            "max_attempts": self.max_attempts,
            "guessed_letters": sorted(self.guessed),
            "game_over": self.is_game_over(),
            "game_won": self.is_game_won(),
            "actual_word": self.word
        }

    # -- Reset Game -- #
    def reset_game(self):
        self.word = ""
        self.guessed = set()
        self.attempts = self.max_attempts
        self.is_pvp = False

