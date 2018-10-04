import os
import sys
import requests
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
import pathlib
import threading
import queue
import time

urlKey = "url"
maxImagesKey = "maxImages"
minImagesKey = "minImages"
defaultSettings = {
        "url": "https://cataas.com/cat",
        "maxImages": 5,
        "minImages": 3
        }

def getConfigPath(configFile):
    configFolder = ""
    if os.name is not 'nt':
        configFolder = os.path.join(os.path.expanduser("~"), ".config", "KittY")
    else :
        configFolder = os.path.join(os.getenv('APPDATA'), "KittY")

    if not os.path.isdir(configFolder):
        pathlib.Path(configFolder).mkdir(parents=True, exist_ok=True)

    return os.path.join(configFolder, configFile)

# Read config
def getSettings(defaultSettings):
    configFile = getConfigPath("config.json")
    settings = dict()

    if not os.path.isfile(configFile):
        settings = defaultSettings
    else :
        fp = open(configFile, "r")
        settings = json.load(fp)
        for setting, value in defaultSettings.items():
            if setting not in settings:
                settings[setting] = value
    return settings

# Fetch link
def fetchCat(url, qimage, errorMsg):
    cat_response = ""

    # Get image
    content = ""
    try:
        content = requests.get(url).content
    except Exception as e:
        print("ERROR: The API on URL " + url + " is not answering!")
        print(e)
        errorMsg = e
        return False

    try:
        qimage.loadFromData(content)
        return True
    except Exception as e:
        print(e)
        errorMsg = e
    return False

class Kitty(threading.Thread):
    def __init__(self, qwidget):
        super().__init__(daemon=True)
        self._settings = getSettings(defaultSettings)
        self._url = self._settings[urlKey]
        self._maxImages = self._settings[maxImagesKey]
        self._minImages = self._settings[minImagesKey]

        self._cv = threading.Condition()
        self._queue = []

        # Setup the qwidget
        self._qwidget = qwidget
        self._label = QLabel()
        self._label.setWordWrap(True)
        self._pixmap = QPixmap()

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._label)
        self._layout.setAlignment(self._label, Qt.AlignHCenter)
        qwidget.setLayout(self._layout)

        qwidget.mousePressEvent=lambda event : self.updateMouse(self._pixmap, self._label, qwidget, self._url)
        qwidget.keyPressEvent=lambda event : self.updateKeyboard(self._pixmap, self._label, qwidget, event, self._url)

    def run(self):
        while True:
            self._cv.acquire()
            while len(self._queue) >= self._maxImages :
                self._cv.wait()
            self._cv.release()

            qimage = QImage()
            errorMsg = ""
            if fetchCat(self._url, qimage, errorMsg):
                self._cv.acquire()
                self._queue.append(qimage)
                self._cv.notify_all()
                self._cv.release()
            else :
                print(errorMsg)

    def loadImage(self):
        self._cv.acquire()
        while len(self._queue) == 0 :
            self._cv.wait()
        qimage = self._queue[0]
        qimage = self._queue.pop(0)

        if len(self._queue) < self._minImages :
            self._cv.notify_all()
        return qimage

    def update(self):
        self.updateMouse(self._pixmap, self._label, self._qwidget, self._url)

    def updateMouse(self, pixmap, label, widget, url):
        pixmap.convertFromImage(self.loadImage())
        label.setPixmap(pixmap)
        widget.resize(pixmap.width(), pixmap.height())

    def updateKeyboard(self, pixmap, label, widget, event, url):
        if event :
            if event.key() != Qt.Key_Escape :
                self.updateMouse(pixmap, label, widget, url)
            else :
                sys.exit(0)
        else :
            update(pixmap, label, widget, url)
