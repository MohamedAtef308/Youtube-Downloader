from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from pytube import YouTube
from pythumb import Thumbnail
import os


def get_thumbnail(thumbnail_url):
    # get the thumbnail
    try:
        # but make sure the url is valid
        t = Thumbnail(thumbnail_url)

    # return false in case of error
    except Exception as e:
        return False

    t.fetch()
    t.save('.')

    # get the video ID
    img_name = thumbnail_url.split("watch?v=")[1]
    # video ID is 11 characters only (to remove the playlist and channel)
    img_name = img_name[:11]

    # delete the previous thumbnail
    if os.path.exists("thumbnail.jpg"):
        os.remove("thumbnail.jpg")

    # standardize the thumbnail name
    os.rename(img_name + ".jpg", "thumbnail.jpg")
    # hide the thumbnail
    os.system("attrib +h " + "thumbnail.jpg")


def convert_video(conversion_url):
    # get the YouTube object
    try:
        # make sure no error while converting
        conversion_yt = YouTube(conversion_url)
        return conversion_yt

    # return false in case of error
    except Exception as e:
        return False


def get_streams(streams_yt):
    # put the MP4 formats in a list
    stream_list = [
        {
            "itag": stream.itag,
            "quality": stream.resolution,
            "type": stream.type
        } for stream in streams_yt.streams.filter(file_extension="mp4")
        if stream.resolution is not None
    ]

    # append the MP3 formats to the list
    stream_list.extend(
        [
            {
                "itag": stream.itag,
                "quality": stream.abr,
                "type": stream.type
            } for stream in streams_yt.streams.filter(only_audio=True)
        ]
    )

    return stream_list


def download(download_yt, download_streams, download_format, download_quality, path="."):
    # search for the wanted quality and type
    for stream in download_streams:
        # for debugging only
        print(stream)

        if (stream["type"] == download_format) and (stream["quality"] == download_quality):
            # get the stream using the itag from the list of dictionaries
            to_download = download_yt.streams.get_by_itag(stream["itag"])

            # for debugging only
            print(to_download)

            # download the stream to the chosen path
            # to_download.download(path)
            return

    # return false in case of not finding the wanted settings
    return False


# -------------------------- debugging only --------------------------
# url = "https://www.youtube.com/watch?v=fHI8X4OXluQ&pp=ygUPYmxpbmRpbmcgbGlnaHRz"
# get_thumbnail(url)
# yt = convert_video(url)
# streams = get_streams(yt)
# download(yt, streams, "audio", "128kbps")

# app = QApplication([])
# window = QWidget()
#
# layout = QVBoxLayout()
#
# button1 = QPushButton("Button 1")
# layout.addWidget(button1)
#
# button2 = QPushButton("Button 2")
# layout.addWidget(button2)
#
# window.setLayout(layout)
# window.show()

# app.exec_()
