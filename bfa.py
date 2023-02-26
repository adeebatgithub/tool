import os
import sys

from pyfiglet import figlet_format

class color:
    
    noc = "\033[0m"
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    white = "\033[1;37m"

def print_ln():
    print(f"{color.yellow}={color.noc}"*56)
def print_dln():
    print(f"{color.yellow}-{color.noc}"*56)
def print_er(e):
    print(f"{color.red}[!] Error : {e} {color.noc}")
def red(txt):
    print(f"{color.red}{txt} {color.noc}")
def green(txt):
    print(f"{color.green}{txt} {color.noc}")
def yellow(txt):
    print(f"{color.yellow}{txt} {color.noc}")
def blue(txt):
    print(f"{color.blue}{txt} {color.noc}")
def input_c(txt):
    try:
        inp = input(f"{color.green}{txt}{color.noc}")
    except KeyboardInterrupt:
        print()
        quit()
    return inp

#################################################

def check_exit(var):
    if var in ["x"]:
        quit()

def clear():
    if sys.platform == "linux":
        os.system("clear")
    if sys.platform == "win32":
        os.system("cls")
        
def yn_trufls(txt):
    
    inp = input_c(f"[?] {txt} (y/n) : ")
    if inp == "y":
        return True
    if inp == "n":
        return False
    if len(inp) == 0:
        return False
    else:
        red(f"[!] option not found : '{inp}'")
        yn_trufls(txt)
        
def get_file_name(path):
    if "/" in path:
        return path.split("/")[-1]
    return path
        
def menu(options_dict, banner_dict=0):
    
    inp = input_c("[=] Select : ")
    check_exit(inp)
    try:
        if banner_dict != 0:
            banner_dict[inp]()
        options_dict[inp]()
    except KeyError:
        red(f"[!] option not found : '{inp}'")
        menu(options_dict, banner_dict)

#####################################

def main_banner():
    head = figlet_format("            TOOLS ")

    clear()
    print_ln()
    print_ln()
    print("")
    print(f"{color.red}{head}{color.noc}")
    print_ln()
    print(f"  version : 1.0                             By : Adeeb")
    print_ln()
    print("")

def yt_banner():
    
    clear()
    print_ln()
    print_ln()
    print(f"{color.red}{figlet_format('    YOUTUBER ')}{color.noc}")
    print_ln()
    print_ln()
    
def motd():
    
    txt = figlet_format("         TERMUX")
    clear()
    if sys.platform == "linux":
        print(txt)
    print("")

def xltool_banner():
    
    txt = figlet_format("        XLTOOLS")
    clear()
    print_ln()
    print_ln()
    print("")
    red(f"{txt}")
    print_ln()
    print_ln()

###################################################

def help_xltools():
    
    txt = '''
 Usage : xltools.py -wb [FILE_NAME] -s [SHEET_NAME] [OPTIONS]

 OPTIONS AND PARAM
-------------------------------------------

 -wb/ --workbook [WORKBOOK]    : set workbook
 -s/ --sheet [WORKSHEET]       : set worksheet
 --tool                        : 
 -dupe/ --duplicate            : find duplicates
 --rm-dupe/ --remove-duplicate : remove duplicates
 -rm-blank/ --remove-blank     : remove blank rows
 -p/ --print [MODE]            : print sheet
   --> MODES                   : json, table, list

-------------------------------------------
 tip :- use print option at last
'''
    print(txt)

def yt_hlp():
    hlp_txt = '''
 Usage : Youtuber.py -u [URL] [OPTIONS]

 OPTIONS
-------------------------------------

  -u   : set url
  -aud : download audio only
  -res : set download resolution

-------------------------------------

'''
    print(hlp_txt)

###################################################

class Error(Exception):
    pass
