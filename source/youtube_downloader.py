import subprocess
import sys

try:
    import socks
    import socket
    import os
    import requests
    import argparse
    import re
    from art import *
except (RuntimeError, IOError):
    if os.path.exists('python3_requirements.txt'):
        print('Installing dependencies...')
        cmd = 'pip3 install -r "python3_requirements.txt"'
        subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        import socks
        import socket
        import os
        import requests
        import argparse
        import re
        from art import *
    else:
        print('[-] Error to import dependencies. Please try to manually install dependencies from requirement file.')
        sys.exit(1)


class YoutubeDownloader:
    """
    Download YouTube video as mp3 or mp4.
    """
    @staticmethod
    def proxy_setup(ip, port):
        """
        Tor proxy setup using this func.
        :param ip: proxy server ip address.
        :param port: proxy server port number.
        :return True or False
        """
        try:
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, ip, int(port))
            socket.socket = socks.socksocket
        except Exception as e:
            print(e)
            return False
        return True

    def youtube_url(self, url):
        """
        YouTube url read and convert it to long url.
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
        except Exception as e:
            print('[-]Error:'+str(e))
            return False
        return True

    def __init__(self):
        print(text2art('Youtube Downloader'))
        self.link = ''
        parser = argparse.ArgumentParser(description="""Install all the dependency before using this script.
            Python2 : "pip2 install -r python2_requirements.txt", Python3: "pip3 install -r python3_requirements.txt"
            and Install tor if you want to use proxy: "pkg install tor" 
            """)
        parser.add_argument('-l', help='Youtube link', dest='link')
        parser.add_argument('-t', help='Download type (audio/video)', dest='type')
        parser.add_argument('-f', help='Youtube link file location', dest='file')
        parser.add_argument('-proxy', help='if you want to use tor proxy then enter (yes/y). example -proxy y',
                            dest='proxy')
        parser.add_argument('-p', help='specific path for file download', dest='path')

        argv = parser.parse_args()

        download_option = ''
        ip = '127.0.0.1'
        port = 9050

        if argv.type == 'audio' or argv.type == 'mp3':
            download_option = "-i -x --audio-format mp3 -o '%(playlist)s/%(title)s.%(ext)s' "
        elif argv.type == 'video' or argv.type == 'mp4':
            download_option = "-i -f 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' " \
                              "-o '%(playlist)s/%(title)s.%(ext)s' "
        else:
            print('[-] Error in execution. Enter the right download type.')
            sys.exit(1)

        if (argv.link is not None or argv.file is not None) and argv.type is not None:
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
                    if argv.proxy is not None:
                        self.proxy_setup(ip, port)
                    old_path = os.getcwd()
                    for youtube_url in youtube_urls:
                        self.youtube_url(youtube_url)
                        command = 'youtube-dl {0} {1}'.format(download_option, self.link)
                        os.chdir(download_folder)
                        os.system(command)
                        os.chdir(old_path)
                else:
                    print('[-] Error in reading of songs.txt file.')

            else:
                self.youtube_url(argv.link)
                youtube_url = self.link
                old_path = os.getcwd()
                if argv.proxy is not None:
                    self.proxy_setup(ip, port)

                command = 'youtube-dl {0} {1}'.format(download_option, youtube_url)
                os.chdir(download_folder)
                os.system(command)
                os.chdir(old_path)
        else:
            print("\n[-] Error. You haven't enter the right options. You should add type and youtube link or "
                  "file path for run this script. Please read -h or --help option description for "
                  "more information.\n")


YoutubeDownloader()
