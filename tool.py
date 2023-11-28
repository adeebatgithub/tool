###################################################
# TOOLS
# Author      : Adeeb
# Version     : 2.0
# Description : some usefull tools
###################################################

from pyfiglet import figlet_format

from Xltool import xltool
from Youtuber import YouTuber
from util import locio, color


class banners:

    def tool_bnr():
        head = figlet_format("TOOLS".center(31))

        locio.clear()
        locio.print_ln()
        locio.print_ln()
        print("")
        print(f"{color.red}{head}{color.noc}")
        locio.print_ln()
        print("  version : 2.0", end="")
        print("By : Adeeb".rjust(39))
        locio.print_ln()
        print("")

    def youtuber_bnr():
        txt = figlet_format("YOUTUBER".center(16))

        locio.clear()
        locio.print_ln()
        locio.print_ln()
        print(f"{color.red}{txt}{color.noc}")
        locio.print_ln()
        locio.print_ln()
        print()

    def xltool_bnr():
        txt = figlet_format("XLTOOLS".center(24))
        locio.clear()
        locio.print_ln()
        locio.print_ln()
        print("")
        locio.red(f"{txt}")
        locio.print_ln()
        locio.print_ln()
        print()


class tool(banners, YouTuber, xltool):

    def __init__(self):

        YouTuber.__init__(self)
        xltool.__init__(self)

        banners.tool_bnr()

    def downloader(self):

        banners.youtuber_bnr()

        url = locio.input_c("URL: ")

        locio.green("checking url...")
        is_url = YouTuber.check_url(url)
        if is_url:
            YouTuber.get_video(self, url)
        else:
            locio.print_er("not a youtube url")
            quit()

        tags = YouTuber.get_res(self)

        print(f"{color.yellow}Available resolution : ", *tags)

        res = locio.input_c("Resolution: ")
        tag = tags[res]

        print(f"Downloading: {YouTuber.get_title(self)}")
        YouTuber.download(self, tag)
        print("\ndownloaded")

    def xl(self):

        banners.xltool_bnr()

        path = locio.input_c("path or file name: ")

        if len(path) == 0:
            quit()

        xltool.file_inp(self, path)

        xltool.get_sheet_name(self)

        sheet = locio.input_c("sheet name: ")

        xltool.sheet_inp(self, sheet)

        print()
        print(" [1] search")
        print(" [x] exit")
        print()
        inp = locio.input_c(" select: ")

        if inp == "x":
            quit()

        options = {
            "1": xltool.find,
        }
        if inp in options:

            options[inp](self)

        else:

            locio.print_er("Option not found")

    def __call__(self):

        print(" [1] youtube video downloader")
        print(" [2] excel tools")
        print(" [x] exit")
        print()
        inp = locio.input_c(" select: ")

        options = {
            "x": quit,
            "1": self.downloader,
            "2": self.xl
        }
        if inp in options:

            options[inp]()

        else:

            locio.print_er("Option not found")


###################################################

if __name__ == "__main__":
    toolbox = tool()
    toolbox()
