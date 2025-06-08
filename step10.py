import pygame
import sys
import random

# 초기화
pygame.init()
pygame.mixer.init()
coin_sound = pygame.mixer.Sound("mario/sound/de_se_potion.ogg")

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("슈퍼 마리오 버섯")

# 색깔
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)

background_colors = [WHITE, LIGHT_BLUE, PINK, ORANGE]

# FPS 설정
clock = pygame.time.Clock()
FPS = 60

# 이미지 로드
player_img_raw = pygame.image.load("mario/mario.png")
player_width, player_height = 50, 60
player_img = pygame.transform.scale(player_img_raw, (player_width, player_height))

# 플레이어 설정
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel_x = 5
player_vel_y = 0
jump_power = 15
gravity = 0.8
is_jumping = False
invincible = False
invincible_timer = 0

# 바닥 설정
ground_y = HEIGHT - 50

# 코인 설정
coin_radius = 15
coin_x = 400
coin_y = ground_y - coin_radius
coin_collected = False

# 점수
score = 0
font = pygame.font.SysFont(None, 40)

# 적 설정
enemy_width, enemy_height = 50, 50
enemy_x = 600
enemy_y = ground_y - enemy_height
enemy_vel_x = 3
enemy_alive = True

# 스테이지
stage = 1
stage_length = 1600
world_shift = 0

# 함정 설정
hole_width = 100
hole_x = random.randint(200, 1500)
hole_y = ground_y

# 점프 블록 설정
block_width, block_height = 50, 20
block_list = [(300, ground_y - 150), (800, ground_y - 200)]
block_hit = [False for _ in block_list]

# 버섯 설정
mushroom_width, mushroom_height = 30, 30
mushroom_x = random.randint(200, stage_length - 200)
mushroom_y = ground_y - mushroom_height
mushroom_collected = False

# 그리기 함수
def draw():
    bg_color = background_colors[(stage - 1) % len(background_colors)]
    screen.fill(bg_color)
    pygame.draw.rect(screen, GREEN, (-world_shift, ground_y, stage_length, 50))
    pygame.draw.rect(screen, bg_color, (hole_x - world_shift, hole_y, hole_width, 50))

    for idx, (bx, by) in enumerate(block_list):
        pygame.draw.rect(screen, BROWN, (bx - world_shift, by, block_width, block_height))
        if block_hit[idx]:
            pygame.draw.circle(screen, YELLOW, (bx - world_shift + block_width // 2, by - 20), 10)

    if not coin_collected:
        pygame.draw.circle(screen, YELLOW, (coin_x - world_shift, coin_y), coin_radius)

    if not mushroom_collected:
        pygame.draw.rect(screen, BROWN, (mushroom_x - world_shift, mushroom_y, mushroom_width, mushroom_height))

    screen.blit(player_img, (player_x - world_shift, player_y))
    if enemy_alive:
        pygame.draw.rect(screen, RED, (enemy_x - world_shift, enemy_y, enemy_width, enemy_height))

    info = f"Score: {score}  Stage: {stage}"
    if invincible:
        info += "  INVINCIBLE"
    score_text = font.render(info, True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.update()

# 게임 루프
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_vel_x
    if keys[pygame.K_RIGHT]:
        player_x += player_vel_x
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        player_vel_y = -jump_power

    player_y += player_vel_y
    player_vel_y += gravity

    if player_y >= ground_y - player_height:
        player_y = ground_y - player_height
        player_vel_y = 0
        is_jumping = False

    for bx, by in block_list:
        if (
            player_y + player_height <= by + 5 and
            player_y + player_height + player_vel_y >= by and
            player_x + player_width > bx and
            player_x < bx + block_width
        ):
            player_y = by - player_height
            player_vel_y = 0
            is_jumping = False

    if player_x - world_shift > WIDTH // 2:
        world_shift = player_x - WIDTH // 2

    if invincible:
        invincible_timer -= 1
        if invincible_timer <= 0:
            invincible = False

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    if player_x > stage_length:
        stage += 1
        player_x = 0
        world_shift = 0
        coin_collected = False
        mushroom_collected = False
        invincible = False
        enemy_alive = True
        player_height = 60
        player_img = pygame.transform.scale(player_img_raw, (player_width, player_height))
        coin_x = random.randint(200, stage_length - 200)
        mushroom_x = random.randint(200, stage_length - 200)
        enemy_x = random.randint(400, stage_length - 100)
        enemy_vel_x = 3 + stage
        hole_x = random.randint(200, stage_length - 200)
        block_list = [(random.randint(100, stage_length - 100), ground_y - random.randint(100, 200)) for _ in range(2)]
        block_hit = [False for _ in block_list]

    if not coin_collected:
        coin_rect = pygame.Rect(coin_x, coin_y, coin_radius * 2, coin_radius * 2)
        if player_rect.colliderect(coin_rect):
            coin_collected = True
            score += 10
            coin_sound.play()

    if not mushroom_collected:
        mushroom_rect = pygame.Rect(mushroom_x, mushroom_y, mushroom_width, mushroom_height)
        if player_rect.colliderect(mushroom_rect):
            mushroom_collected = True
            invincible = True
            invincible_timer = FPS * 5
            player_height = 90
            player_img = pygame.transform.scale(player_img_raw, (player_width, player_height))

    for idx, (bx, by) in enumerate(block_list):
        if (player_rect.centerx in range(bx, bx + block_width)) and (player_y <= by + block_height) and (player_y > by):
            if not block_hit[idx]:
                block_hit[idx] = True
                score += 5

    if enemy_alive:
        enemy_x += enemy_vel_x
        if enemy_x <= 0 or enemy_x >= stage_length - enemy_width:
            enemy_vel_x *= -1

        enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        if player_rect.colliderect(enemy_rect):
            if player_y + player_height <= enemy_y + 10:
                enemy_alive = False
                score += 20
            elif invincible:
                if player_height > 60:
                    player_height = 60
                    player_img = pygame.transform.scale(player_img_raw, (player_width, player_height))
                    invincible = False
                    invincible_timer = FPS * 2
                else:
                    pass
            else:
                if player_height > 60:
                    player_height = 60
                    player_img = pygame.transform.scale(player_img_raw, (player_width, player_height))
                    invincible = True
                    invincible_timer = FPS * 2
                else:
                    pygame.time.delay(1000)
                    running = False

    player_left = player_x
    player_right = player_x + player_width

    if player_left >= hole_x and player_right <= hole_x + hole_width and player_y + player_height >= ground_y:
        if invincible:
            invincible = False
            player_height = 60
            player_img = pygame.transform.scale(player_img_raw, (player_width, player_height))
            player_x = hole_x + hole_width + 5
        else:
            pygame.time.delay(1000)
            running = False

    draw()

pygame.quit()
sys.exit()