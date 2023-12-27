import os
import sys


class Color:
    noc = "\033[0m"
    red = "\033[1;31m"
    green = "\033[1;32m"
    yellow = "\033[1;33m"
    blue = "\033[1;34m"
    white = "\033[1;37m"


class LocIO:

    @staticmethod
    def print_ln():

        print(f"{Color.yellow}={Color.noc}" * 56)

    @staticmethod
    def print_dln():

        print(f"{Color.yellow}-{Color.noc}" * 56)

    @staticmethod
    def print_er(e: str):

        print(f"{Color.red}[!] Error : {e} {Color.noc}")

    @staticmethod
    def red(txt: str):

        print(f"{Color.red}{txt} {Color.noc}")

    @staticmethod
    def green(txt: str):

        print(f"{Color.green}{txt} {Color.noc}")

    @staticmethod
    def yellow(txt: str):

        print(f"{Color.yellow}{txt} {Color.noc}")

    @staticmethod
    def blue(txt: str):

        print(f"{Color.blue}{txt} {Color.noc}")

    @staticmethod
    def input_c(txt: str):

        try:
            inp = input(f"{Color.green}{txt}{Color.noc}")
        except KeyboardInterrupt:
            print()
            quit()

        return inp

    @staticmethod
    def clear():

        if sys.platform == "linux":
            os.system("clear")
        if "win" in sys.platform:
            os.system("cls")
