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
GREEN = (0, 255, 0)
YELLOW = (255,255,0)

# FPS
clock = pygame.time.Clock()
FPS = 60

player_img = pygame.image.load("Mappings/mario/Mario.png")
player_img = pygame.transform.scale(player_img,(50,60))

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
coin_radius = 15
coin_x = 400
coin_y = ground_y - coin_radius
coin_collected = False
def draw():
    screen.fill(WHITE)
    pygame.draw.rect(screen, GREEN, (0,ground_y,WIDTH,50))
    if not coin_collected:
        pygame.draw.circle(screen,YELLOW, (coin_x, coin_y), coin_radius)
    screen.blit(player_img, (player_x, player_y))
    pygame.display.update()

# game loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -=player_vel_x
    if keys[pygame.K_RIGHT]:
        player_x += player_vel_x
    if keys [pygame.K_SPACE]:
        if not is_jumping:
            is_jumping = True
            player_vel_y = -jump_power
    if is_jumping:
        player_y +=player_vel_y
        player_vel_y+=gravity

        if player_y >=ground_y-player_height:
            player_y = ground_y - player_height
            is_jumping=False
    if not coin_collected:
        player_rect = pygame.Rect(player_x,player_y, player_width,player_height)
        coin_rect = pygame.Rect(coin_x-coin_radius,coin_y - coin_radius, coin_radius*2,coin_radius*2)
        if player_rect.colliderect(coin_rect):
            coin_collected = True
            score +=10

    draw()
pygame.quit()
sys.exit()