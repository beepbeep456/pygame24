import pygame
import sys

# Pygame 초기화
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

# 1. 원의 초기 좌표(x, y)와 이동 속도(speed) 변수 추가
x = 400
y = 300
speed = 5

running = True
while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. 키보드 입력 감지 및 좌표 변경
    # pygame.key.get_pressed()를 사용하면 키를 꾹 누르고 있을 때 부드럽게 연속으로 이동합니다.
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:   # 왼쪽 방향키
        x -= speed
    if keys[pygame.K_RIGHT]:  # 오른쪽 방향키
        x += speed
    if keys[pygame.K_UP]:     # 위쪽 방향키
        y -= speed
    if keys[pygame.K_DOWN]:   # 아래쪽 방향키
        y += speed

    # 화면 그리기
    screen.fill(WHITE)
    
    # 3. 고정된 좌표(400, 300) 대신 변수 (x, y)를 사용하도록 수정
    pygame.draw.circle(screen, BLUE, (x, y), 50)
    
    pygame.display.flip()
    clock.tick(60)

# 종료 처리
pygame.quit()
sys.exit()