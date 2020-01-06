# Youtube video download using Termux  
Download any youtube video in mp3 or mp4 format using your android phone.  

1). Install Termux in your phone.    
  
2). Run storage mount command in terminal.  
     >> termux-setup-storage  
       
3). Install git and python command.  
     >> pkg install git  
     >> pkg install python
       
4). Go to storage and download git repo.  
    >> cd storage/music   
    >> git clone https://github.com/t1819/youtube_downloader_termux.git  
    
5). Run setup.py file first time to configure your termux.   
    >> python setup.py

6). Run youtube_downloader.py file and enjoy downloading.  
    >> python youtube_downloader.py -h (for help)  
    >> python youtube_downloader.py -l http://youtube.com/4kdo -t audit

  

# Disclaimer  
Downloading copyright songs may be illegal in your country. This tool is for educational purposes only. We are not resposible of any legal issues or damages.
