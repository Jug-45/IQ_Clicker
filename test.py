from sprites import *
from font import *
from save_system import save_game, load_game, save_upgrades, load_upgrades, save_autoclicker, load_autoclicker
import pygame
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.init()

FPS = 60
clock = pygame.time.Clock()

# Базовое разрешение для разработки
BASE_WIDTH = 1600
BASE_HEIGHT = 900

# Текущее разрешение
screen_width = BASE_WIDTH
screen_height = BASE_HEIGHT

# Версия игры
VERSION = "v1.0"

# Инициализация звука
bgm = pygame.mixer.Sound(resource_path('music/Background.mp3'))
bgm.play(-1)
bgm.set_volume(0.2)
bgm_played = True

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("IQ Clicker")

render = my_font.render


# Функция для масштабирования размеров и позиций
def scale_rect(rect):
    x_scale = screen_width / BASE_WIDTH
    y_scale = screen_height / BASE_HEIGHT

    return pygame.Rect(
        rect.x * x_scale,
        rect.y * y_scale,
        rect.width * x_scale,
        rect.height * y_scale
    )


# Функция для масштабирования позиции
def scale_pos(x, y):
    x_scale = screen_width / BASE_WIDTH
    y_scale = screen_height / BASE_HEIGHT

    return (x * x_scale, y * y_scale)


# Создание текстовых поверхностей
text_surface = my_font_huge.render('IQ Clicker', False, "White")
play_text = render('Играть', False, "White")
settings_text = render('Настройки', False, "White")
exit_text = render('Выход', False, "White")
exit_text2 = exit_text
click_text = render('Клик', False, "White")
upgrade_text = render('Улучшения', False, "White")
minigames = render('Мини Игры', False, "White")
minigames_1 = render('1. Красный шарик', False, "White")
autoclicker_text = render('Автокликер', False, "White")
changelog_text = render('Change Log', False, "White")
version_text = my_font_small.render(VERSION, False, "White")

# Текст для Change Log
changelog_content = [
    "v1.0 - Initial Release:",
    "- Добавлена основная механика кликера",
    "- Система улучшений",
    "- Автокликер",
    "- Система сохранения",
    "- Настройки громкости и разрешения",
    "- Главное меню",
    "- Мини-игры (в разработке)",
    "",
    "v0.9 - Beta:",
    "- Базовая функциональность",
    "- Тестирование баланса",
    "- Исправление критических ошибок"
]

# Создание кнопок с базовыми координатами
press_play = pygame.Rect(920, 350, 400, 100)
press_settings = pygame.Rect(920, 500, 400, 100)
press_exit_1 = pygame.Rect(920, 650, 400, 100)
press_changelog = pygame.Rect(920, 200, 400, 100)
press_exit_2 = pygame.Rect(100, 50, 250, 100)
press_click = pygame.Rect(650, 400, 300, 150)
press_Minig = pygame.Rect(100, 200, 250, 100)
press_Minig_1 = pygame.Rect(600, 200, 350, 100)
press_upg = pygame.Rect(1200, 50, 300, 100)
press_autoclicker = pygame.Rect(100, 350, 250, 100)
press_save = pygame.Rect(100, 500, 250, 100)
press_load = pygame.Rect(100, 650, 250, 100)

# Кнопки настроек
volume_down_rect = pygame.Rect(920, 300, 50, 50)
volume_up_rect = pygame.Rect(1020, 300, 50, 50)
resolution_down_rect = pygame.Rect(920, 400, 50, 50)
resolution_up_rect = pygame.Rect(1020, 400, 50, 50)
apply_resolution_rect = pygame.Rect(920, 500, 200, 50)

button_color = "Black"
button_hover_color = (50, 50, 50)
button_click_color = (100, 100, 100)
current_button_color = button_color


class Autoclicker:
    def __init__(self):
        self.level = 0
        self.iq_per_second = 0
        self.last_update_time = pygame.time.get_ticks()
        self.active = False

    def update(self):
        if self.active and self.level > 0:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.last_update_time) / 1000.0

            if elapsed_time >= 1.0:
                global IQ
                IQ += self.iq_per_second
                self.last_update_time = current_time

    def upgrade(self, cost, iq_increase):
        global IQ
        if IQ >= cost:
            IQ -= cost
            self.level += 1
            self.iq_per_second += iq_increase
            self.active = True
            return True
        return False


