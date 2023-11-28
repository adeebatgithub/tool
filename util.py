import os
import sys


class color:
    noc = "\033[0m"
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    white = "\033[1;37m"


class locio:

    def print_ln():

        print(f"{color.yellow}={color.noc}" * 56)

    def print_dln():

        print(f"{color.yellow}-{color.noc}" * 56)

    def print_er(e: str):

        print(f"{color.red}[!] Error : {e} {color.noc}")

    def red(txt: str):

        print(f"{color.red}{txt} {color.noc}")

    def green(txt: str):

        print(f"{color.green}{txt} {color.noc}")

    def yellow(txt: str):

        print(f"{color.yellow}{txt} {color.noc}")

    def blue(txt: str):

        print(f"{color.blue}{txt} {color.noc}")

    def input_c(txt: str):

        try:
            inp = input(f"{color.green}{txt}{color.noc}")
        except KeyboardInterrupt:
            print()
            quit()

        return inp

    def clear():

        if sys.platform == "linux":
            os.system("clear")
        if "win" in sys.platform:
            os.system("cls")
