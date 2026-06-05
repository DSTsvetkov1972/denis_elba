# Сгенерировано с помощью https://www.asciiart.eu/text-to-ascii-art
# ANSI Shadow

from colorama import Fore


logo = Fore.MAGENTA + """
********************************************************************************
                    СОЗДАНИЕ НАКЛАДНЫХ В ЭЛЬБЕ НА ОСНОВЕ
                           ВЫГРУЗКИ ИЗ УМНЫХ ВЕСОВ
********************************************************************************
""" + Fore.RESET



version = " v.2026-06-05BIZ"

advertisement = """
 Нужна быстрая автоматизация или аналитика
 без ТЗ, совещаний, бюрократии и миллионного бюджета?
 Обращайтесь:
 Цветков Дмитрий Сергеевич
 DSTsvetkovPRO@yandex.ru
 +7 (903) 617-77-55
"""

advertisement_colored = Fore.YELLOW + advertisement + Fore.RESET

logo_colored = ''
for ch in list(logo):
    if ch in ['╝', '═', '║', '╔', '╚', '╗']:
        ch_colored = Fore.MAGENTA+ ch + Fore.RESET
    elif ch in ('█', '▄', '▀'):    
        ch_colored = Fore.CYAN + chr(9619) + Fore.RESET
    else:
        ch_colored = ch
    logo_colored += ch_colored

version_colored = Fore.BLACK + version + Fore.RESET    

logo_colored = logo_colored + version_colored + advertisement_colored