class Upgrade:
    def __init__(self, name, b_cost, cost_increase, b_iq_increase):
        self.name = name
        self.level = 0
        self.b_cost = b_cost
        self.cost_increase = cost_increase
        self.b_iq_increase = b_iq_increase
        self.base_rect = pygame.Rect(1150, 150, 400, 80)  # Базовые координаты
        self.rect = pygame.Rect(0, 0, 400, 80)
        self.color = "Black"
        self.hover_color = (50, 50, 50)
        self.current_color = self.color

    @property
    def cost(self):
        return int(self.b_cost * (self.cost_increase ** self.level))

    @property
    def iq_increase(self):
        return self.b_iq_increase * (self.level + 1)

    def buy(self):
        global IQ, IQ_per_click
        if IQ >= self.cost:
            IQ -= self.cost
            IQ_per_click += self.b_iq_increase
            self.level += 1
            return True
        return False

    def update_position(self, index, scroll_offset=0):
        x_scale = screen_width / BASE_WIDTH
        y_scale = screen_height / BASE_HEIGHT

        self.rect.x = self.base_rect.x * x_scale
        self.rect.y = (self.base_rect.y + index * 100 - scroll_offset) * y_scale
        self.rect.width = self.base_rect.width * x_scale
        self.rect.height = self.base_rect.height * y_scale


# Создание автокликера
autoclicker = Autoclicker()

# Создание списка улучшений
upgrades = [
    Upgrade('Чтение книг', 15, 1.3, 1),
    Upgrade('Тренировка памяти', 50, 1.4, 2),
    Upgrade('Логические задачи', 150, 1.5, 5),
    Upgrade('Изучение наук', 500, 1.6, 10),
    Upgrade('Решение головоломок', 1500, 1.7, 20),
    Upgrade('Изучение языков', 4000, 1.8, 40),
    Upgrade('Квантовая физика', 10000, 1.9, 100),
    Upgrade('Генетика и биотех', 25000, 2.0, 250),
    Upgrade('Искусственный интеллект', 60000, 2.1, 500),
    Upgrade('Теория всего', 150000, 2.2, 1000)
]

# Автокликер улучшения
autoclicker_upgrades = [
    {"name": "Самообучение", "cost": 1000, "iq_per_second": 2},
    {"name": "Аудиокурсы", "cost": 5000, "iq_per_second": 10},
    {"name": "Онлайн-образование", "cost": 20000, "iq_per_second": 40},
    {"name": "Университет", "cost": 75000, "iq_per_second": 150},
    {"name": "Научный институт", "cost": 250000, "iq_per_second": 500},
    {"name": "Космические исследования", "cost": 1000000, "iq_per_second": 2000}
]

IQ, IQ_per_click, loaded_upgrades_data, loaded_autoclicker_data = load_game()
load_upgrades(upgrades, loaded_upgrades_data)
load_autoclicker(autoclicker, loaded_autoclicker_data)

upgrades_scroll_offset = 0
autoclicker_scroll_offset = 0
changelog_scroll_offset = 0
scroll_speed = 20

IQ = 0
IQ_per_click = 1

mouse_pressed = False
running = True

game_state = 'menu'

save_text = render('Сохранить', False, "White")
load_text = render('Загрузить', False, "White")

# Настройки
volume = 0.2
resolution_options = [
    {"name": "1600x900", "width": 1600, "height": 900},
    {"name": "1280x720", "width": 1280, "height": 720},
    {"name": "1920x1080", "width": 1920, "height": 1080}
]
current_resolution_index = 0


