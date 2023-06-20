from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow,
                             QComboBox, QLabel, QHBoxLayout, QLineEdit)
from PyQt5.QtGui import QIcon, QColor, QPalette
from pytube import YouTube
from pythumb import Thumbnail
import os


def get_thumbnail(thumbnail_url):
    # get the thumbnail
    try:
        # but make sure the url is valid
        t = Thumbnail(thumbnail_url)

    # return none in case of error
    except Exception:
        return None

    t.fetch()
    t.save('.')

    # get the video ID
    img_name = thumbnail_url.split("watch?v=")[1]
    # video ID is 11 characters only (to remove the playlist and channel)
    img_name = img_name[:11]

    # delete the previous thumbnail
    if os.path.exists("thumbnail.jpg"):
        print("deleting")
        os.remove("thumbnail.jpg")

    # standardize the thumbnail name
    os.rename(img_name + ".jpg", "thumbnail.jpg")
    # hide the thumbnail
    os.system("attrib +h " + "thumbnail.jpg")

    return False


def convert_video(conversion_url):
    # get the YouTube object
    try:
        # make sure no error while converting
        conversion_streams = YouTube(conversion_url).streams
        return conversion_streams

    # return none in case of error
    except Exception:
        return None


def get_streams(streams_yt):
    # put the MP4 formats in a list
    stream_list = [
        {
            "itag": stream.itag,
            "quality": stream.resolution,
            "type": stream.type
        } for stream in streams_yt.filter(file_extension="mp4")
        if stream.resolution is not None
    ]

    # append the MP3 formats to the list
    stream_list.extend(
        [
            {
                "itag": stream.itag,
                "quality": stream.abr,
                "type": stream.type
            } for stream in streams_yt.filter(only_audio=True)
        ]
    )

    return stream_list


def download(download_streams, download_dict, download_format, download_quality, path="."):
    # search for the wanted quality and type
    for stream in download_dict:
        # for debugging only
        print(stream)

        if (stream["type"] == download_format) and (stream["quality"] == download_quality):
            # get the stream using the itag from the list of dictionaries
            to_download = download_streams.get_by_itag(stream["itag"])

            # for debugging only
            print(to_download)

            # download the stream to the chosen path
            to_download.download(path)
            return

    # return false in case of not finding the wanted settings
    return False


def build_app():
    building_app = QApplication([])
    building_window = QMainWindow()

    # set the icon and window title
    building_window.setWindowTitle("Youtube Downloader")
    icon = QIcon("Icon.png")
    building_app.setWindowIcon(icon)
    building_window.setWindowIcon(icon)

    # set window place, size and background color
    building_window.setGeometry(400, 300, 700, 450)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(25, 25, 25))
    building_window.setPalette(palette)

    # instantiate the main widget
    main_widget = QWidget()
    text_button_layout = QHBoxLayout()
    buttons_row_layout = QHBoxLayout()
    input_layout = QVBoxLayout(main_widget)
    main_widget.setLayout(input_layout)

    # create the first row of elements (text box, convert button)
    link_input = QLineEdit()
    convert_button = QPushButton("Convert")

    # put them in a horizontal layout
    text_button_layout.addWidget(link_input)
    text_button_layout.addWidget(convert_button)

    # add the horizontal layout to the vertical layout
    input_layout.addLayout(text_button_layout)

    # create the second row of elements (combo box, status label, download button)
    download_button = QPushButton("Download")
    status_label = QLabel("")
    quality_box = QComboBox()

    # make the download button inactive by default
    download_button.setEnabled(False)
    quality_box.setEnabled(False)

    # put them in a horizontal layout
    buttons_row_layout.addWidget(quality_box)
    buttons_row_layout.addWidget(status_label)
    buttons_row_layout.addWidget(download_button)

    # add the horizontal layout to the vertical layout
    input_layout.addLayout(buttons_row_layout)

    # put the widget at the center of the window
    building_window.setCentralWidget(main_widget)

    return building_app, building_window, link_input, convert_button, download_button, quality_box, status_label


def conversion_start(text_field, status_msg, download_button, quality_list):

    print("conv started")

    conversion_text = text_field.text()

    print(conversion_text)

    global streams
    streams = convert_video(conversion_text)

    if streams is None:
        print("conv error")
        # put the status = "Conversion Error"
        return

    print("converted")
    # put status = "Converted"

    # put streams into a dictionary
    global streams_list
    streams_list = get_streams(streams)

    if get_thumbnail(conversion_text) is None:
        print("url error")
        # put the status = "URL Error"
        return

    print("thumbnail done")

    download_button.setEnabled(True)
    quality_list.setEnabled(True)
    quality_list.clear()

    print("addition started")
    for stream_item in streams_list:
        quality_list.addItem(f"{stream_item['quality']} {stream_item['type']}")
        print(stream_item['quality'], stream_item['type'])


def download_start(download_streams, status_msg, quality_list, converted_streams_list):
    status_msg.setText("Downloading")
    splitted_choice = quality_list.currentText().split()
    download_quality = splitted_choice[0]
    download_format = splitted_choice[1]
    download(download_streams, converted_streams_list, download_format, download_quality)
    status_msg.setText("Done")
    pass
# -------------------------- debugging only --------------------------
# url = "https://www.youtube.com/watch?v=fHI8X4OXluQ&pp=ygUPYmxpbmRpbmcgbGlnaHRz"
# get_thumbnail(url)
# yt = convert_video(url)
# streams = get_streams(yt)
# download(yt, streams, "audio", "128kbps")


# -------------------------- Building App --------------------------

app, window, url_input, convert_but, download_but, qlty_list, status = build_app()
streams = None
streams_list = None

window.show()

convert_but.clicked.connect(lambda: conversion_start(url_input, status, download_but, qlty_list))
print("------------------------------------")
print(streams)
download_but.clicked.connect(lambda: download_start(streams, status, qlty_list, streams_list))

app.exec_()
