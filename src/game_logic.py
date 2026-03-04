import random

class HangmanGame:
    def __init__(self):
        self.words = ["PYTHON", "HANGMAN", "DEVELOPER", "CODE", "PROGRAM"]
        self.reset_game()

    def reset_game(self):
        """Initialize a new game."""
        self.secret_word = random.choice(self.words).upper()
        self.guessed_letters = set()
        self.wrong_guesses = set()
        self.max_wrong = 6
        self.game_over = False
        self.won = False

    def guess_letter(self, letter):
        """Process a guessed letter."""
        letter = letter.upper()
        if self.game_over or not letter.isalpha() or len(letter) != 1:
            return

        if letter in self.secret_word:
            self.guessed_letters.add(letter)
        else:
            self.wrong_guesses.add(letter)

        self.check_game_over()

    def check_game_over(self):
        """Check if player won or lost."""
        if all(l in self.guessed_letters for l in self.secret_word):
            self.game_over = True
            self.won = True
        elif len(self.wrong_guesses) >= self.max_wrong:
            self.game_over = True
            self.won = False

    def get_display_word(self):
        """Return the secret word with underscores for unguessed letters."""
        return " ".join([l if l in self.guessed_letters else "_" for l in self.secret_word])

    def get_wrong_guesses(self):
        """Return wrong guesses as a string."""
        return ", ".join(sorted(self.wrong_guesses))