import pygame
import os
import sys

def resource_path(relative_path):
    try:
        # Пытаемся получить путь к временной папке (когда приложение упаковано в exe)
        base_path = sys._MEIPASS
    except Exception:
        # Если не упаковано, используем текущую директорию
        base_path = os.path.abspath(".")
    # Объединяем базовый путь с относительным путем к файлу
    return os.path.join(base_path, relative_path)
pygame.display.set_caption('IQ-Кликер')

# Загрузка и установка иконки окна
icon = pygame.image.load(resource_path('img/icon.png'))
pygame.display.set_icon(icon)
# Загрузка фонового изображения
think = pygame.image.load(resource_path('img/think_1.jpg'))
# Загрузка изображений для кнопок
Exit = pygame.image.load(resource_path('img/Exit_Button.png'))
Play = pygame.image.load(resource_path('img/Play_Button.png'))

laugh = pygame.image.load(resource_path('img/laugh.jpg'))

background = pygame.image.load(resource_path('img/background.png'))