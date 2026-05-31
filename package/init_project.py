import os
from colorama import Fore, init, Style
from package.logo import logo_colored

init()
print(Style.BRIGHT)
print(logo_colored)

if not os.path.exists('Исходник'):
    os.mkdir('Исходник')
    print(Fore.GREEN, 'Создана папка Исходник', Fore.RESET)
    
if not os.path.exists('Архив'):
    os.mkdir('Архив')
    print(Fore.GREEN, 'Создана папка Архив', Fore.RESET)    