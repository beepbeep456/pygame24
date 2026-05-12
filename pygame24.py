import pygame
import sys

# 초기화
pygame.init()

# 화면 크기
WIDTH = 480
HEIGHT = 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("탄막 슈팅")

clock = pygame.time.Clock()

# 배경 이미지 불러오기
bg = pygame.image.load("레벨 999 배경-Sheet.png").convert()

# 화면 크기에 맞게 확대
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

# 배경 위치
bg_y1 = 0
bg_y2 = -HEIGHT

# 배경 속도
speed = 20

while True:
    # 종료 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 배경 이동
    bg_y1 += speed
    bg_y2 += speed

    # 화면 아래로 완전히 내려가면 위로 이동
    if bg_y1 >= HEIGHT:
        bg_y1 = -HEIGHT

    if bg_y2 >= HEIGHT:
        bg_y2 = -HEIGHT

    # 배경 그리기
    screen.blit(bg, (0, bg_y1))
    screen.blit(bg, (0, bg_y2))

    pygame.display.update()
    clock.tick(60)
