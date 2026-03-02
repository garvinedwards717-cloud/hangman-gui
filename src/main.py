import random
import pygame
import sys
import os

# -------------------------
# INIT
# -------------------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TestGame")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 80)

BASE_DIR = os.path.dirname(__file__)
SOUNDS_DIR = os.path.join(BASE_DIR, '..', 'assets', "sounds")

# -------------------------
# LOAD SOUNDS
# -------------------------
def load_sound(path):
    if os.path.exists(path):
        return pygame.mixer.Sound(path)
    return None

background_music = os.path.join(SOUNDS_DIR, "background.mp3")
correct_sound = load_sound(os.path.join(SOUNDS_DIR, "correct.wav"))
wrong_sound = load_sound(os.path.join(SOUNDS_DIR, "wrong.wav"))
win_sound = load_sound(os.path.join(SOUNDS_DIR, "win.wav"))
lose_sound = load_sound(os.path.join(SOUNDS_DIR, "lose.wav"))

if os.path.exists(background_music):
    pygame.mixer.music.load(background_music)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

# -------------------------
# WORD LIST
# -------------------------
words = ["python", "developer", "hangman", "keyboard", "computer"]

# -------------------------
# GAME VARIABLES
# -------------------------
def reset_game():
    global chosen_word, guessed_letters, lives, max_lives
    global game_state, shake_timer, fall_offset, is_falling
    global win_sound_played, lose_sound_played

    chosen_word = random.choice(words)
    guessed_letters = []
    lives = 6
    max_lives = 6

    shake_timer = 0
    fall_offset = 0
    is_falling = False

    game_state = "playing"
    win_sound_played = False
    lose_sound_played = False

reset_game()
score = 0

# -------------------------
# FUNCTIONS
# -------------------------
def get_display_word():
    return " ".join([l if l in guessed_letters else "_" for l in chosen_word])

def draw_gallows():
    pygame.draw.line(screen, (255,255,255), (100,500), (300,500), 5)
    pygame.draw.line(screen, (255,255,255), (200,500), (200,150), 5)
    pygame.draw.line(screen, (255,255,255), (200,150), (350,150), 5)
    pygame.draw.line(screen, (255,255,255), (350,150), (350,200), 5)

def draw_hangman():
    global shake_timer, fall_offset, is_falling

    mistakes = max_lives - lives

    # COLOR CHANGE
    body_color = (255 - mistakes*30, 80, 80)

    # SHAKE
    shake_x = 0
    if shake_timer > 0:
        shake_x = random.randint(-5, 5)
        shake_timer -= 1

    # FALL
    if lives <= 0:
        is_falling = True

    if is_falling and fall_offset < 200:
        fall_offset += 4

    x = 350 + shake_x
    y = fall_offset

    if mistakes >= 1:
        pygame.draw.circle(screen, body_color, (x, 240 + y), 40, 3)
    if mistakes >= 2:
        pygame.draw.line(screen, body_color, (x, 280 + y), (x, 380 + y), 3)
    if mistakes >= 3:
        pygame.draw.line(screen, body_color, (x, 300 + y), (x-40, 340 + y), 3)
    if mistakes >= 4:
        pygame.draw.line(screen, body_color, (x, 300 + y), (x+40, 340 + y), 3)
    if mistakes >= 5:
        pygame.draw.line(screen, body_color, (x, 380 + y), (x-40, 440 + y), 3)
    if mistakes >= 6:
        pygame.draw.line(screen, body_color, (x, 380 + y), (x+40, 440 + y), 3)

def draw_lose_eyes():
    # Red X eyes
    pygame.draw.line(screen, (255,0,0), (330,220+fall_offset), (350,240+fall_offset), 3)
    pygame.draw.line(screen, (255,0,0), (350,220+fall_offset), (330,240+fall_offset), 3)
    pygame.draw.line(screen, (255,0,0), (370,220+fall_offset), (390,240+fall_offset), 3)
    pygame.draw.line(screen, (255,0,0), (390,220+fall_offset), (370,240+fall_offset), 3)

def draw_center(text, font_obj, color, y_offset=0):
    surface = font_obj.render(text, True, color)
    screen.blit(surface, (WIDTH//2 - surface.get_width()//2,
                          HEIGHT//2 - surface.get_height()//2 + y_offset))

# -------------------------
# MAIN LOOP
# -------------------------
running = True
while running:

    clock.tick(60)
    screen.fill((30, 30, 60))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                running = False

            if game_state == "playing":

                if event.unicode.isalpha():
                    letter = event.unicode.lower()

                    if letter not in guessed_letters:
                        guessed_letters.append(letter)

                        if letter in chosen_word:
                            score += 10
                            if correct_sound:
                                correct_sound.play()
                        else:
                            lives -= 1
                            score -= 5
                            shake_timer = 15
                            if wrong_sound:
                                wrong_sound.play()

            elif game_state in ["win", "lose"]:
                if event.key == pygame.K_r:
                    reset_game()

    # -------------------------
    # PLAYING STATE
    # -------------------------
    if game_state == "playing":

        draw_gallows()
        draw_hangman()

        word_surface = font.render(get_display_word(), True, (255,255,255))
        screen.blit(word_surface, (WIDTH//2 - word_surface.get_width()//2, 500))

        screen.blit(small_font.render(f"Lives: {lives}", True, (255,100,100)), (20,20))
        screen.blit(small_font.render(f"Score: {score}", True, (255,255,255)), (WIDTH-150,20))

        if all(l in guessed_letters for l in chosen_word):
            game_state = "win"
            score += 50

        if lives <= 0:
            game_state = "lose"
            score -= 20

    # -------------------------
    # WIN SCREEN
    # -------------------------
    elif game_state == "win":

        if not win_sound_played:
            if win_sound:
                win_sound.play()
            win_sound_played = True

        screen.fill((20, 80, 20))

        draw_center("🎉 YOU WIN! 🎉", big_font, (0,255,0), -80)
        draw_center(f"Word: {chosen_word}", font, (255,255,255), 0)
        draw_center(f"Score: {score}", small_font, (255,255,255), 60)
        draw_center("Press R to Restart", small_font, (200,200,200), 120)
        draw_center("Press ESC to Quit", small_font, (200,200,200), 160)

    # -------------------------
    # LOSE SCREEN
    # -------------------------
    elif game_state == "lose":

        if not lose_sound_played:
            if lose_sound:
                lose_sound.play()
            lose_sound_played = True

        screen.fill((80, 20, 20))

        draw_gallows()
        draw_hangman()
        draw_lose_eyes()

        draw_center("💀 YOU LOST 💀", big_font, (255,0,0), -200)
        draw_center(f"Word was: {chosen_word}", font, (255,255,255), -130)
        draw_center(f"Score: {score}", small_font, (255,255,255), -90)
        draw_center("Press R to Restart", small_font, (200,200,200), -40)
        draw_center("Press ESC to Quit", small_font, (200,200,200), 0)

    pygame.display.flip()

pygame.quit()
sys.exit()