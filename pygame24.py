import pygame
import random
import sys

pygame.init()

def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GRAY    = (20,  20,  40)
BLUE    = (50,  150, 255)
RED     = (220, 50,  50)
YELLOW  = (240, 220, 0)
GREEN   = (50,  220, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter - Advanced & Visual")
clock = pygame.time.Clock()
font = get_korean_font(30)
font_big = get_korean_font(72)

# --- 레벨 설정 ---
LEVELS = [
    {"enemy_speed": 2, "spawn": 60, "label": "Lv.1"},
    {"enemy_speed": 3, "spawn": 40, "label": "Lv.2"},
    {"enemy_speed": 5, "spawn": 25, "label": "Lv.3"},
]


# --- 이미지 로드 ---
try:
    # 1. 원본 이미지를 불러옵니다. (13.png로 변환한 파일을 사용한다고 가정합니다)
    player_img_original = pygame.image.load("24.png").convert_alpha()
    
    # 2. ★ 핵심: 원하는 크기를 정합니다. (가로, 세로)
    # 예: 32x32는 원래(약 64x64 추정)의 절반 크기입니다. 
    # 더 줄이고 싶다면 (24, 24)나 (16, 16)으로 숫자를 낮추세요.
    target_size = (32, 32) 
    
    # 3. ★ 중요: 픽셀 아트를 깨지지 않게 줄이는 함수를 사용합니다.
    # pygame.transform.scale 대신 'smoothscale'을 사용하면 
    # 이미지가 작아져도 경계선이 부드럽고 깔끔하게 유지됩니다.
    player_img = pygame.transform.smoothscale(player_img_original, target_size)
    
    # 4. 줄어든 이미지의 크기를 게임 변수에 적용합니다.
    PLAYER_W = player_img.get_width()
    PLAYER_H = player_img.get_height()
    
except FileNotFoundError:
    print("13.png 이미지를 찾을 수 없습니다. 기본 파란색 네모를 사용합니다.")
    player_img = None
    PLAYER_W, PLAYER_H = 40, 40 # 이미지 없을 때 기본 크기
ENEMY_W,  ENEMY_H  = 36, 36
BULLET_SIZE = 10

def draw_player(surf, rect, img, facing):
    if img:
        # 바라보는 방향에 따른 회전 각도 계산
        angle = 0
        if facing == (1, 0): # 오른쪽
            angle = -90
        elif facing == (0, 1): # 아래
            angle = 180
        elif facing == (-1, 0): # 왼쪽
            angle = 90
        
        # 이미지 회전 및 중앙 맞춤
        rotated_img = pygame.transform.rotate(img, angle)
        rotated_rect = rotated_img.get_rect(center=rect.center)
        surf.blit(rotated_img, rotated_rect)
    else:
        # 이미지가 없을 경우 기본 네모 그리기
        pygame.draw.rect(surf, BLUE, rect, border_radius=5)
        pygame.draw.rect(surf, YELLOW, (rect.centerx - 4, rect.centery - 4, 8, 8))

def draw_enemy(surf, rect):
    pygame.draw.rect(surf, RED, rect, border_radius=8)

def spawn_enemy(level_cfg):
    # 위, 왼쪽, 오른쪽 중 무작위 스폰
    side = random.choice(["top", "left", "right"])
    speed = level_cfg["enemy_speed"]
    
    if side == "top":
        rect = pygame.Rect(random.randint(0, WIDTH - ENEMY_W), -ENEMY_H, ENEMY_W, ENEMY_H)
        return {"rect": rect, "dx": 0, "dy": speed}
    elif side == "left":
        rect = pygame.Rect(-ENEMY_W, random.randint(0, HEIGHT - ENEMY_H), ENEMY_W, ENEMY_H)
        return {"rect": rect, "dx": speed, "dy": 0}
    else: # right
        rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT - ENEMY_H), ENEMY_W, ENEMY_H)
        return {"rect": rect, "dx": -speed, "dy": 0}

def draw_stars(stars):
    for s in stars:
        pygame.draw.circle(screen, WHITE, (s[0], s[1]), s[2])

