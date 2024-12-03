import pygame
import random
import sys

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
WIDTH, HEIGHT = 600, 400
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fruit Catcher Game')

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 128, 255)

# Tốc độ và thời gian
clock = pygame.time.Clock()
FPS = 60

# Biến trò chơi
basket_width = 100
basket_height = 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height
basket_speed = 10

fruit_size = 20
fruit_x = random.randint(0, WIDTH - fruit_size)
fruit_y = 0
fruit_speed = 5

score = 0
lives = 3

# Font chữ
font = pygame.font.Font(None, 36)


def draw_text(text, font, color, surface, x, y):
    """Vẽ văn bản trên màn hình."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def reset_fruit():
    """Đặt lại vị trí quả rơi."""
    global fruit_x, fruit_y
    fruit_x = random.randint(0, WIDTH - fruit_size)
    fruit_y = 0


def game_over():
    """Kết thúc trò chơi."""
    window.fill(WHITE)
    draw_text(f'Game Over - Final Score: {score}',
              font, RED, window, WIDTH // 4, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


# Vòng lặp chính của game
running = True
while running:
    window.fill(WHITE)

    # Xử lý các sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Nhận phím điều khiển
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
        basket_x += basket_speed

    # Cập nhật vị trí quả
    fruit_y += fruit_speed

    # Kiểm tra va chạm giữa quả và giỏ
    if (fruit_y + fruit_size >= basket_y and
            basket_x <= fruit_x <= basket_x + basket_width):
        score += 1
        reset_fruit()

    # Kiểm tra nếu quả rơi xuống dưới mà không bắt được
    if fruit_y > HEIGHT:
        lives -= 1
        reset_fruit()
        if lives == 0:
            game_over()

    # Vẽ giỏ
    pygame.draw.rect(window, BLUE, (basket_x, basket_y,
                     basket_width, basket_height))

    # Vẽ quả
    pygame.draw.ellipse(
        window, RED, (fruit_x, fruit_y, fruit_size, fruit_size))

    # Vẽ điểm số và mạng sống
    draw_text(f'Score: {score}', font, RED, window, 10, 10)
    draw_text(f'Lives: {lives}', font, RED, window, 10, 40)

    # Cập nhật màn hình
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
