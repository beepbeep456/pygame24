import pygame
import sys
import os
import math
import random

# =========================================================
# 초기화
# =========================================================
pygame.init()

WIDTH = 480
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("탄막 슈팅")

clock = pygame.time.Clock()

BASE_DIR = os.path.dirname(__file__)

# =========================================================
# 배경
# =========================================================
bg_path = os.path.join(BASE_DIR, "레벨 999 배경-Sheet.png")

bg = pygame.image.load(bg_path).convert()

BG_SCALE = 1.15

bg_width = int(WIDTH * BG_SCALE)
bg_height = int(HEIGHT * BG_SCALE)

bg = pygame.transform.scale(
    bg,
    (bg_width, bg_height)
)

bg_x = -(bg_width - WIDTH) // 2

bg_y1 = 0
bg_y2 = -bg_height

bg_speed = 10

# =========================================================
# 플레이어
# =========================================================
player_path = os.path.join(BASE_DIR, "999.png")

player_img = pygame.image.load(
    player_path
).convert_alpha()

player_width = 60
player_height = 60

player_img = pygame.transform.scale(
    player_img,
    (player_width, player_height)
)

player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 120

player_speed = 8

# =========================================================
# 플레이어 탄
# =========================================================
bullet_path = os.path.join(BASE_DIR, "기기괴괴콩.png")

bullet_img = pygame.image.load(
    bullet_path
).convert_alpha()

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

# =========================================================
# 적 탄
# =========================================================
enemy_bullet_path = os.path.join(BASE_DIR, "탄막1.png")

enemy_bullet_img = pygame.image.load(
    enemy_bullet_path
).convert_alpha()

enemy_bullet_size = 40

enemy_bullet_img = pygame.transform.scale(
    enemy_bullet_img,
    (enemy_bullet_size, enemy_bullet_size)
)

enemy_bullets = []

# =========================================================
# 보스 탄
# =========================================================
boss_bullet_path = os.path.join(
    BASE_DIR,
    "탄막2.png"
)

boss_bullet_img = pygame.image.load(
    boss_bullet_path
).convert_alpha()

boss_bullet_size = 50

boss_bullet_img = pygame.transform.scale(
    boss_bullet_img,
    (boss_bullet_size, boss_bullet_size)
)

boss_bullets = []

# =========================================================
# 폭발
# =========================================================
explosions = []

def create_explosion(x, y):

    for i in range(20):

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(2, 7)

        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed

        particle = {
            "x": x,
            "y": y,
            "dx": dx,
            "dy": dy,
            "life": random.randint(20, 40),
            "size": random.randint(4, 10)
        }

        explosions.append(particle)

# =========================================================
# 적 이미지
# =========================================================
enemy1_img = pygame.image.load(
    os.path.join(BASE_DIR, "곤충2.png")
).convert_alpha()

enemy1_img = pygame.transform.scale(
    enemy1_img,
    (80, 80)
)

enemy2_img = pygame.image.load(
    os.path.join(BASE_DIR, "enemy2.png")
).convert_alpha()

enemy2_img = pygame.transform.scale(
    enemy2_img,
    (70, 70)
)

# =========================================================
# 보스 이미지
# =========================================================
boss_path = os.path.join(
    BASE_DIR,
    "스카라카바즈.png"
)

boss_img = pygame.image.load(
    boss_path
).convert_alpha()

boss_width = 180
boss_height = 180

boss_img = pygame.transform.scale(
    boss_img,
    (boss_width, boss_height)
)

boss = {
    "x": WIDTH // 2 - boss_width // 2,
    "y": -200,
    "target_y": 80,
    "speed": 3,
    "alive": False,
    "hp": 500,
    "phase": 1,
    "phase_timer": 0,
    "last_shot": 0,
    "rotation": 0
}

game_clear = False

# =========================================================
# 웨이브
# =========================================================
current_wave = 1

wave1 = []
wave2 = []
wave3 = []
wave4 = []
wave5 = []

# =========================================================
# Wave1
# =========================================================
for i in range(6):

    enemy = {
        "x": 40 + i * 65,
        "y": -100 - i * 50,
        "target_y": 150,
        "speed": 4,
        "alive": True,
        "stopped": False,
        "last_shot": 0
    }

    wave1.append(enemy)

# =========================================================
# Wave2
# =========================================================
for i in range(6):

    enemy = {
        "x": 40 + i * 65,
        "y": -400 - i * 60,
        "target_y": 180,
        "speed": 5,
        "alive": True,
        "stopped": False,
        "last_shot": 0
    }

    wave2.append(enemy)