def draw_hud(score, lives, level_cfg, ammo, max_ammo, reload_timer, m_time, m_kills, m_target):
    # 점수와 목숨
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (10, 40))
    
    # 탄창 정보
    if reload_timer > 0:
        ammo_text = font.render("RELOADING...", True, RED)
    else:
        ammo_text = font.render(f"Ammo: {ammo}/{max_ammo}", True, YELLOW)
    screen.blit(ammo_text, (10, 70))

    # 타임어택 미션 정보
    time_sec = max(0, m_time // FPS)
    mission_text = font.render(f"Time: {time_sec}s | Target: {m_kills}/{m_target}", True, GREEN if time_sec > 5 else RED)
    screen.blit(mission_text, (WIDTH // 2 - mission_text.get_width() // 2, 10))
    screen.blit(font.render(level_cfg["label"], True, YELLOW), (WIDTH // 2 - 25, 40))

def game_over_screen(score, reason=""):
    screen.fill((10, 10, 30))
    screen.blit(font_big.render("GAME OVER", True, RED), (WIDTH//2 - 180, HEIGHT//2 - 80))
    if reason:
        screen.blit(font.render(reason, True, YELLOW), (WIDTH//2 - 150, HEIGHT//2 + 10))
    screen.blit(font.render(f"Final Score: {score}", True, WHITE), (WIDTH//2 - 90, HEIGHT//2 + 50))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (WIDTH//2 - 120, HEIGHT//2 + 90))
    pygame.display.flip()
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()

def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT // 2, PLAYER_W, PLAYER_H)
    facing = (0, -1) # 처음에는 위쪽을 바라봄
    
    bullets  = []
    enemies  = []
    
    score    = 0
    lives    = 3
    invincible = 0
    
    # 탄창 시스템
    max_ammo = 10
    current_ammo = max_ammo
    shoot_cd = 0
    reload_timer = 0
    reload_delay = 120 # 2초(60프레임 * 2) 딜레이
    
    # 타임어택 미션 시스템
    mission_time = 15 * FPS # 15초 제한
    mission_kills = 0
    mission_target = 5 # 15초 내에 5마리 잡기
    
    spawn_timer = 0
    level_idx = 0
    level_cfg = LEVELS[level_idx]

    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 2)) for _ in range(80)]

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        
        # 이동 및 방향 전환 (누른 방향 기억하기)
        if keys[pygame.K_LEFT]  and player.left  > 0:      
            player.x -= 6; facing = (-1, 0)
        if keys[pygame.K_RIGHT] and player.right < WIDTH:   
            player.x += 6; facing = (1, 0)
        if keys[pygame.K_UP]    and player.top   > 0:      
            player.y -= 6; facing = (0, -1)
        if keys[pygame.K_DOWN]  and player.bottom < HEIGHT: 
            player.y += 6; facing = (0, 1)

        # 총알 발사 및 재장전 로직
        shoot_cd -= 1
        
        if reload_timer > 0:
            reload_timer -= 1
            if reload_timer <= 0:
                current_ammo = max_ammo # 재장전 완료
                
        if keys[pygame.K_SPACE] and shoot_cd <= 0 and current_ammo > 0 and reload_timer <= 0:
            bx = player.centerx - BULLET_SIZE // 2
            by = player.centery - BULLET_SIZE // 2
            b_rect = pygame.Rect(bx, by, BULLET_SIZE, BULLET_SIZE)
            
            # 바라보는 방향으로 총알 발사
            bullets.append({"rect": b_rect, "dx": facing[0] * 12, "dy": facing[1] * 12})
            
            current_ammo -= 1
            shoot_cd = 15
            
            if current_ammo <= 0:
                reload_timer = reload_delay

        # 미션(타임어택) 로직
        mission_time -= 1
        if mission_time <= 0:
            if mission_kills < mission_target:
                if game_over_screen(score, "MISSION FAILED! Time Out!"):
                    main()
                return
            else:
                mission_time = 15 * FPS
                mission_kills = 0
                mission_target += 2
                score += 50

        # 총알 이동
        for b in bullets:
            b["rect"].x += b["dx"]
            b["rect"].y += b["dy"]
        
        # 화면 밖으로 나간 총알 지우기
        bullets = [b for b in bullets if 0 <= b["rect"].right and b["rect"].left <= WIDTH and 0 <= b["rect"].bottom and b["rect"].top <= HEIGHT]

        # 적 생성
        spawn_timer += 1
        if spawn_timer >= level_cfg["spawn"]:
            spawn_timer = 0
            enemies.append(spawn_enemy(level_cfg))

        # 적 이동
        alive_enemies = []
        for en in enemies:
            en["rect"].x += en["dx"]
            en["rect"].y += en["dy"]
            if -50 <= en["rect"].y <= HEIGHT + 50 and -50 <= en["rect"].x <= WIDTH + 50:
                alive_enemies.append(en)
        enemies = alive_enemies

        # 충돌 판정 (총알 vs 적)
        hit_bullets = set()
        hit_enemies = set()
        for bi, b in enumerate(bullets):
            for ei, en in enumerate(enemies):
                if b["rect"].colliderect(en["rect"]):
                    hit_bullets.add(bi)
                    hit_enemies.add(ei)
                    score += 10
                    mission_kills += 1
                    # 명중 시 총알 1개 회복
                    current_ammo = min(max_ammo, current_ammo + 1)

        bullets  = [b  for i, b  in enumerate(bullets)  if i not in hit_bullets]
        enemies  = [en for i, en in enumerate(enemies)   if i not in hit_enemies]

        # 레벨업
        level_idx = min(score // 150, len(LEVELS) - 1)
        level_cfg = LEVELS[level_idx]

        # 충돌 판정 (플레이어 vs 적)
        if invincible > 0:
            invincible -= 1
        else:
            for en in enemies:
                if player.colliderect(en["rect"]):
                    lives -= 1
                    invincible = 90
                    enemies.clear() # 맞으면 화면에 있는 적 모두 지우기
                    if lives <= 0:
                        if game_over_screen(score, "SHIP DESTROYED!"):
                            main()
                        return
                    break

        # 화면 그리기
        screen.fill(GRAY)
        draw_stars(stars)

        for b in bullets:
            pygame.draw.rect(screen, YELLOW, b["rect"])

        for en in enemies:
            draw_enemy(screen, en["rect"])

        blink = (invincible // 10) % 2 == 0
        if blink:
            draw_player(screen, player, player_img, facing)

        draw_hud(score, lives, level_cfg, current_ammo, max_ammo, reload_timer, mission_time, mission_kills, mission_target)
        pygame.display.flip()

if __name__ == "__main__":
    main()