from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from pytube import YouTube
from pythumb import Thumbnail
import os

def get_photo(url):
    t = Thumbnail(url)
    t.fetch()
    t.save('.')

    imgName = url.split("watch?v=")[1]
    imgName = imgName[:11]

    if os.path.exists("thumbnail.jpg"):
        os.remove("thumbnail.jpg")

    os.rename(imgName + ".jpg", "thumbnail.jpg")

def convert_video(url):

    link = argv[1]
    yt = YouTube(link)

    print("Title: ", yt.title)
    print("Length: ", yt.length)

    yd = yt.streams.get_lowest_resolution()
    yd.download(".")



get_photo("https://www.youtube.com/watch?v=_FS28OdK9Mc&ab_channel=ReidCaptain")

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