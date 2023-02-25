from pytube import YouTube as yt
import sys
from bfa import *
from os.path import exists

class YTD:

    def __init__(self):

        self.video = ""
        self.stream = ""
        self.tags = {}
        self.path = self.get_path()

    def available_res(self, aud):
        self.tags = {}
        filtered_stream = self.stream.filter(
            progressive = True,
        ).order_by('resolution')
        if aud:
            for stream in self.stream:
                if stream.type == 'audio':
                    self.tags[stream.abr] = stream.itag
        else:
            for stream in filtered_stream:
                if stream.type == 'video':
                    self.tags[stream.resolution] = stream.itag

    def display_progress_bar(
            self, bytes_received, filesize, ch: str = "█", scale: float = 0.55
    ):

        columns = 35
        max_width = int(columns * scale)

        filled = int(round(max_width * bytes_received / float(filesize)))
        remaining = max_width - filled
        progress_bar = ch * filled + " " * remaining
        percent = round(100.0 * bytes_received / float(filesize), 1)
        text = f" downloading: |{progress_bar}| {percent}% | {round((bytes_received / 1024) / 1024, 2)} MiB\t\r"
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

    def download(
        self,aud=False, res=0, url=0
    ):

        self.url_inp(url=url)
        self.available_res(aud)

        if aud:
            res = max(self.tags.keys())
            file = "Audio"
        if not aud:
            file = "Video"
            if res == 0:
                res = self.res_inp()
        tag = self.tags[res]
        self.set_res = self.stream.get_by_itag(tag)
        file_name = self.chk_file_name()+"."+self.set_res.subtype
        print()
        print_ln()
        green(f"[+] {file} : {file_name}")
        print_ln()
        print()
        is_exists = self.chk_file_exists(file_name)
        if not is_exists:
            self.set_res.download(self.path)
            print("\n")
            print_ln()
            green(" [*] download to : Youtuber")
            print_ln()
            print()

    def get_path(self):
        if sys.platform == "linux":
            return '/storage/emulated/0/Youtuber'
        if "win" in sys.platform:
            return ""
            
    def chk_file_exists(self, name):
        
        path = self.path+"/"+name
        is_exists = exists(path)
        if is_exists:
            red("[!] Already downloaded")
            red(f"[*] At : {path}")
            print()
            return True
        else:
            return False 
            
    def chk_file_name(self):
        
        file_name = self.video.title.replace("|","").replace(".","").replace(":","").replace("'","").replace("#","")
        return file_name
            
    def res_inp(self):
        green(f"[*] Available Resolutions : {list(self.tags.keys())}")
        res = input_c('[+] Resolution : ')
        try:
            self.tags[res]
            return res
        except KeyError:
            print_er(f"Resolution not available  : '{res}'")
            self.res_inp()
        
    def url_inp(self, url=0):
    
        if url == 0:
            url = input_c("[+] URL : ")
            check_exit(url)
        count = 0
        print("")
        yellow("[*] checking URL...")
        if 'https://youtu.be/' in url:
            count = 1
        if "https://youtube.com/" in url:
            count = 1
    
        if count == 1:
            try:
                self.video = yt(
                    url,
                    on_progress_callback=self.on_progress
                )
                self.stream = self.video.streams
            except:
                count = 0
    
        if count == 0:
            red(f"[!] Not a youtube url or url is carrupted : '{url}' ")
            self.url_inp()

if __name__ == '__main__':

    if "-h" in sys.argv or len(sys.argv) == 1:
        yt_hlp()
        quit()
    if "-u" in sys.argv:
        url = sys.argv[sys.argv.index("-u")+1]
    elif "--url" in sys.argv:
        url = sys.argv[sys.argv.index("--url")+1]
    else:
        print_er("URL is not provided")
        quit()
    green(" [====== Youtuber ======]")
    print_ln()
    downloader = YTD()
    
    if len(sys.argv) == 3:
        aud = yn_trufls("Download audio only")
        downloader.download(aud=aud,url=url)
    if len(sys.argv) > 3:
        if "-aud" in sys.argv:
            aud = True
        if "-res" in sys.argv:
            res = sys.argv[sys.argv.index("-res")+1]
        downloader.download(aud=aud,res=res,url=url)