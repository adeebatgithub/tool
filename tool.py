###################################################
# TOOLS
# Author      : Adeeb
# Version     : 2.0
# Description : some usefull tools
###################################################

from pyfiglet import figlet_format

from xltool import XlTool
from Youtuber import YouTuber
from util import LocIO, Color


class Banners:

    @staticmethod
    def tool_bnr():
        head = figlet_format("TOOLS".center(31))

        LocIO.clear()
        LocIO.print_ln()
        LocIO.print_ln()
        print("")
        print(f"{Color.red}{head}{Color.noc}")
        LocIO.print_ln()
        print("  version : 2.0", end="")
        print("By : Adeeb".rjust(39))
        LocIO.print_ln()
        print("")

    @staticmethod
    def youtuber_bnr():
        txt = figlet_format("YOUTUBER".center(16))

        LocIO.clear()
        LocIO.print_ln()
        LocIO.print_ln()
        print(f"{Color.red}{txt}{Color.noc}")
        LocIO.print_ln()
        LocIO.print_ln()
        print()

    @staticmethod
    def xltool_bnr():
        txt = figlet_format("XLTOOLS".center(24))
        LocIO.clear()
        LocIO.print_ln()
        LocIO.print_ln()
        print("")
        LocIO.red(f"{txt}")
        LocIO.print_ln()
        LocIO.print_ln()
        print()


class Tool:

    @staticmethod
    def downloader():

        Banners.youtuber_bnr()
        youtuber = YouTuber()

        url = LocIO.input_c("URL: ")

        LocIO.green("checking url...")
        is_url = youtuber.check_url(url)
        if is_url:
            youtuber.get_video(url)
        else:
            LocIO.print_er("not a youtube url")
            quit()

        tags = youtuber.get_res()

        print(f"{Color.yellow}Available resolution : ", *tags)

        res = LocIO.input_c("Resolution: ")
        tag = tags[res]

        print(f"Downloading: {youtuber.get_title()}")
        youtuber.download(tag)
        print("\ndownloaded")

    def xl(self):

        Banners.xltool_bnr()
        xltool = XlTool()

        path = LocIO.input_c("path or file name: ")

        if len(path) == 0:
            quit()

        xltool.file_inp(path)

        xltool.get_sheet_name()

        sheet = LocIO.input_c("sheet name: ")

        xltool.sheet_inp(sheet)

        print()
        print(" [1] search")
        print(" [x] exit")
        print()
        inp = LocIO.input_c(" select: ")

        if inp == "x":
            quit()

        options = {
            "1": xltool.find,
        }
        if inp in options:

            options[inp](self)

        else:

            LocIO.print_er("Option not found")

    def __call__(self):

        print(" [1] youtube video downloader")
        print(" [2] excel tools")
        print(" [x] exit")
        print()
        inp = LocIO.input_c(" select: ")

        options = {
            "x": quit,
            "1": self.downloader,
            "2": self.xl
        }
        if inp in options:

            options[inp]()

        else:

            LocIO.print_er("Option not found")


###################################################

if __name__ == "__main__":
    toolbox = Tool()
    toolbox()
