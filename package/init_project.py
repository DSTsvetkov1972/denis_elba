import os, sys
sys.path.append(os.getcwd())
import yaml

from colorama import Fore, init, Style
from package.logo import logo_colored
from package.api import get_all_contractors, get_all_goods
from package.sqlite import df_to_sqlite
from package.logo import version


init()
print(Style.BRIGHT)
print(logo_colored)

with open(os.path.join(os.getcwd(), 'config.yml'), 'r', encoding='utf-8') as f:
    config_info = yaml.safe_load(f)
    COMPANIES = config_info['COMPANIES']
    DOWNLOAD_COUNTERPARTIES_ON_START = config_info['DOWNLOAD_COUNTERPARTIES_ON_START']
    DOWNLOAD_GOODS_ON_START = config_info['DOWNLOAD_GOODS_ON_START']

if not os.path.exists(os.path.join(os.getcwd(), 'Исходник')):
    os.makedirs(os.path.join(os.getcwd(), 'Исходник'))
    print(Fore.GREEN+'Создана папка Исходник'+Fore.RESET)
    
if not os.path.exists(os.path.join(os.getcwd(), 'Архив')):
    os.makedirs(os.path.join(os.getcwd(), 'Архив'))
    print(Fore.GREEN+'Создана папка Архив'+Fore.RESET)

db_exists = os.path.exists(os.path.join(os.getcwd(), 'app.db'))

if not db_exists or DOWNLOAD_COUNTERPARTIES_ON_START:
    all_contractors_df = get_all_contractors()

    if all_contractors_df[0]:
        df_to_sqlite(all_contractors_df[1], 'contractors')
    else:
        print(Fore.RED+f'\n{all_contractors_df[1]}\n'+Fore.RESET)
else:
    print(Fore.YELLOW + 'Будем использовать базу контрагентов загруженную ранее...' + Fore.RESET)        

if not db_exists or DOWNLOAD_GOODS_ON_START:
    all_goods_df = get_all_goods()

    if all_goods_df[0]:
        df_to_sqlite(all_goods_df[1], 'goods')
    else:
        print(Fore.RED+f'\n{all_goods_df[1]}\n'+Fore.RESET)
else:
    print(Fore.YELLOW + 'Будем использовать базу номенклатуры загруженную ранее...' + Fore.RESET)            