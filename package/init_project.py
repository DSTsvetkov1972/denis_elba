import os, sys
sys.path.append(os.getcwd())

from colorama import Fore, init, Style
from package.logo import logo_colored
from package.api import get_all_contractors, get_all_goods
from package.sqlite import df_to_sqlite
from package.logo import version

init()
print(Style.BRIGHT)
print(logo_colored)

if not os.path.exists(os.path.join(os.getcwd(), 'Исходник')):
    os.makedirs(os.path.join(os.getcwd(), 'Исходник'))
    print(Fore.GREEN+'Создана папка Исходник'+Fore.RESET)
    
if not os.path.exists(os.path.join(os.getcwd(), 'Архив')):
    os.makedirs(os.path.join(os.getcwd(), 'Архив'))
    print(Fore.GREEN+'Создана папка Архив'+Fore.RESET)

#if not os.path.exists(os.path.join(os.path.expanduser('~'), f'invoice_creator_{version}', 'app.db')):
#    print(Fore.YELLOW + 'Создаём базу данных контрагентов и номенклатуры...' + Fore.RESET)

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
