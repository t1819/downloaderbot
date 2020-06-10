# -*- coding:utf-8 -*-
###
# --------------------------------------------------------------
# Modified Date: Thursday, 11th June 2020 12:21:05 am
# Modified By: Ritesh Singh
# --------------------------------------------------------------
###

import logging, logging.config
import subprocess
import sys
try:
    import socket
    import os
    import requests
    import argparse
    import re
    import socks
    from termcolor import colored
    from pyfiglet import Figlet
except ImportError:
    if os.path.exists('requirements.txt'):
        print('Installing dependencies...')
        cmd = 'pip install -r "downloaderbot/source/requirements.txt"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        import socket
        import socks
        import os
        import requests
        import argparse
        import re
        from termcolor import colored
        from pyfiglet import Figlet
    else:
        print('[-] Error to import dependencies. Please try to manually install dependencies '
              'from requirement file.')
        sys.exit(1)


class CDownloader:
    """
    Download any online video in your device.
    """
    def proxy_setup(self, ip, port):
        """
        Tor proxy setup using this func.
        :param ip: proxy server ip address.
        :param port: proxy server port number.
        :return True or False
        """
        try:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, int(port))
            socket.socket = socks.socksocket
        except:
            self.logger.error('proxy error', exc_info=True)
            return False
        return True

    def youtube_url(self, url):
        """
        YouTube url read and convert it into long url.
        :param url: Youtube short url.
        """
        try:
            if bool(re.search('youtu.be', url)):
                a = str(url).split('be/')[1]
                self.link = 'https://www.youtube.com/watch?v=' + ''.join(a)
            elif bool(re.search('m.youtube.com', url)):
                self.link = str(url).replace('m.youtube', 'youtube')
            else:
                self.link = url
        except:
            self.logger.error('issue in youtube_url', exc_info=True)
            return False
        return True
    
    def main(self):
        try:
            # ascii logo maker.
            fig = Figlet(font='graffiti')
            ascii_font = fig.renderText('Downloader Bot')
            print(ascii_font)
            fig = Figlet(font='digital')
            ascii_font = fig.renderText('Downloader Bot')
            print(ascii_font)

            self.link = ''
            parser = argparse.ArgumentParser(description="""pip install -r requirements.txt & 
            Install tor if you want to use proxy: pkg install tor""")

            # Configuring tool parameters.
            parser.add_argument('-l', help='Youtube link', dest='link')
            parser.add_argument('-t', help='Download type (audio/video)', dest='type')
            parser.add_argument('-f', help='Youtube link file location', dest='file')
            parser.add_argument('-proxy', help='if you want to use tor proxy then enter (yes/y). example -proxy y',
                                dest='proxy')
            parser.add_argument('-p', help='specific path for file download', dest='path')
            parser.add_argument('-c', help='costume commands', dest='command')

            custom_command = ''
            argv = parser.parse_args()
            ip = '127.0.0.1'
            port = 9050

            if (argv.link is not None or argv.file is not None) and argv.type is not None:
                if (argv.type == 'audio' or argv.type == 'mp3') and re.search('youtu', argv.link):
                    if argv.path is None:
                        download_option = "-i -x --audio-format mp3 -o '%(playlist)s/%(title)s.%(ext)s' "
                    else:
                        download_option = "-i -x --audio-format mp3 -o '%(title)s.%(ext)s'"
                elif (argv.type == 'video' or argv.type == 'mp4') and re.search('youtu', argv.link):
                    if argv.path is None:
                        download_option = "-i -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' " \
                                        "-o '%(playlist)s/%(title)s.%(ext)s' "
                    else:
                        download_option = "-i -x --audio-format mp3 -o '%(title)s.%(ext)s'"
                else:
                    download_option = ''

                if argv.command is not None:
                    custom_command = argv.command

                # Configuring download folder.
                if argv.type is not None:
                    if argv.path is not None:
                        download_folder = '/data/data/com.termux/files/home/storage/music/' \
                                        '{0}/{1}'.format(argv.type, argv.path)
                    else:
                        download_folder = '/data/data/com.termux/files/home/storage/music/{0}'.format(argv.type)
                else:
                    print('Please enter the type of file you want to download')
                    input()
                    sys.exit(1)

                # Creating download folder if not exists.
                if not os.path.exists(download_folder):
                    os.makedirs(download_folder)

                # Download from txt file.
                if argv.file is not None:
                    usr_input = argv.file
                    if not os.path.exists(usr_input):
                        open(usr_input, 'w').close()
                        print('[-]Error File not found {0}'.format(os.path.join(os.getcwd(), argv.f)))
                        input()
                        sys.exit(1)

                    if os.path.exists(usr_input) or os.stat(usr_input).st_size == 0:
                        youtube_urls = open(usr_input, 'r').read().split('\n')
                        if argv.proxy is not None:
                            self.proxy_setup(ip, port)
                        old_path = os.getcwd()
                        for youtube_url in youtube_urls:
                            self.youtube_url(youtube_url)
                            command = 'youtube-dl {0} {1} {2}'.format(custom_command, download_option, self.link)
                            os.chdir(download_folder)
                            os.system(command)
                            os.chdir(old_path)
                    else:
                        print('[-] Error in reading of songs.txt file.')

                else:
                    self.youtube_url(argv.link)
                    old_path = os.getcwd()
                    if argv.proxy is not None:
                        self.proxy_setup(ip, port)

                    command = 'youtube-dl {0} {1} {2}'.format(custom_command, download_option, self.link)
                    os.chdir(download_folder)
                    os.system(command)
                    os.chdir(old_path)
            else:
                print("\n[-] Error. You have not enter the right options. Please read -h or --help option description for "
                    "more information.\n")
        except:
            self.logger.error('issue in main function.', exc_info=True)

    def __init__(self):
        logging.config.fileConfig("log.ini")
        self.logger = logging.getLogger('sLogger')
        

CDownloader().main()
