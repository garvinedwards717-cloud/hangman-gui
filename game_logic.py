# game_logic.py

import random

class HangmanGame:
    def __init__(self, word_list=None, max_wrong_guesses=6):
        """
        Initialize a new Hangman game.

        Parameters:
        - word_list: list of words to choose from
        - max_wrong_guesses: how many wrong guesses allowed before losing
        """
        # Use default words if none are provided
        self.word_list = word_list if word_list else [
            "PYTHON", "HANGMAN", "DEVELOPER", "PYGAME", "COMMIT", "GITHUB"
        ]
        self.max_wrong_guesses = max_wrong_guesses
        self.reset_game()

    def reset_game(self):
        """Reset the game to start a new round."""
        self.secret_word = random.choice(self.word_list).upper()
        self.correct_guesses = set()
        self.wrong_guesses = set()
        self.game_over = False
        self.won = False

    def guess_letter(self, letter):
        """
        Process a guessed letter.
        
        Parameters:
        - letter: a single character string
        """
        letter = letter.upper()
        if self.game_over:
            return

        if letter in self.secret_word:
            self.correct_guesses.add(letter)
        else:
            self.wrong_guesses.add(letter)

        self.check_game_status()

    def check_game_status(self):
        """Check if the game has been won or lost."""
        if all(l in self.correct_guesses for l in self.secret_word):
            self.won = True
            self.game_over = True
        elif len(self.wrong_guesses) >= self.max_wrong_guesses:
            self.won = False
            self.game_over = True

    def get_display_word(self):
        """
        Returns the current display version of the secret word.
        Unguessed letters are shown as underscores.
        """
        return " ".join([l if l in self.correct_guesses else "_" for l in self.secret_word])

    def get_wrong_guesses(self):
        """Return a string of wrong letters guessed so far."""
        return " ".join(sorted(self.wrong_guesses))