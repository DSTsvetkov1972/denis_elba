from package import init_project
from colorama import Fore
from datetime import datetime
from package.preparator import check_source_folder, download_file_preparator
from package.sqlite import df_to_sqlite
from package.api import get_all_contractors, get_all_goods
from package.invoices_maker import invoices_maker
from package.confirm_download import confirm
import os

if datetime.now()>datetime(2026, 6, 7):
    print(Fore.RED, 'Что-то пошло не так...', Fore.RESET)
    while True:
        continue
        
while True:

    try:
        n = 60
        print(Fore.BLUE + '-'*n + Fore.RESET)

        print(Fore.WHITE + '1' + Fore.BLUE + ' - подготовить файл для создания накладных' + Fore.RESET)
        print(Fore.WHITE + '2' + Fore.BLUE + ' - создать накладные' + Fore.RESET)
        print(Fore.WHITE + '3' + Fore.BLUE + ' - отправить файл в архив' + Fore.RESET)

        print(Fore.BLUE + '-'*n + Fore.RESET)

        print(Fore.WHITE + '4' + Fore.BLUE + ' - посмотреть контрагентов' + Fore.RESET)
        print(Fore.WHITE + '5' + Fore.BLUE + ' - посмотреть номенклатуру' + Fore.RESET)
        print(Fore.WHITE + '6' + Fore.BLUE + ' - обновить базу данных контрагентов и номенклатуры' + Fore.RESET)               

        print(Fore.MAGENTA + "Ваш выбор: " + Fore.RESET, end='')
        choise = input()

        if choise == '1':
            print(Fore.YELLOW + 'Подготавливаем файл для создания накладных...' + Fore.RESET)
            
            check_source_folder_res = check_source_folder()
            if check_source_folder_res[0]:
                source_file_name = check_source_folder_res[1]
                print(Fore.GREEN+f'В папке Исходник находится единственный файл "{source_file_name}" и он с расширением .xlsx'+Fore.RESET)
            else:
                os.startfile(os.path.join(os.getcwd(), 'Исходник'))
                print(Fore.RED+f'{check_source_folder_res[1]}\n'+Fore.RESET)
                continue
            
            if os.path.exists('~$Контрагенты.xlsx'):
                os.startfile('Контрагенты.xlsx')
                print(Fore.RESET+'Файл "Контрагенты.xlsx" должен быть закрыт\n'+Fore.RESET)
                continue
            if os.path.exists('~$Номенклатура.xlsx'):
                os.startfile('Номенклатура.xlsx')
                print(Fore.RED+'Файл "Номенклатура.xlsx" должен быть закрыт\n'+Fore.RESET)
                continue
            if os.path.exists('~$Для накладных.xlsx'):
                os.startfile('Для накладных.xlsx')
                print(Fore.RESET+'Файл "Для накладных.xlsx" должен быть закрыт\n'+Fore.RESET)
                continue
            
           
            download_file_preparator_res = download_file_preparator(source_file_name)
            if download_file_preparator_res[0]:
                print(Fore.GREEN+f'{download_file_preparator_res[1]}\n'+Fore.RESET)
            else:
                print(Fore.RED+f'{download_file_preparator_res[1]}\n'+Fore.RESET)

            os.startfile('Для накладных.xlsx')
            continue            


        elif choise == '2':
            print(Fore.YELLOW + 'Создаём накладные в Эльбе...' + Fore.RESET)
            invoices_maker_res = invoices_maker()
            if invoices_maker_res[0]:
                print(Fore.GREEN+f'{invoices_maker_res[1]}\n'+Fore.RESET)
            else:
                print(Fore.RED+f'{invoices_maker_res[1]}\n'+Fore.RESET)
            
        elif choise == '3':
            print(Fore.YELLOW + 'Переместить в архив...' + Fore.RESET)
            confirm_res = confirm()
            if confirm_res[0]:
                print(Fore.GREEN+f'{confirm_res[1]}\n'+Fore.RESET)
            else:
                print(Fore.RED+f'{confirm_res[1]}\n'+Fore.RESET)
            
        elif choise == '4':
            print(Fore.YELLOW + 'Открываем список контрагентов...' + Fore.RESET)
            os.startfile('Контрагенты.xlsx')
            
        elif choise == '5':
            print(Fore.YELLOW + 'Открываем номенклатуру...' + Fore.RESET)
            os.startfile('Номенклатура.xlsx')

        elif choise == '6':
            print(Fore.YELLOW + 'Обновляем базу данных контрагентов...' + Fore.RESET)

            all_contractors_df = get_all_contractors()

            if all_contractors_df[0]:
                df_to_sqlite(all_contractors_df[1], 'contractors')
            else:
                print(Fore.RED+f'\n{all_contractors_df[1]}\n'+Fore.RESET)

        elif choise == '7':
            print(Fore.YELLOW + 'Обновляем базу данных номенклатуры...' + Fore.RESET)

            all_goods_df = get_all_goods()

            if all_goods_df[0]:
                df_to_sqlite(all_goods_df[1], 'goods')
            else:
                print(Fore.RED+f'\n{all_goods_df[1]}\n'+Fore.RESET) 
        

    except Exception as e:
        print(Fore.RED, str(e), Fore.RESET)






















# print(folders_rules_dict['Согаз_изменение объёма'])

   

  


#
##if __name__ == '__main__':
#    folder = 'Согаз_изменение объёма'
#    file = 'Согаз изменение объема пример.xls'
#    file_processor_res = file_processor(folder, file)
#    print(file_processor_res)



