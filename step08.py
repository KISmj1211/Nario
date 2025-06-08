import pygame
import sys
import random

# Initialize pygame
pygame.init()
pygame.mixer.init()
coin_sound = pygame.mixer.Sound("Mappings/Mario/de_se_potion.ogg")  # fixed path kept

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skeleton Code")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)  # Added missing color

background_colors = [WHITE, LIGHT_BLUE, PINK, ORANGE]

# FPS setup
clock = pygame.time.Clock()
FPS = 60

# Load player image
player_img = pygame.image.load("Mappings/mario/Mario.png")  # fixed path kept
player_img = pygame.transform.scale(player_img, (50, 60))

# Player settings
player_width, player_height = 50, 60
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_x = 5
player_vel_y = 0
jump_power = 15
gravity = 0.8
is_jumping = False
invincible = False
invincible_timer = 0

# Ground setup
ground_y = HEIGHT - 50

# Coin setup
coin_radius = 15
coin_x = 400
coin_y = ground_y - coin_radius
coin_collected = False

# Score and font
score = 0
font = pygame.font.SysFont(None, 40)

# Enemy setup
enemy_width, enemy_height = 50, 50
enemy_x = 600
enemy_y = ground_y - enemy_height
enemy_vel_x = 3
enemy_alive = True

# Stage info
stage = 1
stage_length = 1600
world_shift = 0

# Trap (hole) setup
hole_width = 100
hole_x = random.randint(200, 600)
hole_y = ground_y

# Block (brick) setup
block_width, block_height = 50, 20
block_list = [(300, ground_y - 150), (500, ground_y - 200)]  # block positions
block_hit = [False for _ in block_list]  # whether the block was hit

mushroom_width, mushroom_height = 30, 30
mushroom_x = random.randint(200, stage_length - 200)
mushroom_y = ground_y - mushroom_height
mushroom_collected = False

def draw():
    bg_color = background_colors[(stage - 1) % len(background_colors)]
    screen.fill(bg_color)

    # Ground
    pygame.draw.rect(screen, GREEN, (-world_shift, ground_y, WIDTH, 50))

    # Hole
    pygame.draw.rect(screen, bg_color, (hole_x - world_shift, hole_y, hole_width, 50))

    # Blocks
    for idx, (bx, by) in enumerate(block_list):
        pygame.draw.rect(screen, BROWN, (bx - world_shift, by, block_width, block_height))
        if block_hit[idx]:
            pygame.draw.circle(screen, YELLOW, (bx - world_shift + block_width // 2, by - 20), 10)

    # Coin
    if not coin_collected:
        pygame.draw.circle(screen, YELLOW, (coin_x - world_shift, coin_y), coin_radius)

    if not mushroom_collected:
        pygame.draw.rect(screen, BROWN, (mushroom_x - world_shift, mushroom_y, mushroom_width,mushroom_y))

    screen.blit(player_img, (player_x - world_shift, player_y))
    if enemy_alive:
        pygame.draw.rect(screen, RED, (enemy_x - world_shift, enemy_y,enemy_width, enemy_height))
    # Player and Enemy
    screen.blit(player_img, (player_x, player_y))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_width, enemy_height))

    # Score display
    score_text = font.render(f"Score: {score}  Stage: {stage}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    info = f"Score: {score} Stage: {stage}"
    if invincible:
        info += "INVINCIBLE"
    score_text = font.render(info, True, (0,0,0))
    screen.blit(score_text, (10,10))
    pygame.display.update()

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_vel_x
    if keys[pygame.K_RIGHT]:
        player_x += player_vel_x
    if keys[pygame.K_SPACE]:
        if not is_jumping:
            is_jumping = True
            player_vel_y = -jump_power

    # Gravity
    if is_jumping:
        player_y += player_vel_y
        player_vel_y += gravity

        # Landing
        if player_y >= ground_y - player_height:
            player_y = ground_y - player_height
            is_jumping = False

    # Player collision box
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Stage clear
    if player_x > WIDTH:
        stage += 1
        player_x = 0
        coin_collected = False
        coin_x = random.randint(200, 600)
        enemy_x = random.randint(400, 700)
        enemy_vel_x = 3 + stage
        hole_x = random.randint(200, 600)
        block_list = [(random.randint(100, 700), ground_y - random.randint(100, 200)) for _ in range(2)]
        block_hit = [False for _ in block_list]

    # Coin collision
    if not coin_collected:
        coin_rect = pygame.Rect(coin_x - coin_radius, coin_y - coin_radius, coin_radius * 2, coin_radius * 2)
        if player_rect.colliderect(coin_rect):
            coin_collected = True
            score += 10
            coin_sound.play()

    # Block collision (hit from below)
    for idx, (bx, by) in enumerate(block_list):
        block_rect = pygame.Rect(bx, by, block_width, block_height)
        if (player_rect.centerx in range(bx, bx + block_width)) and (player_y <= by + block_height) and (player_y > by):
            if not block_hit[idx]:
                block_hit[idx] = True
                score += 5

    # Enemy movement
    enemy_x += enemy_vel_x
    if enemy_x <= 0 or enemy_x >= WIDTH - enemy_width:
        enemy_vel_x *= -1

    # Enemy collision
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
    if player_rect.colliderect(enemy_rect):
        print("Game Over! (Hit enemy)")
        pygame.time.delay(1000)
        running = False
    if player_rect.colliderect(enemy_rect):
        if player_y + player_height <=enemy_y +10:
            print("Killed the Enemy by stepping!")
            enemy_x = -1000
            score+=10
            coin_sound.play()
            player_vel_y = -10
        else:
            print("gameover! (hit enemy)")
            pygame.time.delay(1000)
            running = False

    # Hole collision
    if (player_x>=hole_x) and (player_x + player_width <= hole_x + hole_width) and (player_y + player_height >= ground_y):
        print("Game Over! (Fell into hole)")
        pygame.time.delay(1000)
        running = False

    draw()

pygame.quit()
sys.exit()