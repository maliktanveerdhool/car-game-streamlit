import streamlit as st
import pygame
import numpy as np
from PIL import Image
import io
import random

# Initialize Pygame
pygame.init()

# Set up the game
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
SKY_BLUE = (135, 206, 235)

# Car class
class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        self.color = color
        self.draw_car_icon()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 0
        self.max_speed = 10

    def draw_car_icon(self):
        pygame.draw.rect(self.image, self.color, (0, 10, 40, 40))
        pygame.draw.polygon(self.image, self.color, [(0, 10), (20, 0), (40, 10)])
        pygame.draw.rect(self.image, BLACK, (5, 15, 30, 20))
        pygame.draw.circle(self.image, BLACK, (10, 50), 5)
        pygame.draw.circle(self.image, BLACK, (30, 50), 5)

    def update(self):
        # The car stays in place, but we'll move the road and obstacles
        pass

    def accelerate(self):
        self.speed = min(self.speed + 1, self.max_speed)

    def brake(self):
        self.speed = max(self.speed - 1, 0)

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60), pygame.SRCALPHA)
        self.color = random.choice([RED, YELLOW, GREEN])
        self.draw_car_icon()
        self.rect = self.image.get_rect()
        self.reset()

    def draw_car_icon(self):
        pygame.draw.rect(self.image, self.color, (0, 10, 40, 40))
        pygame.draw.polygon(self.image, self.color, [(0, 10), (20, 0), (40, 10)])
        pygame.draw.rect(self.image, BLACK, (5, 15, 30, 20))
        pygame.draw.circle(self.image, BLACK, (10, 50), 5)
        pygame.draw.circle(self.image, BLACK, (30, 50), 5)

    def update(self, player_speed):
        self.rect.y += player_speed + self.speed
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.x = random.randint(50, WIDTH - 90)
        self.rect.y = random.randint(-200, -100)
        self.speed = random.randint(0, 2)

# Function to render Pygame surface to a Streamlit-compatible image
def pygame_to_streamlit(surface):
    return Image.fromarray(pygame.surfarray.array3d(surface).swapaxes(0, 1))

# Streamlit app
st.set_page_config(page_title="Stylized Car Racing Game", page_icon="🏎️", layout="wide")

st.title("🏎️ Stylized Car Racing Game")

# Game state
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'road_scroll' not in st.session_state:
    st.session_state.road_scroll = 0

# Initialize game objects
if 'game_objects' not in st.session_state:
    st.session_state.game_objects = {
        'screen': pygame.Surface((WIDTH, HEIGHT)),
        'clock': pygame.time.Clock(),
        'player': Car(WIDTH // 2, HEIGHT - 100, BLUE),
        'obstacles': pygame.sprite.Group(),
        'all_sprites': pygame.sprite.Group()
    }
    st.session_state.game_objects['all_sprites'].add(st.session_state.game_objects['player'])
    for _ in range(5):
        obstacle = Obstacle()
        st.session_state.game_objects['obstacles'].add(obstacle)
        st.session_state.game_objects['all_sprites'].add(obstacle)

# Game controls
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    left_button = st.button("⬅️ Left")
with col2:
    right_button = st.button("➡️ Right")
with col3:
    accelerate_button = st.button("🚀 Accelerate")
with col4:
    brake_button = st.button("🛑 Brake")
with col5:
    restart_button = st.button("🔄 Restart")

# Game loop
def game_loop():
    screen = st.session_state.game_objects['screen']
    clock = st.session_state.game_objects['clock']
    player = st.session_state.game_objects['player']
    obstacles = st.session_state.game_objects['obstacles']
    all_sprites = st.session_state.game_objects['all_sprites']

    if left_button:
        player.rect.x -= 5
    if right_button:
        player.rect.x += 5
    if accelerate_button:
        player.accelerate()
    if brake_button:
        player.brake()

    player.rect.clamp_ip(pygame.Rect(50, 0, WIDTH - 100, HEIGHT))

    # Update road scroll
    st.session_state.road_scroll = (st.session_state.road_scroll + player.speed) % 40

    # Update player separately
    player.update()

    # Update obstacles with player speed
    for obstacle in obstacles:
        obstacle.update(player.speed)

    # Check for collisions
    if pygame.sprite.spritecollide(player, obstacles, False):
        st.session_state.game_over = True

    # Drawing
    screen.fill(SKY_BLUE)
    pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))
    pygame.draw.rect(screen, WHITE, (60, 0, 10, HEIGHT))
    pygame.draw.rect(screen, WHITE, (WIDTH - 70, 0, 10, HEIGHT))
    for i in range(-40 + st.session_state.road_scroll, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 5, i, 10, 20))

    all_sprites.draw(screen)

    # Update score
    if not st.session_state.game_over:
        st.session_state.score += player.speed

    # Update high score
    st.session_state.high_score = max(st.session_state.high_score, st.session_state.score)

    # Display score and speed
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {st.session_state.score}", True, WHITE)
    speed_text = font.render(f"Speed: {player.speed}", True, WHITE)
    high_score_text = font.render(f"High Score: {st.session_state.high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(speed_text, (10, 50))
    screen.blit(high_score_text, (10, 90))

    if st.session_state.game_over:
        game_over_text = font.render("Game Over!", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 70, HEIGHT // 2 - 18))

    clock.tick(FPS)
    return pygame_to_streamlit(screen)

# Main game display
game_image = st.empty()

if restart_button or st.session_state.game_over:
    st.session_state.game_over = False
    st.session_state.score = 0
    st.session_state.road_scroll = 0
    st.session_state.game_objects['player'].rect.center = (WIDTH // 2, HEIGHT - 100)
    st.session_state.game_objects['player'].speed = 0
    for obstacle in st.session_state.game_objects['obstacles']:
        obstacle.reset()

game_image.image(game_loop())

# Display score and high score
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"## Score: {st.session_state.score}")
with col2:
    st.markdown(f"## High Score: {st.session_state.high_score}")

# Game instructions
st.markdown("""
## How to Play
1. Use the "Left" and "Right" buttons to move the car.
2. Press "Accelerate" to increase speed and "Brake" to slow down.
3. Avoid the other cars on the road.
4. Try to survive as long as possible to increase your score!
5. Click "Restart" to start a new game.
""")