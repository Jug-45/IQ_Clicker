import pygame
import sys
import random
import math

pygame.init()

WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Кликер")

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

circle_radius = 30
circle_x = random.randint(circle_radius, WIDTH - circle_radius)
circle_y = random.randint(circle_radius, HEIGHT - circle_radius)

font = pygame.font.SysFont("Arial", 36) or pygame.font.SysFont(None, 36)

score = 0
game_over = False

clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)

    if not game_over:
        pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                mouse_x, mouse_y = event.pos
                distance = math.sqrt((mouse_x - circle_x) ** 2 + (mouse_y - circle_y) ** 2)
                if distance <= circle_radius:
                    score += 1
                    circle_x = random.randint(circle_radius, WIDTH - circle_radius)
                    circle_y = random.randint(circle_radius, HEIGHT - circle_radius)
                else:
                    game_over = True
            else:
                score = 0
                game_over = False
                circle_x = random.randint(circle_radius, WIDTH - circle_radius)
                circle_y = random.randint(circle_radius, HEIGHT - circle_radius)

    if game_over:
        text = font.render("Ты проиграл!", True, BLACK)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2,
                           HEIGHT // 2 - text.get_height() // 2))
        restart = font.render("Кликни чтобы начать заново", True, BLACK)
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2,
                              HEIGHT // 2 + 40))
    else:
        score_text = font.render(f"Очки: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()
