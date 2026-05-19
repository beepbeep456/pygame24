import pygame
import sys
import os
import math
import random

# -------------------------
# 초기화
# -------------------------
pygame.init()

# -------------------------
# 화면 크기
# -------------------------
WIDTH = 480
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("탄막 슈팅")

clock = pygame.time.Clock()

# -------------------------
# 상대경로 설정
# -------------------------
BASE_DIR = os.path.dirname(__file__)

# -------------------------
# 배경 이미지
# -------------------------
bg_path = os.path.join(BASE_DIR, "레벨 999 배경-Sheet.png")

bg = pygame.image.load(bg_path).convert()

BG_SCALE = 1.15

bg_width = int(WIDTH * BG_SCALE)
bg_height = int(HEIGHT * BG_SCALE)

bg = pygame.transform.scale(bg, (bg_width, bg_height))

bg_x = -(bg_width - WIDTH) // 2

# -------------------------
# 플레이어 이미지
# -------------------------
player_path = os.path.join(BASE_DIR, "999.png")

player_img = pygame.image.load(player_path).convert_alpha()

player_width = 60
player_height = 60

player_img = pygame.transform.scale(
    player_img,
    (player_width, player_height)
)

player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120

player_speed = 8

# -------------------------
# 플레이어 탄 이미지
# -------------------------
bullet_path = os.path.join(BASE_DIR, "기기괴괴콩.png")

bullet_img = pygame.image.load(bullet_path).convert_alpha()

bullet_width = 40
bullet_height = 40

bullet_img = pygame.transform.scale(
    bullet_img,
    (bullet_width, bullet_height)
)

bullets = []

bullet_speed = 15

shoot_delay = 120

last_shot = 0

# -------------------------
# 적 탄 이미지
# -------------------------
enemy_bullet_path = os.path.join(BASE_DIR, "탄막1.png")

enemy_bullet_img = pygame.image.load(enemy_bullet_path).convert_alpha()

enemy_bullet_size = 40

enemy_bullet_img = pygame.transform.scale(
    enemy_bullet_img,
    (enemy_bullet_size, enemy_bullet_size)
)

enemy_bullets = []

# =========================================================
# 1웨이브 적
# =========================================================

enemy_path = os.path.join(BASE_DIR, "곤충2.png")

enemy_img = pygame.image.load(enemy_path).convert_alpha()

enemy_width = 80
enemy_height = 80

enemy_img = pygame.transform.scale(
    enemy_img,
    (enemy_width, enemy_height)
)

enemies = []

enemy_count = 6

start_x = 40
gap = 65

target_y = random.randint(80, 220)

for i in range(enemy_count):

    enemy = {
        "x": start_x + i * gap,
        "y": -100 - i * 40,
        "target_y": target_y,
        "speed": 4,
        "stopped": False,
        "alive": True
    }

    enemies.append(enemy)

enemy_shoot_delay = 1300

last_enemy_shot = 0

# =========================================================
# 2웨이브 적
# =========================================================

enemy2_path = os.path.join(BASE_DIR, "enemy2.png")

enemy2_img = pygame.image.load(enemy2_path).convert_alpha()

enemy2_width = 70
enemy2_height = 70

enemy2_img = pygame.transform.scale(
    enemy2_img,
    (enemy2_width, enemy2_height)
)

enemies2 = []

enemy2_count = 6

start_x2 = 30
gap2 = 70

target_y2 = random.randint(120, 260)

for i in range(enemy2_count):

    enemy = {

        "x": start_x2 + i * gap2,
        "y": -400 - i * 60,

        "target_y": target_y2,

        "speed": 5,

        "stopped": False,

        "alive": True,

        "enter_shot": False,

        "last_shot": 0
    }

    enemies2.append(enemy)

# -------------------------
# 웨이브 상태
# -------------------------
wave2_started = False

# -------------------------
# 배경 위치
# -------------------------
bg_y1 = 0
bg_y2 = -bg_height

bg_speed = 10

