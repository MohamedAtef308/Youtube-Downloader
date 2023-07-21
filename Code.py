from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow,
                             QComboBox, QLabel, QHBoxLayout, QLineEdit)
from PyQt5.QtGui import QIcon, QColor, QPalette, QPixmap
from pytube import YouTube
from pythumb import Thumbnail
import os
import socket


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
        # print("deleting")
        os.remove("thumbnail.jpg")

    # standardize the thumbnail name
    os.rename(img_name + ".jpg", "thumbnail.jpg")
    # hide the thumbnail
    os.system("attrib +h " + "thumbnail.jpg")

    return False


def convert_video(conversion_url):
    # check for network connection
    try:
        socket.create_connection(("8.8.8.8", 53))
    except OSError:
        return False, False

    # get the YouTube object
    try:
        # make sure no error while converting
        conversion_result = YouTube(conversion_url)
        return conversion_result.streams, conversion_result.title

    # return none in case of error
    except Exception:
        return None, None


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


def download(download_streams, download_dict, download_format, download_quality, file_title):

    file_name = file_title.text().replace('|', '')

    # search for the wanted quality and type
    for stream in download_dict:
        # for debugging only
        # print(stream)

        if (stream["type"] == download_format) and (stream["quality"] == download_quality):
            # get the stream using the itag from the list of dictionaries
            to_download = download_streams.get_by_itag(stream["itag"])

            # print(to_download)

            # make the directory if it doesn't exist
            if not os.path.exists("Downloads"):
                os.mkdir("Downloads")

            # download the stream to the chosen path
            to_download.download("Downloads")

            # if the format wanted is mp3 then rename it
            if download_format == "audio" and os.path.exists(f"Downloads/{file_name}.webm"):
                if os.path.exists(f"Downloads/{file_name}.mp3"):
                    os.remove(f"Downloads/{file_name}.mp3")
                os.rename(f"Downloads/{file_name}.webm", f"Downloads/{file_name}.mp3")

            elif download_format == "audio" and os.path.exists(f"Downloads/{file_name}.mp4"):
                if os.path.exists(f"Downloads/{file_name}.mp3"):
                    os.remove(f"Downloads/{file_name}.mp3")
            os.rename(f"Downloads/{file_name}.mp4", f"Downloads/{file_name}.mp3")

            return True

    # return false in case of not finding the wanted settings
    return False


def get_button_style(font_color, background_color):
    button_style = f"""
                background-color: {background_color};
                border: 2px solid transparent;
                border-radius: 15px;
                font-size: 10pt;
                color: {font_color};
                font-weight: bold;
            """
    return button_style


light_blue = "#5f6993"
grey = "#2a2a2a"


def enter_button(button):
    if button.isEnabled():
        global light_blue, grey
        button.setStyleSheet(get_button_style(grey, light_blue))


def leave_button(button):
    if button.isEnabled():
        global light_blue, grey
        button.setStyleSheet(get_button_style(light_blue, grey))


def build_app():
    building_app = QApplication([])
    building_window = QMainWindow()

    # set the icon and window title
    building_window.setWindowTitle("Youtube Downloader")
    icon = QIcon("Icon.png")
    building_app.setWindowIcon(icon)
    building_window.setWindowIcon(icon)

    # set window place, size and background color
    building_window.setFixedSize(700, 300)
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(25, 25, 25))
    building_window.setPalette(palette)

    # instantiate the main widget
    main_widget = QWidget()
    text_button_layout = QHBoxLayout()
    buttons_row_layout = QHBoxLayout()
    input_layout = QVBoxLayout(main_widget)
    main_widget.setLayout(input_layout)

    # --------- styles ---------
    global light_blue, grey

    # url text input style
    text_input_style = """
            font-size: 10pt;
            padding-left: 10px;
            border-radius: 15px;
        """

    # combobox style
    quality_box_style = """
            QComboBox::drop-down { width: 0; }
            
            QComboBox {
            border-radius: 15px;
            border: 3px solid #5f6993;
            background-color: #2a2a2a;
            padding: 10px;
            color: #5f6993;
            font-weight: bold;
            font-size: 10pt;
            }
        """

    # create the first row of elements (text box, convert button)
    link_input = QLineEdit()
    link_input.setFixedSize(500, 41)
    link_input.setStyleSheet(text_input_style)
    link_input.setPlaceholderText("Youtube link here")
    convert_button = QPushButton("Convert")
    convert_button.setStyleSheet(get_button_style(light_blue, grey))
    convert_button.setFixedHeight(45)

    # put them in a horizontal layout
    text_button_layout.addWidget(link_input)
    text_button_layout.addWidget(convert_button)

    thumbnail_space = QLabel("")
    thumbnail_space.setFixedHeight(100)
    input_layout.addWidget(thumbnail_space)

    # add a title label and the horizontal layout to the vertical layout
    title_label = QLabel("")
    title_label.setStyleSheet("font-size: 12pt; font-weight: bold; color: #5f6993;")
    title_label.setFixedHeight(38)
    input_layout.addWidget(title_label)
    input_layout.addLayout(text_button_layout)

    # create the second row of elements (combo box, status label, download button)
    download_button = QPushButton("Download")
    download_button.setStyleSheet(get_button_style(light_blue, grey))
    download_button.setFixedSize(200, 45)
    status_label = QLabel("")
    status_label.setFixedHeight(45)
    quality_box = QComboBox()
    quality_box.setFixedHeight(45)
    quality_box.setStyleSheet(quality_box_style)

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

    return (building_app, building_window, link_input, convert_button,
            download_button, quality_box, status_label, title_label, thumbnail_space)