# Функция для обновления позиций всех элементов интерфейса
def update_ui_positions():
    global press_play, press_settings, press_exit_1, press_changelog, press_exit_2
    global press_click, press_Minig, press_Minig_1, press_upg, press_autoclicker, press_save, press_load
    global volume_down_rect, volume_up_rect, resolution_down_rect, resolution_up_rect, apply_resolution_rect

    # Базовые координаты для разрешения 1600x900
    base_rects = {
        'press_play': pygame.Rect(920, 350, 400, 100),
        'press_settings': pygame.Rect(920, 500, 400, 100),
        'press_exit_1': pygame.Rect(920, 650, 400, 100),
        'press_changelog': pygame.Rect(920, 200, 400, 100),
        'press_exit_2': pygame.Rect(100, 50, 250, 100),
        'press_click': pygame.Rect(650, 400, 300, 150),
        'press_Minig': pygame.Rect(100, 200, 250, 100),
        'press_Minig_1': pygame.Rect(600, 200, 350, 100),
        'press_upg': pygame.Rect(1200, 50, 300, 100),
        'press_autoclicker': pygame.Rect(100, 350, 250, 100),
        'press_save': pygame.Rect(100, 500, 250, 100),
        'press_load': pygame.Rect(100, 650, 250, 100),
        'volume_down_rect': pygame.Rect(920, 300, 50, 50),
        'volume_up_rect': pygame.Rect(1020, 300, 50, 50),
        'resolution_down_rect': pygame.Rect(920, 400, 50, 50),
        'resolution_up_rect': pygame.Rect(1020, 400, 50, 50),
        'apply_resolution_rect': pygame.Rect(920, 500, 200, 50)
    }

    # Масштабирование всех прямоугольников
    press_play = scale_rect(base_rects['press_play'])
    press_settings = scale_rect(base_rects['press_settings'])
    press_exit_1 = scale_rect(base_rects['press_exit_1'])
    press_changelog = scale_rect(base_rects['press_changelog'])
    press_exit_2 = scale_rect(base_rects['press_exit_2'])
    press_click = scale_rect(base_rects['press_click'])
    press_Minig = scale_rect(base_rects['press_Minig'])
    press_Minig_1 = scale_rect(base_rects['press_Minig_1'])
    press_upg = scale_rect(base_rects['press_upg'])
    press_autoclicker = scale_rect(base_rects['press_autoclicker'])
    press_save = scale_rect(base_rects['press_save'])
    press_load = scale_rect(base_rects['press_load'])
    volume_down_rect = scale_rect(base_rects['volume_down_rect'])
    volume_up_rect = scale_rect(base_rects['volume_up_rect'])
    resolution_down_rect = scale_rect(base_rects['resolution_down_rect'])
    resolution_up_rect = scale_rect(base_rects['resolution_up_rect'])
    apply_resolution_rect = scale_rect(base_rects['apply_resolution_rect'])


# Первоначальное обновление позиций
update_ui_positions()

