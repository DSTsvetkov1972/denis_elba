from package import init_project
from colorama import Fore
from datetime import datetime

if datetime.now()>datetime(2026, 5, 7):
    print(Fore.RED, 'Что-то пошло не так...', Fore.RESET)
    while True:
        continue
        
while True:


    try:
        print(Fore.WHITE + '1' + Fore.BLUE + ' - подготовить файл загрузки' + Fore.RESET)
        print(Fore.WHITE + '2' + Fore.BLUE + ' - загрузить' + Fore.RESET)                    

        print(Fore.MAGENTA + "Ваш выбор: " + Fore.RESET, end='')
        choise = input()



        if choise == '1':
            print(Fore.YELLOW + 'Подготавливаем файл загрузки...' + Fore.RESET)

            if True:
                print(Fore.WHITE + '1' + Fore.BLUE + ' - подготовить файл загрузки' + Fore.RESET)
                print(Fore.WHITE + '2' + Fore.BLUE + ' - загрузить' + Fore.RESET)                    

                print(Fore.MAGENTA + "Ваш выбор: " + Fore.RESET, end='')
                choise = input()

                elif choise == '2':
                    print(Fore.YELLOW + 'Создаём накладные в Эльбе1...' + Fore.RESET)                
    

    except Exception as e:
        print(Fore.RED, str(e), Fore.RESET)






















# print(folders_rules_dict['Согаз_изменение объёма'])

   

  


#
##if __name__ == '__main__':
#    folder = 'Согаз_изменение объёма'
#    file = 'Согаз изменение объема пример.xls'
#    file_processor_res = file_processor(folder, file)
#    print(file_processor_res)



