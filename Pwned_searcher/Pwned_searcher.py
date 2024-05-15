#<---  Pwned searcher | Database searcher by Adapters  --->
#<---                  python 3.x                      --->
#<---      Only for educationnal / good purposes       --->

import os
import time
import subprocess
import json
from colorama import Fore, init

def start_solr(ram_choice):
    # Démarrer Solr en arrière-plan
    subprocess.Popen([f'{os.getcwd()}/app/bin/solr', 'start', '-m', f'{ram_choice}g'], shell=True)
    time.sleep(10)

def main():
    #colorama setup
    w = Fore.LIGHTWHITE_EX
    y = Fore.LIGHTYELLOW_EX
    g = Fore.LIGHTGREEN_EX
    r = Fore.LIGHTRED_EX

    #retieve json params
    with open('utils/pwned_config.json', 'r', encoding='utf-8') as config:
        params = json.load(config)

    # show banner
    os.system('cls')
    print((y + """██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║
██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║
██║     ╚███╔███╔╝██║ ╚████║███████╗██████╔╝
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝""" + y + """ by Adapters""" + w).replace('█', w + '█' + y))
    print(f"""\n{y}[{w}+{y}]{w} Menu:              |    {y}[{w}INFO{y}]{w} Current Settings:            
                       |
{y}[{w}1{y}]{w} Start              |    {y}[{w}>{y}]{w} Allocated ram: {params['allowed-ram'] + 'go' if params['allowed-ram']  != '' else 'Undefined'}
{y}[{w}2{y}]{w} Change setup       |    {y}[{w}>{y}]{w} Undef: .
{y}[{w}3{y}]{w} Exit               |    {y}[{w}>{y}]{w} Undef: .""")      
    
    #Choices system
    general_choice = input(f"\n{w}[{g}+{w}] Enter your choice here: ")
    if general_choice == '1':
        if params['allowed-ram'] != '':
            print('-----')
            start_solr(params['allowed-ram'])
        else:
            os.system('cls')
            input(f'{w}[{r}+{w}] Please allocate ram !')
            main()
    elif general_choice == '2':
        os.system('cls')
        ram_choice = input(f'{w}[{g}+{w}] Enter the amount of ram to be allocated (in GO not MO): ')
        params['allowed-ram'] = ram_choice
        with open('utils/pwned_config.json', 'w', encoding='utf-8') as config:
            json.dump(params, config)
        main()
    elif general_choice == '3':
        exit()
    else:
        os.system('cls')
        input(f'{w}[{r}+{w}] Invalid choice !')
        main()

if __name__ == '__main__':
    os.system('title Pwned searcher')
    main()
    os.system(f'python app/app.py')