def conversion_start(text_field, status_msg, download_button, quality_list, title_label, thumbnail_space):
    # update status label
    status_msg.setStyleSheet("color: #ffce45; font-size: 12pt; font-weight: bold;")
    status_msg.setText("Converting...")
    status_msg.repaint()

    # get the url
    conversion_text = text_field.text()

    # to get access to the global variable instead of creating a new one and pass the streams to it
    global streams
    streams, vid_title = convert_video(conversion_text)

    # if the function couldn't process the URL
    if streams is None:
        status_msg.setStyleSheet("color: #6e0d25; font-size: 12pt; font-weight: bold;")
        status_msg.setText("Conversion Error!")
        status_msg.repaint()

        # disable downloading when an error happens
        download_button.setEnabled(False)
        quality_list.setEnabled(False)
        quality_list.clear()
        return

    # if there's no internet connection
    elif streams is False:
        status_msg.setStyleSheet("color: #6e0d25; font-size: 12pt; font-weight: bold;")
        status_msg.setText("Connection Error!")
        status_msg.repaint()

        # disable downloading when an error happens
        download_button.setEnabled(False)
        quality_list.setEnabled(False)
        quality_list.clear()
        return

    # to get access to the global variable instead of creating a new one and pass the streams dictionaries to it
    global streams_list
    streams_list = get_streams(streams)

    # if the function couldn't download the thumbnail
    if get_thumbnail(conversion_text) is None:
        status_msg.setStyleSheet("color: #6e0d25; font-size: 12pt; font-weight: bold;")
        status_msg.setText("URL Error!")
        status_msg.repaint()

        # disable downloading when an error happens
        download_button.setEnabled(False)
        quality_list.setEnabled(False)
        quality_list.clear()
        return

    # print("thumbnail done")

    # activate the download button and the combo box and clear it
    download_button.setEnabled(True)
    quality_list.setEnabled(True)
    quality_list.clear()

    # add elements to the combo box
    for stream_item in streams_list:
        quality_list.addItem(f"{stream_item['quality']} {stream_item['type']}")

    quality_list.update()
    download_button.update()

    # update the status label and title label
    status_msg.setStyleSheet("color: #306844; font-size: 12pt; font-weight: bold;")
    status_msg.setText("Conversion Done")
    status_msg.repaint()
    title_label.setStyleSheet("color: #306844; font-size: 12pt; font-weight: bold;")
    title_label.setText(vid_title)
    title_label.repaint()

    # update the thumbnail
    pic = QPixmap("thumbnail.jpg")
    thumbnail_space.setPixmap(pic)
    thumbnail_space.setScaledContents(True)
    thumbnail_space.repaint()


def download_start(download_streams, status_msg, quality_list, converted_streams_list, file_title):
    # update the status label
    status_msg.setStyleSheet("color: #ffce45; font-size: 12pt; font-weight: bold;")
    status_msg.setText("Downloading...")
    status_msg.repaint()

    # get the quality and type
    splitted_choice = quality_list.currentText().split()
    download_quality = splitted_choice[0]
    download_format = splitted_choice[1]

    # download the stream
    download(download_streams, converted_streams_list, download_format, download_quality, file_title)

    # update the status label
    status_msg.setStyleSheet("color: #306844; font-size: 12pt; font-weight: bold;")
    status_msg.setText("Done")
    status_msg.repaint()


# -------------------------- Building App --------------------------
app, window, url_input, convert_but, download_but, qlty_list, status, title, thumbnail = build_app()
streams = None
streams_list = None


window.show()

convert_but.clicked.connect(lambda: conversion_start(url_input, status, download_but, qlty_list, title, thumbnail))
download_but.clicked.connect(lambda: download_start(streams, status, qlty_list, streams_list, title))

download_but.enterEvent = lambda event: enter_button(download_but)
download_but.leaveEvent = lambda event: leave_button(download_but)

convert_but.enterEvent = lambda event: enter_button(convert_but)
convert_but.leaveEvent = lambda event: leave_button(convert_but)

app.exec_()
