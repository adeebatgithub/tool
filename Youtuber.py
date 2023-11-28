###################################################
# YOUTUBER
# Author       : Adeebdanish
# version      : 1.0
# Description  : YouTube video downloader
###################################################

import os
import re
import sys
from os.path import exists

from pytube import YouTube

from util import locio


class YouTuber:
    aud = False

    def __init__(self):

        if sys.platform == "linux":

            self.path = "/storage/emulated/0/Youtuber/"

            r = exists(self.path)
            if not r:
                os.mkdir(self.path)

        if "win" in sys.platform:
            self.path = ""

    @staticmethod
    def display_progress_bar(
            bytes_received, filesize, ch: str = "█", scale: float = 0.55
    ):

        columns = 35
        max_width = int(columns * scale)

        filled = int(round(max_width * bytes_received / float(filesize)))
        remaining = max_width - filled
        progress_bar = ch * filled + " " * remaining
        percent = round(100.0 * bytes_received / float(filesize), 1)
        text = f"downloading: |{progress_bar}| {percent}% | {round((bytes_received / 1024) / 1024, 2)} MiB\t\r"
        sys.stdout.write(text)
        sys.stdout.flush()

    def on_progress(
            self, stream, chunk, bytes_remaining
    ):

        self.file_size = self.set_res.filesize

        bytes_received = self.file_size - bytes_remaining
        self.display_progress_bar(
            bytes_received, self.file_size)

    @staticmethod
    def check_url(url: str):

        youtube_pattern = (
            r"(https?://)?(www\.)?"
            "(youtube|youtu|youtube-nocookie)\.(com|be)/")
        youtube_regex = re.compile(youtube_pattern)
        match = youtube_regex.match(url)

        return bool(match)

    def get_video(self, url: str):

        self.video = YouTube(
            url,
            on_progress_callback=self.on_progress
        )
        self.streams = self.video.streams

    def get_res(self):

        tags = {}

        filtered_streams = self.streams.filter(
            progressive=True,
        ).order_by('resolution')

        if self.aud:
            tags = {stream.abr: stream.itag for stream in self.streams if stream.type == "audio"}

        else:
            tags = {stream.resolution: stream.itag for stream in filtered_streams if stream.type == "video"}

        return tags

    def get_file_name(self):

        file_name = self.video.title
        pattern = r'[^a-zA-Z0-9\s]'
        file_name = re.sub(pattern, '', file_name)

        return file_name

    def get_title(self):

        return self.video.title

    def download(self, tag):

        self.set_res = self.streams.get_by_itag(tag)
        file_name = self.get_file_name() + "." + self.set_res.subtype
        self.set_res.download(self.path)


def yt_hlp():
    hlp_txt = '''
 Usage : Youtuber.py -u [URL] -r [RESOLUTION] [OPTIONS]

 OPTIONS
-------------------------------------

  -u    : set url
  -aud  : download audio only
  -r    : set download resolution
        : A - Show available resolutions

-------------------------------------

'''
    print(hlp_txt)


if __name__ == "__main__":

    ytd = YouTuber()

    argv = sys.argv

    if len(argv) < 2:
        yt_hlp()
        quit()

    if len(argv) == 2:

        if "-h" in argv:
            yt_hlp()
            quit()
    if "-aud" in argv:
        ytd.aud = True

    if "-u" in argv:
        url = argv[argv.index("-u") + 1]

    else:
        locio.print_er("url not provided ")
        quit()
    print("[*] checking url...")
    is_url = ytd.check_url(url)
    if is_url:
        ytd.get_video(url)
    else:
        locio.print_er("not a youtube url")
        quit()

    tags = ytd.get_res()

    if "-r" in argv:

        res = argv[argv.index("-r") + 1]

        if res == "A":
            print("[~] Available resolution : ", *tags)
            quit()

        if res not in tags:
            locio.print_er("[!] resolution not found")
            quit()

        tag = tags[res]

    else:
        if "-aud" not in argv:
            locio.print_er("[!] resolution is not provided ")
            quit()

        tag = max(tags)

    print(f"[*] downloading: {ytd.get_title()}")
    ytd.download(tag)
    print("\n[*] downloaded")
