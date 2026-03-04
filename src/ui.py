import pygame

# -----------------------
# CONSTANTS
# -----------------------
BG_COLOR = (30, 30, 30)        # Background color
LINE_COLOR = (255, 255, 255)   # Text & line color
WIN_COLOR = (0, 200, 0)        # Win text color
LOSE_COLOR = (200, 0, 0)       # Lose text color
BODY_COLOR = (255, 100, 100)   # Wrong guesses text
FONT_NAME = "Arial"

# -----------------------
# DRAW FUNCTIONS
# -----------------------
def draw_game_screen(screen, game, font):
    """
    Draw the main game screen: gallows, hangman, word, wrong letters.
    """
    screen.fill(BG_COLOR)

    # Draw gallows and hangman
    draw_gallows(screen)
    draw_hangman(screen, len(game.wrong_guesses))

    # Display the word with underscores
    word_surface = font.render(game.get_display_word(), True, LINE_COLOR)
    screen.blit(word_surface, (50, 100))

    # Display wrong letters
    wrong_surface = font.render(f"Wrong: {game.get_wrong_guesses()}", True, BODY_COLOR)
    screen.blit(wrong_surface, (50, 200))

    pygame.display.flip()

def draw_win_screen(screen, width, height):
    """
    Draw the win screen with restart instructions.
    """
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont(FONT_NAME, 64)
    small_font = pygame.font.SysFont(FONT_NAME, 32)

    text = font.render("You Won!", True, WIN_COLOR)
    restart = small_font.render("Press ENTER to restart", True, LINE_COLOR)

    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 40))
    screen.blit(restart, (width // 2 - restart.get_width() // 2, height // 2 + 30))

    pygame.display.flip()

def draw_lose_screen(screen, width, height, secret_word):
    """
    Draw the lose screen showing the correct word and restart instructions.
    """
    screen.fill(BG_COLOR)
    font = pygame.font.SysFont(FONT_NAME, 64)
    small_font = pygame.font.SysFont(FONT_NAME, 32)

    text = font.render("You Lost!", True, LOSE_COLOR)
    word_text = small_font.render(f"The word was: {secret_word}", True, LINE_COLOR)
    restart = small_font.render("Press ENTER to restart", True, LINE_COLOR)

    screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - 60))
    screen.blit(word_text, (width // 2 - word_text.get_width() // 2, height // 2))
    screen.blit(restart, (width // 2 - restart.get_width() // 2, height // 2 + 40))

    pygame.display.flip()

# -----------------------
# HANGMAN DRAWING
# -----------------------
def draw_gallows(screen):
    """
    Draw the static gallows structure.
    """
    # Base
    pygame.draw.line(screen, LINE_COLOR, (50, 500), (250, 500), 5)
    # Vertical pole
    pygame.draw.line(screen, LINE_COLOR, (150, 500), (150, 100), 5)
    # Top beam
    pygame.draw.line(screen, LINE_COLOR, (150, 100), (350, 100), 5)
    # Rope
    pygame.draw.line(screen, LINE_COLOR, (350, 100), (350, 150), 5)

def draw_hangman(screen, wrong_count):
    """
    Draw the hangman step by step based on wrong guesses.
    """
    # Head
    if wrong_count > 0:
        pygame.draw.circle(screen, LINE_COLOR, (350, 200), 30, 3)
    # Body
    if wrong_count > 1:
        pygame.draw.line(screen, LINE_COLOR, (350, 230), (350, 350), 3)
    # Left arm
    if wrong_count > 2:
        pygame.draw.line(screen, LINE_COLOR, (350, 250), (300, 300), 3)
    # Right arm
    if wrong_count > 3:
        pygame.draw.line(screen, LINE_COLOR, (350, 250), (400, 300), 3)
    # Left leg
    if wrong_count > 4:
        pygame.draw.line(screen, LINE_COLOR, (350, 350), (300, 420), 3)
    # Right leg
    if wrong_count > 5:
        pygame.draw.line(screen, LINE_COLOR, (350, 350), (400, 420), 3)