# =========================================================
# Wave3
# =========================================================
for i in range(8):

    enemy = {
        "x": random.randint(50, WIDTH - 100),
        "y": -600 - i * 120,
        "speed": random.randint(8, 12),
        "alive": True
    }

    wave3.append(enemy)

# =========================================================
# Wave4
# =========================================================
for i in range(5):

    enemy = {
        "x": 60 + i * 75,
        "y": -800 - i * 70,
        "target_y": 170,
        "speed": 4,
        "alive": True,
        "stopped": False,
        "last_shot": 0,
        "angle_offset": 0
    }

    wave4.append(enemy)

# =========================================================
# Wave5
# =========================================================
for i in range(7):

    enemy = {
        "x": random.randint(50, WIDTH - 100),
        "y": -1200 - i * 80,
        "target_y": random.randint(100, 250),
        "speed": 6,
        "alive": True,
        "stopped": False,
        "last_shot": 0
    }

    wave5.append(enemy)

# =========================================================
# 웨이브 클리어 체크
# =========================================================
def wave_cleared(wave):

    for enemy in wave:

        if enemy["alive"]:
            return False

    return True

# =========================================================
# 게임 루프
# =========================================================
while True:

    current_time = pygame.time.get_ticks()

    # -------------------------------------------------
    # 종료
    # -------------------------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # -------------------------------------------------
    # 입력
    # -------------------------------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_speed

    if keys[pygame.K_RIGHT]:
        player_x += player_speed

    if keys[pygame.K_UP]:
        player_y -= player_speed

    if keys[pygame.K_DOWN]:
        player_y += player_speed

    player_x = max(
        0,
        min(WIDTH - player_width, player_x)
    )

    player_y = max(
        0,
        min(HEIGHT - player_height, player_y)
    )

    # =========================================================
    # 자동 발사
    # =========================================================
    if current_time - last_shot > shoot_delay:

        bullets.append([
            player_x + player_width // 2 - bullet_width // 2,
            player_y
        ])

        last_shot = current_time

    # =========================================================
    # WAVE 1
    # =========================================================
    if current_wave == 1:

        for enemy in wave1:

            if enemy["alive"]:

                if not enemy["stopped"]:

                    enemy["y"] += enemy["speed"]

                    if enemy["y"] >= enemy["target_y"]:

                        enemy["stopped"] = True

                if enemy["stopped"]:

                    if current_time - enemy["last_shot"] > 1500:

                        for i in range(24):

                            angle = (
                                360 / 24
                            ) * i

                            rad = math.radians(angle)

                            dx = math.cos(rad) * 4
                            dy = math.sin(rad) * 4

                            enemy_bullets.append([
                                enemy["x"] + 40,
                                enemy["y"] + 40,
                                dx,
                                dy
                            ])

                        enemy["last_shot"] = current_time

        if wave_cleared(wave1):
            current_wave = 2

    # =========================================================
    # WAVE 2
    # =========================================================
    if current_wave == 2:

        for enemy in wave2:

            if enemy["alive"]:

                enemy["x"] += random.randint(-2, 2)

                if not enemy["stopped"]:

                    enemy["y"] += enemy["speed"]

                    if enemy["y"] >= enemy["target_y"]:

                        enemy["stopped"] = True

                if enemy["stopped"]:

                    if current_time - enemy["last_shot"] > 1200:

                        dx = player_x - enemy["x"]
                        dy = player_y - enemy["y"]

                        dist = math.sqrt(
                            dx * dx + dy * dy
                        )

                        if dist != 0:

                            dx /= dist
                            dy /= dist

                            enemy_bullets.append([
                                enemy["x"] + 35,
                                enemy["y"] + 35,
                                dx * 7,
                                dy * 7
                            ])

                        enemy["last_shot"] = current_time

        if wave_cleared(wave2):
            current_wave = 3

    # =========================================================
    # WAVE 3
    # =========================================================
    if current_wave == 3:

        for enemy in wave3:

            if enemy["alive"]:

                enemy["y"] += enemy["speed"]

                if random.randint(0, 20) == 0:

                    dx = player_x - enemy["x"]
                    dy = player_y - enemy["y"]

                    dist = math.sqrt(
                        dx * dx + dy * dy
                    )

                    if dist != 0:

                        dx /= dist
                        dy /= dist

                        enemy_bullets.append([
                            enemy["x"] + 35,
                            enemy["y"] + 35,
                            dx * 8,
                            dy * 8
                        ])

                if enemy["y"] > HEIGHT + 100:
                    enemy["y"] = -200

        if wave_cleared(wave3):
            current_wave = 4

    # =========================================================
    # WAVE 4
    # =========================================================
    if current_wave == 4:

        for enemy in wave4:

            if enemy["alive"]:

                if not enemy["stopped"]:

                    enemy["y"] += enemy["speed"]

                    if enemy["y"] >= enemy["target_y"]:

                        enemy["stopped"] = True

                if enemy["stopped"]:

                    if current_time - enemy["last_shot"] > 1000:

                        enemy["angle_offset"] += 15

                        for i in range(28):

                            angle = (
                                (360 / 28) * i
                            ) + enemy["angle_offset"]

                            rad = math.radians(angle)

                            dx = math.cos(rad) * 5
                            dy = math.sin(rad) * 5

                            enemy_bullets.append([
                                enemy["x"] + 40,
                                enemy["y"] + 40,
                                dx,
                                dy
                            ])

                        enemy["last_shot"] = current_time

        if wave_cleared(wave4):
            current_wave = 5

    # =========================================================
    # WAVE 5
    # =========================================================
    if current_wave == 5:

        for enemy in wave5:

            if enemy["alive"]:

                enemy["x"] += random.randint(-4, 4)

                if not enemy["stopped"]:

                    enemy["y"] += enemy["speed"]

                    if enemy["y"] >= enemy["target_y"]:

                        enemy["stopped"] = True

                if enemy["stopped"]:

                    if current_time - enemy["last_shot"] > 700:

                        for i in range(3):

                            target_x = (
                                player_x +
                                random.randint(-60, 60)
                            )

                            target_y = player_y

                            dx = target_x - enemy["x"]
                            dy = target_y - enemy["y"]

                            dist = math.sqrt(
                                dx * dx + dy * dy
                            )

                            if dist != 0:

                                dx /= dist
                                dy /= dist

                                enemy_bullets.append([
                                    enemy["x"] + 35,
                                    enemy["y"] + 35,
                                    dx * 9,
                                    dy * 9
                                ])

                        enemy["last_shot"] = current_time

        if wave_cleared(wave5):

            boss["alive"] = True

            current_wave = 6

    # =========================================================
    # 보스
    # =========================================================
    if current_wave == 6:

        if boss["y"] < boss["target_y"]:
            boss["y"] += boss["speed"]

        if current_time - boss["phase_timer"] > 7000:

            boss["phase"] += 1

            if boss["phase"] > 4:
                boss["phase"] = 1

            boss["phase_timer"] = current_time

        # 패턴1
        if boss["phase"] == 1:

            if current_time - boss["last_shot"] > 1200:

                for i in range(5):

                    enemy = {
                        "x": random.randint(
                            50,
                            WIDTH - 100
                        ),
                        "y": -100,
                        "speed": random.randint(4, 7),
                        "alive": True
                    }

                    wave3.append(enemy)

                boss["last_shot"] = current_time

        # 패턴2
        if boss["phase"] == 2:

            if current_time - boss["last_shot"] > 120:

                boss["rotation"] += 12

                bullet_count = 20

                for i in range(bullet_count):

                    angle = (
                        (360 / bullet_count) * i
                    ) + boss["rotation"]

                    rad = math.radians(angle)

                    dx = math.cos(rad) * 3
                    dy = math.sin(rad) * 3

                    boss_bullets.append([
                        boss["x"] + boss_width // 2,
                        boss["y"] + boss_height // 2,
                        dx,
                        dy
                    ])

                boss["last_shot"] = current_time

        # 패턴3
        if boss["phase"] == 3:

            if current_time - boss["last_shot"] > 500:

                for y in range(80, HEIGHT, 70):

                    for i in range(10):

                        boss_bullets.append([
                            WIDTH + (i * 60),
                            y,
                            -4,
                            0
                        ])

                boss["last_shot"] = current_time

        # 패턴4
        if boss["phase"] == 4:

            if current_time - boss["last_shot"] > 250:

                center_x = WIDTH + 100

                center_y = random.randint(
                    100,
                    500
                )

                bullet_count = 18

                for i in range(bullet_count):

                    angle = (
                        360 / bullet_count
                    ) * i

                    rad = math.radians(angle)

                    dx = math.cos(rad) * 2 -3
                    dy = math.sin(rad) * 2

                    boss_bullets.append([
                        center_x,
                        center_y,
                        dx,
                        dy
                    ])

                boss["last_shot"] = current_time

    # =========================================================
    # 플레이어 탄 이동
    # =========================================================
    for bullet in bullets:
        bullet[1] -= bullet_speed

    bullets = [
        b for b in bullets
        if b[1] > -100
    ]

    # =========================================================
    # 적 탄 이동
    # =========================================================
    for bullet in enemy_bullets:

        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    enemy_bullets = [

        b for b in enemy_bullets

        if -100 < b[0] < WIDTH + 100
        and -100 < b[1] < HEIGHT + 100
    ]

    # =========================================================
    # 보스 탄 이동
    # =========================================================
    for bullet in boss_bullets:

        bullet[0] += bullet[2]
        bullet[1] += bullet[3]

    boss_bullets = [

        b for b in boss_bullets

        if -100 < b[0] < WIDTH + 100
        and -100 < b[1] < HEIGHT + 100
    ]

    # =========================================================
    # 폭발 업데이트
    # =========================================================
    for particle in explosions:

        particle["x"] += particle["dx"]
        particle["y"] += particle["dy"]

        particle["life"] -= 1

    explosions = [

        p for p in explosions

        if p["life"] > 0
    ]

    # =========================================================
    # 적 충돌
    # =========================================================
    all_waves = [
        wave1,
        wave2,
        wave3,
        wave4,
        wave5
    ]

    for wave in all_waves:

        for enemy in wave:

            if enemy["alive"]:

                rect = pygame.Rect(
                    enemy["x"],
                    enemy["y"],
                    80,
                    80
                )

                for bullet in bullets[:]:

                    bullet_rect = pygame.Rect(
                        bullet[0],
                        bullet[1],
                        bullet_width,
                        bullet_height
                    )

                    if rect.colliderect(bullet_rect):

                        enemy["alive"] = False

                        create_explosion(
                            enemy["x"] + 40,
                            enemy["y"] + 40
                        )

                        if bullet in bullets:
                            bullets.remove(bullet)

                        break

    # =========================================================
    # 보스 충돌
    # =========================================================
    if boss["alive"]:

        boss_rect = pygame.Rect(
            boss["x"],
            boss["y"],
            boss_width,
            boss_height
        )

        for bullet in bullets[:]:

            bullet_rect = pygame.Rect(
                bullet[0],
                bullet[1],
                bullet_width,
                bullet_height
            )

            if boss_rect.colliderect(
                bullet_rect
            ):

                boss["hp"] -= 1

                create_explosion(
                    bullet[0],
                    bullet[1]
                )

                if bullet in bullets:
                    bullets.remove(bullet)

                if boss["hp"] <= 0:

                    boss["alive"] = False

                    game_clear = True

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
        screen.blit(
            bullet_img,
            (bullet[0], bullet[1])
        )

    # 적 탄
    for bullet in enemy_bullets:
        screen.blit(
            enemy_bullet_img,
            (bullet[0], bullet[1])
        )

    # 보스 탄
    for bullet in boss_bullets:
        screen.blit(
            boss_bullet_img,
            (bullet[0], bullet[1])
        )

    # 폭발
    for particle in explosions:

        pygame.draw.circle(
            screen,
            (255, 180, 40),
            (
                int(particle["x"]),
                int(particle["y"])
            ),
            particle["size"]
        )

    # 적 그리기
    for wave in all_waves:

        for enemy in wave:

            if enemy["alive"]:

                if wave in [
                    wave1,
                    wave3,
                    wave4
                ]:

                    screen.blit(
                        enemy1_img,
                        (enemy["x"], enemy["y"])
                    )

                else:

                    screen.blit(
                        enemy2_img,
                        (enemy["x"], enemy["y"])
                    )

    # 보스
    if boss["alive"]:

        screen.blit(
            boss_img,
            (boss["x"], boss["y"])
        )

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            (40, 20, 400, 20)
        )

        hp_width = int(
            400 * (boss["hp"] / 500)
        )

        pygame.draw.rect(
            screen,
            (255, 50, 50),
            (40, 20, hp_width, 20)
        )

    # 플레이어
    screen.blit(
        player_img,
        (player_x, player_y)
    )

    # 웨이브 표시
    font = pygame.font.SysFont(
        None,
        40
    )

    text = font.render(
        f"WAVE {current_wave}",
        True,
        (255, 255, 255)
    )

    screen.blit(text, (20, 50))

    # 게임 클리어
    if game_clear:

        clear_font = pygame.font.SysFont(
            None,
            80
        )

        clear_text = clear_font.render(
            "GAME CLEAR",
            True,
            (255, 255, 0)
        )

        screen.blit(
            clear_text,
            (40, HEIGHT // 2)
        )

    pygame.display.update()

    clock.tick(60)