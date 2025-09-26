import os
import sys
import shelve
from pathlib import Path


def get_save_path():
    """Получаем путь для сохранения в зависимости от платформы"""
    if getattr(sys, 'frozen', False):
        # Если программа запакована в exe
        if os.name == 'nt':  # Windows
            save_dir = Path(os.environ['APPDATA']) / 'IQ_Clicker'
        else:  # Linux/Mac
            save_dir = Path.home() / '.local' / 'share' / 'iq_clicker'
    else:
        # Если запущено как Python скрипт
        save_dir = Path(__file__).parent / 'saves'

    # Создаем папку, если ее нет
    save_dir.mkdir(parents=True, exist_ok=True)
    return save_dir / 'savegame.dat'


def save_game(IQ, IQ_per_click, upgrades_data, autoclicker_data):
    """Сохраняет данные игры"""
    try:
        save_path = get_save_path()
        with shelve.open(str(save_path)) as save_file:
            save_file['IQ'] = IQ
            save_file['IQ_per_click'] = IQ_per_click
            save_file['upgrades'] = upgrades_data
            save_file['autoclicker'] = autoclicker_data
        return True
    except Exception as e:
        print(f"Ошибка при сохранении: {e}")
        return False


def load_game():
    """Загружает данные игры"""
    try:
        save_path = get_save_path()
        with shelve.open(str(save_path)) as save_file:
            IQ = save_file.get('IQ', 0)
            IQ_per_click = save_file.get('IQ_per_click', 1)
            upgrades_data = save_file.get('upgrades', [])
            autoclicker_data = save_file.get('autoclicker', {})
        return IQ, IQ_per_click, upgrades_data, autoclicker_data
    except Exception:
        # Если файла нет или ошибка, возвращаем значения по умолчанию
        return 0, 1, [], {}

def save_upgrades(upgrades_list):
    """
    Подготавливает данные улучшений для сохранения
    """
    upgrades_data = []
    for upgrade in upgrades_list:
        upgrades_data.append({
            'name': upgrade.name,
            'level': upgrade.level,
            'b_cost': upgrade.b_cost,
            'cost_increase': upgrade.cost_increase,
            'b_iq_increase': upgrade.b_iq_increase
        })
    return upgrades_data

def load_upgrades(upgrades_list, upgrades_data):
    """
    Восстанавливает улучшения из сохраненных данных
    """
    for i, upgrade_data in enumerate(upgrades_data):
        if i < len(upgrades_list):
            upgrades_list[i].level = upgrade_data['level']

def save_autoclicker(autoclicker_obj):
    """
    Подготавливает данные автокликера для сохранения
    """
    return {
        'level': autoclicker_obj.level,
        'iq_per_second': autoclicker_obj.iq_per_second,
        'active': autoclicker_obj.active
    }

def load_autoclicker(autoclicker_obj, autoclicker_data):
    """
    Восстанавливает автокликер из сохраненных данных
    """
    autoclicker_obj.level = autoclicker_data.get('level', 0)
    autoclicker_obj.iq_per_second = autoclicker_data.get('iq_per_second', 0)
    autoclicker_obj.active = autoclicker_data.get('active', False)