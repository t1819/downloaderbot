import os


def system_default():
    packages = ['curl', 'ffmpeg', 'tor', 'git']
    for i in packages:
        cmd = "pkg install {0} -y".format(i)
        os.system(cmd)
    os.system('termux-setup-storage')
    os.system('pip install -r python2_requirements.txt')


if __name__ == '__main__':
    print('Starting setup process...')
    system_default()
    print('\nProcess completed successfully')
