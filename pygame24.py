import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Triangle Move")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

radius = 50

# 🔥 삼각형 중심 위치
x = 400
y = 300
speed = 5

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 🔥 키 입력
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # 🔥 화면 경계 제한
    x = max(radius, min(800 - radius, x))
    y = max(radius, min(600 - radius, y))

    screen.fill(WHITE)

    # 🔺 삼각형 좌표
    points = [
        (x, y - radius),          # 위
        (x - radius, y + radius), # 왼쪽 아래
        (x + radius, y + radius)  # 오른쪽 아래
    ]

    # 🔺 삼각형 그리기
    pygame.draw.polygon(screen, BLUE, points)

    # FPS 표시
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, BLACK)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()