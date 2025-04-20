import pygame
import sys

# pygame init
pygame.init()

# Display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skeleton Code")

# Color
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# FPS
clock = pygame.time.Clock()
FPS = 60

# player
player_width, player_height = 50, 60
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_x = 5
player_vel_y = 0
jump_power = 15
gravity = 0.8
is_jumping = False

# floor
ground_y = HEIGHT - 50


# game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()