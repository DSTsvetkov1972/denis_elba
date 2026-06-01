import os, sys
sys.path.append(os.getcwd())

from colorama import Fore, init, Style
from package.logo import logo_colored
from package.api import get_all_contractors, get_all_goods
from package.sqlite import df_to_sqlite

init()
print(Style.BRIGHT)
print(logo_colored)

if not os.path.exists('Исходник'):
    os.mkdir('Исходник')
    print(Fore.GREEN+'Создана папка Исходник'+Fore.RESET)
    
if not os.path.exists('Архив'):
    os.mkdir('Архив')
    print(Fore.GREEN+'Создана папка Архив'+Fore.RESET)

if not os.path.exists(os.path.join(os.getcwd(), 'app.db')):
    print(Fore.YELLOW + 'Создаём базу данных контрагентов и номенклатуры...' + Fore.RESET)

    all_contractors_df = get_all_contractors()

    if all_contractors_df[0]:
        df_to_sqlite(all_contractors_df[1], 'contractors')
    else:
        print(Fore.RED+f'\n{all_contractors_df[1]}\n'+Fore.RESET)

                
    all_goods_df = get_all_goods()

    if all_goods_df[0]:
        df_to_sqlite(all_goods_df[1], 'goods')
    else:
        print(Fore.RED+f'\n{all_goods_df[1]}\n'+Fore.RESET)
