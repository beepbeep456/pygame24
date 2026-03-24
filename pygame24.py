import pygame
import sys
import math

# --- SAT(분리축 정리) 충돌 감지 함수들 ---
def get_axes(vertices):
    axes = []
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        edge = p2 - p1
        if edge.length() != 0:
            normal = pygame.math.Vector2(-edge.y, edge.x).normalize()
            axes.append(normal)
    return axes

def project(vertices, axis):
    dots = [v.dot(axis) for v in vertices]
    return min(dots), max(dots)

def sat_collide(poly1_verts, poly2_verts):
    axes = get_axes(poly1_verts) + get_axes(poly2_verts)
    for axis in axes:
        min1, max1 = project(poly1_verts, axis)
        min2, max2 = project(poly2_verts, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True
# -----------------------------------------

# 1. Pygame 및 폰트 초기화
pygame.init()
pygame.font.init()  # 텍스트 출력을 위한 폰트 모듈 초기화
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Collision Types (Circle, AABB, OBB)")
clock = pygame.time.Clock()

# 시스템 기본 폰트 설정 (크기 36)
font = pygame.font.SysFont(None, 36)

# 색상 정의
BG_COLOR = (30, 30, 30)
GRAY = (150, 150, 150)
WHITE = (255, 255, 255)
RED = (255, 50, 50)      # AABB 색상
BLUE = (100, 150, 255)   # 원형 색상
GREEN = (50, 255, 50)    # OBB 색상

# 2. 오브젝트 설정
fixed_center = (WIDTH // 2, HEIGHT // 2)
fixed_width, fixed_height = 100, 100
fixed_surface = pygame.Surface((fixed_width, fixed_height), pygame.SRCALPHA)
fixed_surface.fill(GRAY)

moving_rect = pygame.Rect(100, 100, 80, 80)
speed = 5  

# 원의 반지름 설정
fixed_radius = fixed_width // 2
moving_radius = moving_rect.width // 2

# 회전 관련 변수
angle = 0
normal_rot_speed = 1
fast_rot_speed = 5

# 메인 루프
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # 이동 및 회전 처리
    if keys[pygame.K_LEFT]: moving_rect.x -= speed
    if keys[pygame.K_RIGHT]: moving_rect.x += speed
    if keys[pygame.K_UP]: moving_rect.y -= speed
    if keys[pygame.K_DOWN]: moving_rect.y += speed

    current_rot_speed = fast_rot_speed if keys[pygame.K_z] else normal_rot_speed
    angle = (angle + current_rot_speed) % 360

    # ==== 기하학적 데이터 계산 ====
    # 1. 고정된 오브젝트 회전 적용 및 AABB(rotated_rect) 획득
    rotated_surface = pygame.transform.rotate(fixed_surface, angle)
    rotated_rect = rotated_surface.get_rect(center=fixed_center)

    # 2. OBB 꼭짓점 계산
    center_vec = pygame.math.Vector2(fixed_center)
    hw, hh = fixed_width / 2, fixed_height / 2
    corners = [
        pygame.math.Vector2(-hw, -hh),
        pygame.math.Vector2(hw, -hh),
        pygame.math.Vector2(hw, hh),
        pygame.math.Vector2(-hw, hh)
    ]
    rotated_corners = [(center_vec + c.rotate(-angle)) for c in corners]
    moving_corners = [
        pygame.math.Vector2(moving_rect.topleft),
        pygame.math.Vector2(moving_rect.topright),
        pygame.math.Vector2(moving_rect.bottomright),
        pygame.math.Vector2(moving_rect.bottomleft)
    ]

    # 3. 원형 충돌용 거리 계산
    dx = fixed_center[0] - moving_rect.centerx
    dy = fixed_center[1] - moving_rect.centery
    distance = math.hypot(dx, dy)

    # ==== 충돌 감지 평가 ====
    circle_hit = distance <= (fixed_radius + moving_radius)
    aabb_hit = rotated_rect.colliderect(moving_rect)  # Pygame 내장 AABB 충돌 함수
    obb_hit = sat_collide(rotated_corners, moving_corners)

    # ==== 화면 그리기 ====
    screen.fill(BG_COLOR)

    # 오브젝트 본체 렌더링
    screen.blit(rotated_surface, rotated_rect.topleft)
    pygame.draw.rect(screen, GRAY, moving_rect)

    # AABB 렌더링 (빨간색)
    pygame.draw.rect(screen, RED, rotated_rect, 3)
    pygame.draw.rect(screen, RED, moving_rect, 3)

    # OBB 렌더링 (초록색)
    pygame.draw.polygon(screen, GREEN, rotated_corners, 3)

    # 원형 Bounding Box 렌더링 (파란색)
    pygame.draw.circle(screen, BLUE, fixed_center, fixed_radius, 3)
    pygame.draw.circle(screen, BLUE, moving_rect.center, moving_radius, 3)

    # ==== 텍스트 렌더링 (좌측 상단) ====
    # 충돌 시 각 영역의 색상으로 HIT 표시, 아닐 경우 흰색으로 MISS 표시
    circle_text_color = BLUE if circle_hit else WHITE
    aabb_text_color = RED if aabb_hit else WHITE
    obb_text_color = GREEN if obb_hit else WHITE

    circle_text = font.render(f"Circle: {'HIT' if circle_hit else 'MISS'}", True, circle_text_color)
    aabb_text = font.render(f"AABB: {'HIT' if aabb_hit else 'MISS'}", True, aabb_text_color)
    obb_text = font.render(f"OBB:  {'HIT' if obb_hit else 'MISS'}", True, obb_text_color)

    # 화면에 텍스트 그리기 (x, y 좌표 지정)
    screen.blit(circle_text, (20, 20))
    screen.blit(aabb_text, (20, 60))
    screen.blit(obb_text, (20, 100))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
# 1.원형 aaa모서리 차이
# aaa의 모서리는 사각형 형태로 대가선 모서리 끝까지 충돌 영역이 차있음
# 원형의 모서리는 중심에서 일정한 거리만큼을 영역으로 삼아 뾰족한 모서리가 깎여 있음
# 2.AABB vs OBB 회전 시 차이
# AABB: 경계 상자가 X축 Y축과 평행해야 함
# 오브젝트가 회전하는 각도에 맞춰 상자도 같이 회전
# 3.어떤 방식이 더 적합할까
#회전 상태가 중요한 대부분의 게임들은 OBB를 사용하게 될거 같다
# 4. AI에게 한 질문 중 흥미로운 답
# sqrt를 사용하던 사용하지 않던 충돌 판정 결과는 100% 동일하다는 답이 제일 흥미로웠