import pygame
import random
import math

# 1. 초기 설정
pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Delayed Particle Playground")

clock = pygame.time.Clock()

# 리스트 관리: 실제 입자들과 '예약된' 폭발들
particles = []
waiting_explosions = []

# 2. Particle 클래스 (입자의 성격)
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        # 사방으로 퍼지는 각도와 속도
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 6)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(40, 80)
        self.size = random.randint(3, 7)

        # 무작위 색상 (보라~하늘색 계열)
        self.color = (
            random.randint(150, 255),
            random.randint(100, 255),
            random.randint(150, 255)
        )

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.08  # 중력 효과
        self.life -= 1

    def draw(self, surf):
        if self.life > 0:
            pygame.draw.circle(
                surf,
                self.color,
                (int(self.x), int(self.y)),
                self.size
            )

    def alive(self):
        return self.life > 0

# 3. 배경 그리기 함수 (일렁이는 효과)
def draw_background(surface, t):
    for y in range(HEIGHT):
        # 사인 함수를 이용해 세로 방향으로 색상이 변함
        c = int(40 + 30 * math.sin(y * 0.01 + t))
        color = (10, c, 50 + c // 2)
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

# 4. 메인 루프
running = True
time_counter = 0

while running:
    # (1) 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 마우스 클릭 시 '폭발 예약' (클릭할 때 딱 한 번만 등록되도록)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 왼쪽 클릭
                # 현재 시각으로부터 500ms(0.5초) 뒤에 터지도록 설정
                trigger_time = pygame.time.get_ticks() + 500
                waiting_explosions.append({
                    "pos": event.pos,
                    "time": trigger_time
                })

    # (2) 예약된 폭발 확인 및 처리
    current_time = pygame.time.get_ticks()
    remained_waiting = []

    for exp in waiting_explosions:
        if current_time >= exp["time"]:
            # 시간이 됐으면 실제 파티클 20개 생성
            for _ in range(20):
                particles.append(Particle(exp["pos"][0], exp["pos"][1]))
        else:
            # 아직 시간이 안 됐으면 대기 목록에 유지
            remained_waiting.append(exp)
    
    waiting_explosions = remained_waiting

    # (3) 업데이트 및 그리기
    time_counter += 0.03
    draw_background(screen, time_counter)

    # 대기 중인 폭발 위치에 작은 점 표시 (힌트 효과)
    for exp in waiting_explosions:
        # 0.5초 동안 깜빡이는 효과
        if (current_time // 100) % 2 == 0:
            pygame.draw.circle(screen, (255, 255, 255), exp["pos"], 3)

    # 파티클 업데이트 및 그리기
    for p in particles:
        p.update()
        p.draw(screen)

    # 죽은 파티클 제거
    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()