# =========================================================
# 게임 루프
# =========================================================
while True:

    current_time = pygame.time.get_ticks()

    # -------------------------
    # 종료 처리
    # -------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -------------------------
    # 키 입력
    # -------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if keys[pygame.K_UP]:
        player_y -= player_speed

    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # -------------------------
    # 화면 제한
    # -------------------------
    if player_x < 0:
        player_x = 0

    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width

    if player_y < 0:
        player_y = 0

    if player_y > HEIGHT - player_height:
        player_y = HEIGHT - player_height

    # =========================================================
    # 자동 발사
    # =========================================================
    if current_time - last_shot > shoot_delay:

        bullet_x = player_x + player_width // 2 - bullet_width // 2
        bullet_y = player_y

        bullets.append([bullet_x, bullet_y])

        last_shot = current_time

    # =========================================================
    # 1웨이브 적 이동
    # =========================================================
    for enemy in enemies:

        if enemy["alive"]:

            if not enemy["stopped"]:

                enemy["y"] += enemy["speed"]

                if enemy["y"] >= enemy["target_y"]:

                    enemy["y"] = enemy["target_y"]
                    enemy["stopped"] = True

    # =========================================================
    # 1웨이브 원형 탄막
    # =========================================================
    if current_time - last_enemy_shot > enemy_shoot_delay:

        for enemy in enemies:

            if enemy["alive"] and enemy["stopped"]:

                bullet_count = 24

                for i in range(bullet_count):

                    angle = (360 / bullet_count) * i

                    rad = math.radians(angle)

                    speed = 4

                    dx = math.cos(rad) * speed
                    dy = math.sin(rad) * speed

                    enemy_bullets.append([
                        enemy["x"] + enemy_width // 2,
                        enemy["y"] + enemy_height // 2,
                        dx,
                        dy
                    ])

        last_enemy_shot = current_time

    # =========================================================
    # 1웨이브 종료 체크
    # =========================================================
    all_dead = True

    for enemy in enemies:

        if enemy["alive"]:
            all_dead = False
            break

    if all_dead:
        wave2_started = True

    # =========================================================
    # 2웨이브 적 이동
    # =========================================================
    if wave2_started:

        for i, enemy in enumerate(enemies2):

            if enemy["alive"]:

                # 좌우 랜덤 이동
                move_x = random.randint(-3, 3)

                next_x = enemy["x"] + move_x

                if next_x < 0:
                    next_x = 0

                if next_x > WIDTH - enemy2_width:
                    next_x = WIDTH - enemy2_width

                # 겹침 방지
                can_move = True

                next_rect = pygame.Rect(
                    next_x,
                    enemy["y"],
                    enemy2_width,
                    enemy2_height
                )

                for j, other in enumerate(enemies2):

                    if i != j and other["alive"]:

                        other_rect = pygame.Rect(
                            other["x"],
                            other["y"],
                            enemy2_width,
                            enemy2_height
                        )

                        if next_rect.colliderect(other_rect):
                            can_move = False
                            break

                if can_move:
                    enemy["x"] = next_x

                # 아래 이동
                if not enemy["stopped"]:

                    enemy["y"] += enemy["speed"]

                    # 등장 중 탄 발사
                    if not enemy["enter_shot"] and enemy["y"] > 0:

                        dx = player_x - enemy["x"]
                        dy = player_y - enemy["y"]

                        dist = math.sqrt(dx * dx + dy * dy)

                        if dist != 0:

                            dx /= dist
                            dy /= dist

                            speed = 6

                            enemy_bullets.append([
                                enemy["x"] + 15,
                                enemy["y"] + enemy2_height // 2,
                                dx * speed,
                                dy * speed
                            ])

                            enemy_bullets.append([
                                enemy["x"] + enemy2_width - 15,
                                enemy["y"] + enemy2_height // 2,
                                dx * speed,
                                dy * speed
                            ])

                        enemy["enter_shot"] = True

                    # 정지
                    if enemy["y"] >= enemy["target_y"]:

                        enemy["y"] = enemy["target_y"]

                        enemy["stopped"] = True

    # =========================================================
    # 2웨이브 플레이어 조준 탄막
    # =========================================================
    if wave2_started:

        for enemy in enemies2:

            if enemy["alive"] and enemy["stopped"]:

                if current_time - enemy["last_shot"] > 1200:

                    dx = player_x - enemy["x"]
                    dy = player_y - enemy["y"]

                    dist = math.sqrt(dx * dx + dy * dy)

                    if dist != 0:

                        dx /= dist
                        dy /= dist

                        speed = 7

                        enemy_bullets.append([
                            enemy["x"] + 15,
                            enemy["y"] + enemy2_height // 2,
                            dx * speed,
                            dy * speed
                        ])

                        enemy_bullets.append([
                            enemy["x"] + enemy2_width - 15,
                            enemy["y"] + enemy2_height // 2,
                            dx * speed,
                            dy * speed
                        ])

                    enemy["last_shot"] = current_time

    # =========================================================
    # 플레이어 탄 이동
    # =========================================================
    for bullet in bullets:
        bullet[1] -= bullet_speed

    bullets = [b for b in bullets if b[1] > -bullet_height]

    # =========================================================
    # 적 탄 이동
    # =========================================================
    for bullet in enemy_bullets:

        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    enemy_bullets = [
        b for b in enemy_bullets
        if -50 < b[0] < WIDTH + 50
        and -50 < b[1] < HEIGHT + 50
    ]

    # =========================================================
    # 플레이어 탄 vs 1웨이브 적 충돌
    # =========================================================
    for enemy in enemies:

        if enemy["alive"]:

            enemy_rect = pygame.Rect(
                enemy["x"],
                enemy["y"],
                enemy_width,
                enemy_height
            )

            for bullet in bullets[:]:

                bullet_rect = pygame.Rect(
                    bullet[0],
                    bullet[1],
                    bullet_width,
                    bullet_height
                )

                if enemy_rect.colliderect(bullet_rect):

                    enemy["alive"] = False

                    if bullet in bullets:
                        bullets.remove(bullet)

                    break

    # =========================================================
    # 플레이어 탄 vs 2웨이브 적 충돌
    # =========================================================
    for enemy in enemies2:

        if enemy["alive"]:

            enemy_rect = pygame.Rect(
                enemy["x"],
                enemy["y"],
                enemy2_width,
                enemy2_height
            )

            for bullet in bullets[:]:

                bullet_rect = pygame.Rect(
                    bullet[0],
                    bullet[1],
                    bullet_width,
                    bullet_height
                )

                if enemy_rect.colliderect(bullet_rect):

                    enemy["alive"] = False

                    if bullet in bullets:
                        bullets.remove(bullet)

                    break

    # =========================================================
    # 배경 스크롤
    # =========================================================
    bg_y1 += bg_speed
    bg_y2 += bg_speed

    if bg_y1 >= bg_height:
        bg_y1 = bg_y2 - bg_height

    if bg_y2 >= bg_height:
        bg_y2 = bg_y1 - bg_height

    # =========================================================
    # 그리기
    # =========================================================
    screen.blit(bg, (bg_x, bg_y1))
    screen.blit(bg, (bg_x, bg_y2))

    # 플레이어 탄
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    # 적 탄
    for bullet in enemy_bullets:
        screen.blit(enemy_bullet_img, (bullet[0], bullet[1]))

    # 1웨이브 적
    for enemy in enemies:

        if enemy["alive"]:
            screen.blit(enemy_img, (enemy["x"], enemy["y"]))

    # 2웨이브 적
    if wave2_started:

        for enemy in enemies2:

            if enemy["alive"]:
                screen.blit(enemy2_img, (enemy["x"], enemy["y"]))

    # 플레이어
    screen.blit(player_img, (player_x, player_y))

    pygame.display.update()

    clock.tick(60)