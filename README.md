# YouTube Downloader

YouTube Downloader is a PyQt5-based desktop application that allows users to download YouTube videos in both MP4 and MP3 formats. The app is built using the PyTube library and packaged using PyInstaller.

## Used Languages and Packages
- **python 3**
- **pytube**
- **pyinstaller** (to package the script into an app)
<!-- end list -->

## Files
- **Code** (has the python script used to make the app)
- **icon** (used to change the program icon)
- **Bin** (has the packaged version of the script)
<!-- end list -->


## Usage
1. Enter the youtube url
2. Press Convert
3. Choose the wanted format and quality
4. Press Download
5. The wanted file will be inside the **Downloads** folder
<!-- end list -->

## Packaging

The YouTube Downloader app has been packaged using PyInstaller, which converts the [Python Script](https://github.com/MohamedAtef308/Youtube-Downloader/blob/main/Code.py) into a standalone executable file. To create a new executable file, run the following command:
**pyinstaller -F -noconsole Code.py**