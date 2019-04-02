import os


def system_default():
    curl = 'pkg install curl'
    mpeg = 'pkg install ffmpeg'
    youtube_dl = 'pkg install youtube_dl'
    storage = 'termux-setup-storage'
    os.system(curl)
    os.system(mpeg)
    os.system(youtube_dl)
    os.system(storage)


def log_file_create(log_file):
    try:
        f = open(log_file, 'w')
        f.write('1')
        f.close()
    except:
        return False
    return True


def main():
    url = input('Please enter the url:\n')
    playlist_name = input('Please enter the playlist name:\n')
    quality = input('Please enter the quality:\n')
    log_file = '.log'
    if not os.path.exists(log_file):
	system_default()
        log_file_create(log_file)
    cur_dir = os.getcwd()
    if quality == 'mp4':
        download = 'youtube-dl --format mp4 --geo-bypass '+url
    elif quality == 'mp3':
        download = 'youtube-dl --extract-audio --audio-format mp3 '+url
    else:
        download = 'youtube-dl --extract-audio --audio-format mp3 '+url
    folder = '/data/data/com.termux/files/home/storage/music/'+playlist_name
    if not os.path.exists(folder):
        os.mkdir(folder)
    os.chdir(folder)
    os.system(download)
    os.chdir(cur_dir)


if __name__ == '__main__':
    main()
