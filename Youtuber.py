###################################################
# YOUTUBER
# Author       : Adeebdanish
# version      : 1.0
# Description  : Youtube video downloader
###################################################

from pytube import YouTube as yt
import sys, os
from os.path import exists

from util import locio


class youtuber:
    
    def __init__(self):
        
        
        if sys.platform == "linux":
            
            self.path = "/storage/emulated/0/Youtuber/"
     
            r = exists(self.path)
            if not r:
                os.mkdir(self.path)
                
        if "win" in sys.platform:
            
            self.path = ""
            
    
    def display_progress_bar(
            self, bytes_received, filesize, ch: str = "█", scale: float = 0.55
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
        # print(text)

    def on_progress(
            self, stream, chunk, bytes_remaining
    ):

        self.file_size = self.set_res.filesize

        bytes_received = self.file_size - bytes_remaining
        self.display_progress_bar(
            bytes_received, self.file_size)
            
    def url_inp(self, url):
    
        count = 0
        if 'https://youtu.be/' in url:
            count = 1
        if "https://youtube.com/" in url:
            count = 1
    
        if count == 0:
            
            print(f"[!] Not a youtube url or url is carrupted : '{url}' ")
    
        else:
            
            try:
                print("[~] checking url...")
                self.video = yt(
                    url,
                    on_progress_callback=self.on_progress
                )
                self.stream = self.video.streams
            except:
                print("[!] something went wrong")
                
    def get_res(self, aud):
        
        tags = {}
        
        filtered_stream = self.stream.filter(
            progressive = True,
        ).order_by('resolution')
        
        if aud:
            
            for stream in self.stream:
                if stream.type == 'audio':
                    tags[stream.abr] = stream.itag
        
        else:
            
            for stream in filtered_stream:
                if stream.type == 'video':
                    tags[stream.resolution] = stream.itag
        
        return tags
                
    def get_file_name(self):
        
        file_name = self.video.title.replace("|","").replace(".","").replace(":","").replace("'","").replace("#","")
        return file_name
                
    def download(self, tag):
        
        self.set_res = self.stream.get_by_itag(tag)
        file_name = self.get_file_name()+"."+self.set_res.subtype
        print()
        locio.print_dln()
        print(f"[+] Video : {file_name}")
        locio.print_dln()
        print()
        self.set_res.download(self.path)
        if self.path == "":
            self.path = os.getcwd()
        locio.print_dln()
        print()
        print(f"\n[*] downloaded to : Youtuber")
        print()
                

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
    
    ytd = youtuber()
    
    argv = sys.argv
    
    if len(argv) < 2:
        
        yt_hlp()
        quit()
    
    if len(argv) == 2:
        
        if "-h" in argv:
            
            yt_hlp()
            quit()
    
    if "-u" in argv:
        
        url = argv[argv.index("-u")+1]
        
    else:
        
        print("[!] url not provided ")
        quit()
        
    ytd.url_inp(url)
    
    if "-aud" in argv:
        
        tags = ytd.get_res(True)
        print(tags)
        tag = tags[max(tags)]
    
    if "-r" in argv:
        
        res = argv[argv.index("-r")+1]
        tags = ytd.get_res(False)
        
        if res == "A":
        
            print("[~] Available resolution : ", *tags)
            quit()
            
        if res not in tags:
            
            print("[!] resolution not found")
            quit()
            
        tag = tags[res]
        
    else:
        
        if "-aud" not in argv:
            print("[!] resolution is not provided ")
            quit()
        
    ytd.download(tag)
        
        