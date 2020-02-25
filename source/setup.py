import os


def system_default():
    """
    Run this setup file first time and it will configure your termux for youtube_downloader app.
    """
    try:
        packages = ['curl', 'ffmpeg', 'tor', 'git', 'vim']
        for i in packages:
            cmd = "pkg install {0} -y".format(i)
            os.system(cmd)
        os.system('termux-setup-storage')
        os.system('pip install -r python3_requirements.txt')
        os.system("echo alias ydownloader='python /data/data/com.termux/files/home/youtube_downloader/"
                  "source/youtube_downloader.py' >> /data/data/com.termux/files/usr/etc/bash.bashrc")

    except (RuntimeError, IOError, FileExistsError) as r:
        print('[-]Error: ' + str(r))


if __name__ == '__main__':
    print('Starting setup process...')
    system_default()
    print('\nProcess completed successfully')