while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            upgrades_data = save_upgrades(upgrades)
            autoclicker_data = save_autoclicker(autoclicker)
            save_game(IQ, IQ_per_click, upgrades_data, autoclicker_data)
            running = False

        # Обработка изменения размера окна
        if event.type == pygame.VIDEORESIZE:
            screen_width, screen_height = event.size
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            update_ui_positions()

        # Обработка прокрутки колесиком мыши
        if event.type == pygame.MOUSEWHEEL:
            if game_state == 'upgrades':
                upgrades_scroll_offset -= event.y * scroll_speed
                upgrades_scroll_offset = max(0, min(upgrades_scroll_offset, len(upgrades) * 100 - 500))
            elif game_state == 'autoclicker':
                autoclicker_scroll_offset -= event.y * scroll_speed
                autoclicker_scroll_offset = max(0,
                                                min(autoclicker_scroll_offset, len(autoclicker_upgrades) * 100 - 500))
            elif game_state == 'changelog':
                changelog_scroll_offset -= event.y * scroll_speed
                max_changelog_scroll = max(0, len(changelog_content) * 30 - 500)
                changelog_scroll_offset = max(0, min(changelog_scroll_offset, max_changelog_scroll))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
            if game_state == 'menu':
                if press_play.collidepoint(event.pos):
                    game_state = 'gameplay'
                if press_settings.collidepoint(event.pos):
                    game_state = 'settings'
                if press_exit_1.collidepoint(event.pos):
                    running = False
                if press_changelog.collidepoint(event.pos):
                    game_state = 'changelog'
                    changelog_scroll_offset = 0
            elif game_state == 'settings':
                if press_exit_2.collidepoint(event.pos):
                    game_state = 'menu'
                elif volume_down_rect.collidepoint(event.pos):
                    volume = max(0.0, volume - 0.05)
                    bgm.set_volume(volume)
                elif volume_up_rect.collidepoint(event.pos):
                    volume = min(1.0, volume + 0.05)
                    bgm.set_volume(volume)
                elif resolution_down_rect.collidepoint(event.pos):
                    current_resolution_index = max(0, current_resolution_index - 1)
                elif resolution_up_rect.collidepoint(event.pos):
                    current_resolution_index = min(len(resolution_options) - 1, current_resolution_index + 1)
                elif apply_resolution_rect.collidepoint(event.pos):
                    new_width = resolution_options[current_resolution_index]["width"]
                    new_height = resolution_options[current_resolution_index]["height"]
                    screen_width, screen_height = new_width, new_height
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    update_ui_positions()
            elif game_state == 'gameplay':
                if press_exit_2.collidepoint(event.pos):
                    game_state = 'menu'
                elif press_Minig.collidepoint(event.pos):
                    game_state = 'minigames'
                elif press_autoclicker.collidepoint(event.pos):
                    game_state = 'autoclicker'
                elif press_click.collidepoint(event.pos):
                    current_button_color = button_click_color
                    IQ += IQ_per_click
                elif press_upg.collidepoint(event.pos):
                    game_state = 'upgrades'
                    upgrades_scroll_offset = 0
                elif press_save.collidepoint(event.pos):
                    upgrades_data = save_upgrades(upgrades)
                    autoclicker_data = save_autoclicker(autoclicker)
                    if save_game(IQ, IQ_per_click, upgrades_data, autoclicker_data):
                        print("Игра сохранена!")
                    else:
                        print("Ошибка сохранения!")
                elif press_load.collidepoint(event.pos):
                    IQ, IQ_per_click, loaded_upgrades_data, loaded_autoclicker_data = load_game()
                    load_upgrades(upgrades, loaded_upgrades_data)
                    load_autoclicker(autoclicker, loaded_autoclicker_data)
                    print("Игра загружена!")
            elif game_state == 'minigames':
                if press_exit_2.collidepoint(event.pos):
                    game_state = 'gameplay'
            elif game_state == 'upgrades':
                if press_exit_2.collidepoint(event.pos):
                    game_state = 'gameplay'
                for upgrade in upgrades:
                    upgrade.update_position(upgrades.index(upgrade), upgrades_scroll_offset)
                    if upgrade.rect.collidepoint(event.pos):
                        upgrade.buy()
            elif game_state == 'autoclicker':
                if press_exit_2.collidepoint(event.pos):
                    game_state = 'gameplay'
                    autoclicker_scroll_offset = 0
                for i, upgrade in enumerate(autoclicker_upgrades):
                    upgrade_rect = pygame.Rect(
                        screen_width - 450 * (screen_width / BASE_WIDTH),
                        150 * (screen_height / BASE_HEIGHT) + i * 100 * (
                                    screen_height / BASE_HEIGHT) - autoclicker_scroll_offset,
                        400 * (screen_width / BASE_WIDTH),
                        80 * (screen_height / BASE_HEIGHT)
                    )
                    if upgrade_rect.collidepoint(event.pos):
                        if autoclicker.upgrade(upgrade["cost"], upgrade["iq_per_second"]):
                            autoclicker_upgrades.pop(i)
                            break
            elif game_state == 'changelog':
                if press_exit_2.collidepoint(event.pos):
                    game_state = 'menu'

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pressed = False
            current_button_color = button_color

    # Обновление автокликера
    autoclicker.update()

    # Обновление позиций улучшений
    for upgrade in upgrades:
        upgrade.update_position(upgrades.index(upgrade), upgrades_scroll_offset)

    # Проверка наведения на кнопки
    if press_click.collidepoint(mouse_pos):
        if mouse_pressed and game_state == 'gameplay':
            current_button_color = button_click_color
        elif game_state == 'gameplay':
            current_button_color = button_hover_color
    else:
        current_button_color = button_color

    for upgrade in upgrades:
        if upgrade.rect.collidepoint(mouse_pos):
            upgrade.current_color = upgrade.hover_color
        else:
            upgrade.current_color = upgrade.color

    # Создание текстовых поверхностей с актуальными значениями
    IQ_text = my_font.render(f'IQ: {IQ}', False, "White")
    iq_per_click_text = render(f'IQ за клик: {IQ_per_click} ', True, 'White')
    autoclicker_text_info = render(f'Автокликер: {autoclicker.iq_per_second} IQ/сек (Ур. {autoclicker.level})', True,
                                   'White')

    # Отображение версии игры
    version_display = my_font_small.render(VERSION, False, "White")

    # Отрисовка интерфейса в зависимости от состояния игры
    if game_state == 'menu':
        # Масштабирование фона под текущее разрешение
        scaled_think = pygame.transform.scale(think, (screen_width, screen_height))
        screen.blit(scaled_think, (0, 0))

        # Масштабирование позиции текста
        text_x, text_y = scale_pos(800, 100)
        screen.blit(text_surface, (text_x, text_y))

        # Отрисовка кнопок
        pygame.draw.rect(screen, current_button_color, press_play)
        pygame.draw.rect(screen, current_button_color, press_settings)
        pygame.draw.rect(screen, current_button_color, press_exit_1)
        pygame.draw.rect(screen, current_button_color, press_changelog)

        # Масштабирование позиций текста на кнопках
        play_x, play_y = scale_pos(1060, 375)
        settings_x, settings_y = scale_pos(1040, 525)
        exit_x, exit_y = scale_pos(1060, 675)
        changelog_x, changelog_y = scale_pos(1040, 225)

        screen.blit(play_text, (play_x, play_y))
        screen.blit(settings_text, (settings_x, settings_y))
        screen.blit(exit_text, (exit_x, exit_y))
        screen.blit(changelog_text, (changelog_x, changelog_y))

        # Отображение версии
        version_x, version_y = scale_pos(1580, 880)
        screen.blit(version_display, (version_x, version_y))

        if not bgm_played:
            bgm.play(-1)
            bgm.set_volume(0.2)
            bgm_played = True

    elif game_state == 'settings':
        screen.fill((50, 50, 50))

        # Заголовок настроек
        settings_title = my_font_huge.render("Настройки", True, "White")
        title_x, title_y = scale_pos(700, 100)
        screen.blit(settings_title, (title_x, title_y))

        # Настройка громкости
        volume_text = my_font.render(f"Громкость: {int(volume * 100)}%", True, "White")
        volume_text_x, volume_text_y = scale_pos(920, 250)
        screen.blit(volume_text, (volume_text_x, volume_text_y))

        # Кнопки регулировки громкости
        pygame.draw.rect(screen, button_color, volume_down_rect)
        pygame.draw.rect(screen, button_color, volume_up_rect)

        volume_down_x, volume_down_y = scale_pos(940, 310)
        volume_up_x, volume_up_y = scale_pos(1040, 310)

        screen.blit(my_font.render("-", True, "White"), (volume_down_x, volume_down_y))
        screen.blit(my_font.render("+", True, "White"), (volume_up_x, volume_up_y))

        # Настройка разрешения
        resolution_text = my_font.render("Разрешение экрана:", True, "White")
        resolution_text_x, resolution_text_y = scale_pos(920, 350)
        screen.blit(resolution_text, (resolution_text_x, resolution_text_y))

        current_res = resolution_options[current_resolution_index]
        resolution_value_text = my_font.render(current_res["name"], True, "White")
        resolution_value_x, resolution_value_y = scale_pos(920, 380)
        screen.blit(resolution_value_text, (resolution_value_x, resolution_value_y))

        # Кнопки изменения разрешения
        pygame.draw.rect(screen, button_color, resolution_down_rect)
        pygame.draw.rect(screen, button_color, resolution_up_rect)

        resolution_down_x, resolution_down_y = scale_pos(940, 410)
        resolution_up_x, resolution_up_y = scale_pos(1040, 410)

        screen.blit(my_font.render("<", True, "White"), (resolution_down_x, resolution_down_y))
        screen.blit(my_font.render(">", True, "White"), (resolution_up_x, resolution_up_y))

        # Кнопка применения разрешения
        pygame.draw.rect(screen, button_color, apply_resolution_rect)
        apply_x, apply_y = scale_pos(930, 515)
        screen.blit(my_font.render("Применить разрешение", True, "White"), (apply_x, apply_y))

        # Кнопка возврата
        pygame.draw.rect(screen, 'Black', press_exit_2)
        exit2_x, exit2_y = scale_pos(170, 75)
        screen.blit(exit_text2, (exit2_x, exit2_y))

        # Отображение версии
        version_x, version_y = scale_pos(1580, 880)
        screen.blit(version_display, (version_x, version_y))

    elif game_state == 'gameplay':
        # Масштабирование фона
        scaled_background = pygame.transform.scale(background, (screen_width, screen_height))
        screen.blit(scaled_background, (0, 0))

        pygame.draw.rect(screen, 'Black', press_exit_2)
        exit2_x, exit2_y = scale_pos(170, 75)
        screen.blit(exit_text2, (exit2_x, exit2_y))

        pygame.draw.rect(screen, current_button_color, press_click)
        click_x, click_y = scale_pos(770, 450)
        screen.blit(click_text, (click_x, click_y))

        # Отображение информации об IQ
        iq_x, iq_y = scale_pos(380, 100)
        iq_per_click_x, iq_per_click_y = scale_pos(380, 150)
        autoclicker_info_x, autoclicker_info_y = scale_pos(380, 200)

        screen.blit(IQ_text, (iq_x, iq_y))
        screen.blit(iq_per_click_text, (iq_per_click_x, iq_per_click_y))
        screen.blit(autoclicker_text_info, (autoclicker_info_x, autoclicker_info_y))

        # Отрисовка остальных кнопок
        pygame.draw.rect(screen, 'Black', press_Minig)
        minigames_x, minigames_y = scale_pos(140, 230)
        screen.blit(minigames, (minigames_x, minigames_y))

        pygame.draw.rect(screen, 'Black', press_upg)
        upgrade_x, upgrade_y = scale_pos(1270, 80)
        screen.blit(upgrade_text, (upgrade_x, upgrade_y))

        pygame.draw.rect(screen, 'Black', press_autoclicker)
        autoclicker_x, autoclicker_y = scale_pos(140, 380)
        screen.blit(autoclicker_text, (autoclicker_x, autoclicker_y))

        pygame.draw.rect(screen, 'Black', press_save)
        save_x, save_y = scale_pos(140, 530)
        screen.blit(save_text, (save_x, save_y))

        pygame.draw.rect(screen, 'Black', press_load)
        load_x, load_y = scale_pos(140, 680)
        screen.blit(load_text, (load_x, load_y))

        # Отображение версии
        version_x, version_y = scale_pos(1580, 880)
        screen.blit(version_display, (version_x, version_y))

    # Остальные состояния игры (minigames, upgrades, autoclicker, changelog) обрабатываются аналогично

    pygame.display.update()

    elif game_state == 'minigames':

        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, 'Black', press_exit_2)
        screen.blit(exit_text2, (170, 75))

        pygame.draw.rect(screen, 'Black', press_Minig_1)
        screen.blit(minigames_1, (635, 225))

        # Отображение версии
        screen.blit(version_display,
                    (height - version_display.get_width() - 20, width - version_display.get_height() - 20))
    elif game_state == 'upgrades':
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, 'Black', press_exit_2)
        screen.blit(exit_text2, (170, 75))

        screen.blit(IQ_text, (380, 100))
        screen.blit(iq_per_click_text, (380, 150))
        screen.blit(autoclicker_text_info, (380, 200))

        upgrade_title = render("Улучшения:", True, 'White')
        screen.blit(upgrade_title, (height - 450, 100 - upgrades_scroll_offset))

        for upgrade in upgrades:
            # Создаем скорректированный прямоугольник с учетом прокрутки
            adjusted_rect = pygame.Rect(
                upgrade.rect.x,
                upgrade.rect.y - upgrades_scroll_offset,
                upgrade.rect.width,
                upgrade.rect.height
            )

            # Проверяем, видима ли кнопка на экране
            if 0 <= adjusted_rect.y <= width:
                # Определение цвета кнопки
                if adjusted_rect.collidepoint(mouse_pos):
                    if IQ >= upgrade.cost:
                        upgrade.current_color = (0, 100, 0)  # Зеленый - можно купить
                    else:
                        upgrade.current_color = (100, 0, 0)  # Красный - нельзя купить
                else:
                    if IQ >= upgrade.cost:
                        upgrade.current_color = (0, 150, 0)  # Более светлый зеленый
                    else:
                        upgrade.current_color = (150, 0, 0)  # Более светлый красный

                # Рисуем кнопку улучшения
                pygame.draw.rect(screen, upgrade.current_color, adjusted_rect)

                # Создаем тексты с информацией об улучшении
                name_text = upg_font.render(f"{upgrade.name} (Ур. {upgrade.level})", True, 'White')
                cost_text = upg_font.render(f"Стоимость: {upgrade.cost} IQ", True, 'White')
                effect_text = upg_font.render(f"+{upgrade.b_iq_increase} IQ/клик", True, 'White')

                # Размещаем тексты на кнопке улучшения
                screen.blit(name_text, (adjusted_rect.x + 10, adjusted_rect.y + 5))
                screen.blit(cost_text, (adjusted_rect.x + 10, adjusted_rect.y + 30))
                screen.blit(effect_text, (adjusted_rect.x + 10, adjusted_rect.y + 55))

        # Отображение версии
        screen.blit(version_display,
                    (height - version_display.get_width() - 20, width - version_display.get_height() - 20))
    elif game_state == 'autoclicker':
        screen.blit(background, (0, 0))

        pygame.draw.rect(screen, 'Black', press_exit_2)
        screen.blit(exit_text2, (170, 75))

        screen.blit(IQ_text, (380, 100))
        screen.blit(iq_per_click_text, (380, 150))
        screen.blit(autoclicker_text_info, (380, 200))

        autoclicker_title = render("Улучшения автокликера:", True, 'White')
        screen.blit(autoclicker_title, (height - 450, 100 - autoclicker_scroll_offset))

        # Отрисовка улучшений автокликера с учетом прокрутки
        for i, upgrade in enumerate(autoclicker_upgrades):
            upgrade_rect = pygame.Rect(
                height - 450,
                150 + i * 100 - autoclicker_scroll_offset,
                400,
                80
            )

            # Проверяем, видима ли кнопка на экране
            if 0 <= upgrade_rect.y <= width:
                # Определение цвета кнопки
                if upgrade_rect.collidepoint(mouse_pos):
                    if IQ >= upgrade["cost"]:
                        color = (0, 100, 0)  # Зеленый - можно купить
                    else:
                        color = (100, 0, 0)  # Красный - нельзя купить
                else:
                    if IQ >= upgrade["cost"]:
                        color = (0, 150, 0)  # Более светлый зеленый
                    else:
                        color = (150, 0, 0)  # Более светлый красный

                pygame.draw.rect(screen, color, upgrade_rect)

                # Тексты с информацией об улучшении
                name_text = upg_font.render(upgrade["name"], True, 'White')
                cost_text = upg_font.render(f"Стоимость: {upgrade['cost']} IQ", True, 'White')
                effect_text = upg_font.render(f"+{upgrade['iq_per_second']} IQ/сек", True, 'White')

                screen.blit(name_text, (upgrade_rect.x + 10, upgrade_rect.y + 5))
                screen.blit(cost_text, (upgrade_rect.x + 10, upgrade_rect.y + 30))
                screen.blit(effect_text, (upgrade_rect.x + 10, upgrade_rect.y + 55))

