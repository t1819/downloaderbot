import socks
import socket
import requests
import argparse
import sys
import os
from art import *


class YoutubeDownloader:
    @staticmethod
    def proxy_setup(server_ip, port_number):
        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, server_ip, int(port_number))
        req1 = requests.get('http://api.ipify.org/?format=text')
        print('Your real ip is {0}'.format(req1.text))
        socket.socket = socks.socksocket

    def __init__(self):
        print(text2art('Youtube Downloader'))
        parser = argparse.ArgumentParser(description="""Install all the dependency before using this script.
            Python2 : "pip2 install -r python2_requirements.txt", Python3: "pip3 install -r python3_requirements.txt"
            and Install tor if you want to use proxy: "apt-get install tor" 
            """)
        parser.add_argument('-l', help='Youtube link', dest='link')
        parser.add_argument('-t', help='Download type', dest='type')
        parser.add_argument('-f', help='Youtube link file location', dest='file')
        parser.add_argument('-proxy', help='if you want to use tor proxy then enter (yes/y). example -proxy y',
                            dest='proxy')
        parser.add_argument('-s', help='proxy server ip', dest='ip')
        parser.add_argument('-p', help='proxy server port number', dest='port')
        parser.add_argument('-c', help='customized Youtube-dl commands', dest='commands')

        argv = parser.parse_args()

        download_option = ''

        if argv.type == 'audio':
            download_option = "-x --audio-format mp3"
        elif argv.type == 'video':
            download_option = "-f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'"
        # else:
        #     print('[-] Error. enter the right option')
        #     input()
        #     sys.exit(1)

        if argv.commands is not None:
            download_option = download_option+" '"+argv.commands+"' "

        if argv.commands is None:
            if (argv.link is not None or argv.file is not None) and argv.type is not None:
                if argv.type is not None:
                    download_folder = 'Download/{0}'.format(argv.type)
                else:
                    print('Please enter the type of file you want to download')
                    input()
                    sys.exit(1)

                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)

                if argv.file is not None:
                    usr_input = argv.file
                    if not os.path.exists(usr_input):
                        open(usr_input, 'w').close()
                        print('[-]Error File not found {0}'.format(os.path.join(os.getcwd(), argv.f)))
                        input()
                        sys.exit(1)

                    if os.path.exists(usr_input) or os.stat(usr_input).st_size == 0:
                        youtube_urls = open(usr_input, 'r').read().split('\n')
                        if argv.proxy is not None and argv.ip is not None and argv.port is not None:
                            self.proxy_setup(argv.ip, argv.port)
                        old_path = os.getcwd()
                        for youtube_url in youtube_urls:
                            if argv.proxy is not None:
                                req2 = requests.get('http://api.ipify.org/?format=text')
                                print('Your proxy ip is {0}'.format(req2.text))

                            cmd = 'youtube-dl {0} {1}'.format(download_option, youtube_url)
                            os.chdir(download_folder)
                            os.system(cmd)
                            os.chdir(old_path)
                    else:
                        print('[-] Error in reading of songs.txt file.')

                else:
                    youtube_url = argv.link
                    old_path = os.getcwd()
                    if argv.proxy is not None and argv.ip is not None and argv.port is not None:
                        self.proxy_setup(argv.ip, argv.port)
                        req2 = requests.get('http://api.ipify.org/?format=text')
                        print('Your proxy ip is {0}'.format(req2.text))

                    cmd = 'youtube-dl {0} {1}'.format(download_option, youtube_url)
                    os.chdir(download_folder)
                    os.system(cmd)
                    os.chdir(old_path)
            else:
                print("\n[-] Error. You haven't enter the right options. You should add type and youtube link or "
                      "file path for run this script. Please read -h or --help option description for "
                      "more information.\n")
        else:
            cmd = 'youtube-dl {0} {1}'.format(argv.commands, argv.link)
            download_folder = 'Download'
            old_path = os.getcwd()
            os.chdir(download_folder)
            os.system(cmd)
            os.chdir(old_path)


YoutubeDownloader()
