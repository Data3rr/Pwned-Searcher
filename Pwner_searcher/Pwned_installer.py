import os
import jdk
import sys
import winreg
import ctypes
import zipfile
import shutil
import urllib.request
from colorama import Fore, init


# Run as admin
def run_as_admin(func):
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


# Install java
def java_installer(output_path):
    try:
        jdk.install('17', vendor='Corretto', path=output_path)
        return True
    except Exception as e:
        return e


# JAVA_HOME env
def java_home(pwned_path):
    try:
        # Create dir
        if not os.path.exists(pwned_path + '\\app'):
            os.makedirs(pwned_path + '\\app')
        else: pass

        # Fix pwned_path
        if not ':' in pwned_path:
            pwned_path = os.path.join(os.getcwd() + '\\' + pwned_path)
        else: pass

        # Detect Java
        java_path = []
        for root, dirs, files in os.walk(pwned_path + '\\app'):
            for name in dirs:
                if 'jdk' in name:
                    java_path.append(os.path.join(root, name))
                    break
        try:
            os.environ['JAVA_HOME'] # Detect key
        except KeyError:
            # Create key
            reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(reg_key, 'JAVA_HOME', 0, winreg.REG_SZ, java_path[0])
            winreg.CloseKey(reg_key)
        return True
    except Exception as e:
        return e


# Install Solr
def install_solr(pwned_path):
    try:
        # Main var
        solr_path = []
        solr_url = "https://www.apache.org/dyn/closer.lua/lucene/solr/8.11.3/solr-8.11.3.zip?action=download"
        
        # Donwload + unzip
        solr_zip_file, _ = urllib.request.urlretrieve(solr_url)
        with zipfile.ZipFile(solr_zip_file, 'r') as zip_ref:
            zip_ref.extractall(path=pwned_path + '\\app', pwd=os.fsencode(pwned_path + '\\app'))
        
        # Extract folder content
        for root, dirs, files in os.walk(pwned_path + '\\app'):
            for name in dirs:
                if 'solr-' in name:
                    solr_path.append(os.path.join(root, name))
                    break
        for item in os.listdir(solr_path[0]):
            source = os.path.join(solr_path[0], item)
            destination = os.path.join(pwned_path + '\\app', item)
            shutil.move(source, destination)
        os.rmdir(solr_path[0])
        return True
    
    except Exception as e: 
        return e


def reorganization(pwned_path, w, y, g, r):
    try:
        # Import solr config
        shutil.copytree(os.getcwd() + '\\Pwned_data\\searcher', pwned_path + '\\app\\server\\solr\\searcher')
        print(f'{y}[{w}+{y}]{w} Solr config: ok')
        
        # Import webapp
        for item in os.listdir(os.getcwd() + '\\Pwned_data\\app_content'):
            try:
                shutil.copy(os.getcwd() + '\\Pwned_data\\app_content\\' + item, pwned_path + '\\app\\' + item)
            except:
                shutil.copytree(os.getcwd() + '\\Pwned_data\\app_content\\' + item, pwned_path + '\\app\\' + item)
        print(f'{y}[{w}+{y}]{w} Webapp: ok')

        # Import parser 
        shutil.copytree(os.getcwd() + '\\Pwned_data\\parser', pwned_path + '\\parser')
        print(f'{y}[{w}+{y}]{w} Parser: ok')

        # Push python main & parser
        shutil.copy(os.getcwd() + '\\Pwned_data\\Pwned_searcher.py', pwned_path + '\\Pwned_searcher.py')
        print(f'{y}[{w}+{y}]{w} Start file: ok')
        return True
    except Exception as e:
        return e

    
def menu(): 
    #colorama setup
    w = Fore.LIGHTWHITE_EX
    y = Fore.LIGHTYELLOW_EX
    g = Fore.LIGHTGREEN_EX
    r = Fore.LIGHTRED_EX
    init()

    # Banner & style
    os.system('cls')
    os.system('title Pwned installer')
    print((y + """██████╗ ██╗    ██╗███╗   ██╗███████╗██████╗ 
██╔══██╗██║    ██║████╗  ██║██╔════╝██╔══██╗
██████╔╝██║ █╗ ██║██╔██╗ ██║█████╗  ██║  ██║
██╔═══╝ ██║███╗██║██║╚██╗██║██╔══╝  ██║  ██║
██║     ╚███╔███╔╝██║ ╚████║███████╗██████╔╝
╚═╝      ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝╚═════╝""" + y + """ by Adapters""" + w).replace('█', w + '█' + y))
    pwned_path = input(f"""\n{y}[{w}+{y}]{w} Enter your installation path here: """)              
    
    # Create dir if not exists
    if not os.path.exists(pwned_path):
        os.makedirs(pwned_path)

    # Install Java 
    print(f'-----\n{y}[{w}+{y}]{w} Java installation...')
    java = java_installer(pwned_path + '\\app')
    if java != True:
        print(f"{r}[{w}!{r}]{w} Error while downloading Java ({java})")
    else: print(f'{g}[{w}+{g}]{w} Java downloaded succesfully !')

    # Create JAVA_HOME environnement variable
    print(f"-----\n{y}[{w}+{y}]{w} Creating the JAVA_HOME environment variable...")
    java_var = java_home(pwned_path)
    if java_var != True:
        print(f"{r}[{w}!{r}]{w} Error while creating JAVA_HOME ({java_var})")
    else: print(f'{g}[{w}+{g}]{w} Variable created succesfully !')
    
    # Download solr source
    print(f"-----\n{y}[{w}+{y}]{w} Solr installation...")
    solr_source = install_solr(pwned_path)
    if solr_source != True:
        print(f"{r}[{w}!{r}]{w} Error while downloading Solr ({solr_source})")
    else: print(f'{g}[{w}+{g}]{w} Solr downloaded succesfully !')

    # Reorganisation
    print(f"-----\n{y}[{w}+{y}]{w} Reorganization...")
    reorg = reorganization(pwned_path, w, y, g, r)
    if reorg != True:
        print(f"{r}[{w}!{r}]{w} Error while reoganization ({reorg})")
    else: print(f'{g}[{w}+{g}]{w} Reorganization ended succesfully !')

    input(f'-----\n{y}[{w}+{y}]{w} Installation finished !\n   {y}>{w} Pwned path: {pwned_path}')
   


if __name__ == "__main__":
    if not ctypes.windll.shell32.IsUserAnAdmin():
        run_as_admin(sys.argv[0])
    else:
        menu()
