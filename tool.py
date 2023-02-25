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
    end_menu(downloader, main)
        
def xltool_func():
    print("")
    toolbox = xltool()
    toolbox.file_inp()
    toolbox.chk_sheet()
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
        
    options_dict = {
        "1": dupe,
        "2": rm_blnk,
    }    
    print("")    
    blue("    [1] Remove duplicates")
    blue("    [2] Remove blank rows")
    red("    [x] exit")
    print("")
    print_ln()
    main_menu(options_dict)
            
    print("")
    print_ln()
    green(' [1] Back to Xltools ')
    green(' [0] Back to Tools ')
    red(" [x] exit ")
    print("")
    print_ln()
    print("")
    
    end_menu(xltool_func, main)

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
    main_menu(options_dict, banner_dict=banner_dict)

###################################################

if __name__ == "__main__":
    
    main()