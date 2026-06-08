import subprocess
import os
print(os.path.join(os.getcwd(), 'Контрагенты.xlsx'))
print(os.path.exists(os.path.join(os.getcwd(), 'Контрагенты.xlsx')))
subprocess.run(['open', os.path.join(os.getcwd(), 'Контрагенты.xlsx')]) 