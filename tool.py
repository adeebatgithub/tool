###################################################
# TOOLS
# Author      : Adeeb
# Version     : 1.0
# Description : some usefull tools
###################################################

import os
from bfa import *
from Youtuber import YTD
from xltools import xltool

def downloader():
    print()
    ytd_obj = YTD()
    print()
    aud = yn_trufls("Download audio only")
    check_exit(aud)
    ytd_obj.download(aud)
    
    green(' [1] Download again ')
    green(' [0] Back to Tools')
    print("")
    print_ln()
    print("")
    
    menu({"1":downloader,"0":main})
        
def xltool_func():
    print("")
    toolbox = xltool()
    toolbox.file_inp()
    toolbox.sheet_inp()
    def dupe():
        print("")
        print_ln()
        print("")
        toolbox.dupe_tool()
            
    def rm_blnk():
        print("")
        print_ln()
        print("")
        toolbox.rm_blnk()
        
    def search():
        print()
        print_ln()
        print()
        toolbox.search()
    
    def main_menu():    
        main_options_dict = {
            "1": dupe,
            "2": rm_blnk,
            "3": search,
        }
        print("")    
        blue("    [1] Remove duplicates")
        blue("    [2] Remove blank rows")
        blue("    [3] Search ")
        red("    [x] exit")
        print("")
        print_ln()
        menu(main_options_dict)
    
    def end_menu():
        end_options_dict = {
            "1": main_menu,
            "2": xltool_func,
            "0": main,
        }
        print("")
        print_ln()
        green(' [1] Back ')
        green(' [2] Back to Xltools ')
        green(' [0] Back to Tools ')
        red(" [x] exit ")
        print("")
        print_ln()
        print("")
        menu(end_options_dict)
        end_menu()
        
    main_menu()
    end_menu()

def main():
    main_banner()

    blue(f'    [1] Youtube video downloader')
    blue(f'    [2] Xltools')
    red(f'    [x] Exit ')
    print("")
    print_ln()
    options_dict = {
        "1": downloader,
        "2": xltool_func,
    }
    banner_dict = {
        "1": yt_banner,
        "2": xltool_banner,
    }
    menu(options_dict, banner_dict=banner_dict)

###################################################

if __name__ == "__main__":
    
    main()