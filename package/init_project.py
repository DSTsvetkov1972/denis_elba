import os
from colorama import Fore, init, Style
from package.logo import logo_colored

init()
print(Style.BRIGHT)
print(logo_colored)

if os.path.exists('Исходник'):
    print(Fore.GREEN, 'Папка Исходник существует', Fore.RESET)
else:
    os.mkdir('Исходник')
    print(Fore.GREEN, 'Создана папка Исходник', Fore.RESET)