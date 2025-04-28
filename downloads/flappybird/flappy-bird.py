import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
GRAVITY = 0.5
FLAP_STRENGTH = -5
PIPE_WIDTH = 70
PIPE_HEIGHT = 500
PIPE_GAP = 130
PIPE_SPEED = 4
POWER_UP_DURATION = 5  # Duration of power-up effect in seconds

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load bird image and scale it
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))
bird_rect = bird_img.get_rect()
bird_rect.center = (50, SCREEN_HEIGHT // 2)

# Load background images
day_background_img = pygame.image.load("day_background.png")
day_background_img = pygame.transform.scale(day_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
night_background_img = pygame.image.load("night_background.png")
night_background_img = pygame.transform.scale(night_background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load sound effects
flap_sound = pygame.mixer.Sound("flap.wav")
crash_sound = pygame.mixer.Sound("crash.wav")
background_music = pygame.mixer.music.load("background_music.mp3")

# Function to create pipes
def create_pipe():
    height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 150)
    top_pipe = pygame.Rect(SCREEN_WIDTH, height - PIPE_HEIGHT, PIPE_WIDTH, PIPE_HEIGHT)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, PIPE_HEIGHT)
    return top_pipe, bottom_pipe

# Function to create power-ups
def create_power_up():
    x = random.randint(100, SCREEN_WIDTH - 100)
    y = random.randint(100, SCREEN_HEIGHT - 100)
    power_up = pygame.Rect(x, y, 30, 30)
    return power_up

# Create initial pipes and power-ups
pipes = [create_pipe()]
power_ups = [create_power_up()]

# Game variables
bird_y_velocity = 0
score = 0
high_score = 0
font = pygame.font.Font(None, 36)
game_over = False
power_up_active = False
power_up_start_time = 0

def reset_game():
    global bird_rect, bird_y_velocity, pipes, power_ups, score, game_over, power_up_active, power_up_start_time
    bird_rect.center = (50, SCREEN_HEIGHT // 2)
    bird_y_velocity = 0
    pipes = [create_pipe()]
    power_ups = [create_power_up()]
    score = 0
    game_over = False
    power_up_active = False
    power_up_start_time = 0

# Main game loop
running = True
pygame.mixer.music.play(-1)  # Play background music in a loop
while running:
    # Determine background based on time of day
    current_hour = time.localtime().tm_hour
    if 6 <= current_hour < 18:
        background_img = day_background_img
    else:
        background_img = night_background_img

    screen.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bird_y_velocity = FLAP_STRENGTH
                flap_sound.play()
            if event.key == pygame.K_RETURN and game_over:
                reset_game()

    if not game_over:
        # Bird movement
        bird_y_velocity += GRAVITY
        bird_rect.y += bird_y_velocity

        # Pipe movement and collision detection
        for pipe in pipes:
            pipe[0].x -= PIPE_SPEED
            pipe[1].x -= PIPE_SPEED

            if pipe[0].x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(create_pipe())
                score += 1

            if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                if not power_up_active:
                    game_over = True
                    crash_sound.play()

        # Power-up movement and collision detection
        for power_up in power_ups:
            if bird_rect.colliderect(power_up):
                power_up_active = True
                power_up_start_time = time.time()
                power_ups.remove(power_up)
                power_ups.append(create_power_up())

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe[0])
            pygame.draw.rect(screen, GREEN, pipe[1])

        # Draw power-ups
        for power_up in power_ups:
            pygame.draw.rect(screen, RED, power_up)

        # Draw bird
        screen.blit(bird_img, bird_rect)

        # Check if bird is out of bounds
        if bird_rect.top < 0 or bird_rect.bottom > SCREEN_HEIGHT:
            game_over = True
            crash_sound.play()

        # Check if power-up effect has expired
        if power_up_active and time.time() - power_up_start_time > POWER_UP_DURATION:
            power_up_active = False

    else:
        # Update high score if necessary
        if score > high_score:
            high_score = score

        # Display game over message and instructions to restart
        game_over_text = font.render("Game Over! Press Enter to Restart", True, RED)
        screen.blit(game_over_text, (20, SCREEN_HEIGHT // 2 - 20))

    # Draw score and high score
    score_text = font.render(f"Score: {score}", True, BLACK)
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

    # Update display and tick clock
    pygame.display.update()
    pygame.time.Clock().tick(30)

# Quit Pygame
pygame.quit()