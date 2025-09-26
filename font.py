import pygame
import sys
import os
def resource_path(relative_path):
    try:
        # Пытаемся получить путь к временной папке (когда приложение упаковано в exe)
        base_path = sys._MEIPASS
    except Exception:
        # Если не упаковано, используем текущую директорию
        base_path = os.path.abspath(".")
    # Объединяем базовый путь с относительным путем к файлу
    return os.path.join(base_path, relative_path)
pygame.init()

my_font_huge = pygame.font.Font(resource_path('ttf_otf/Andy_Bold.otf'), 180)
my_font = pygame.font.Font(resource_path('ttf_otf/Andy_Bold.otf'), 40)
upg_font = pygame.font.Font(resource_path('ttf_otf/Andy_Bold.otf'), 25)
my_font_small = pygame.font.Font(resource_path('ttf_otf/Andy_Bold.otf'), 20)