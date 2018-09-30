import os
import sys
import time
import platform
import tempfile
import requests
from PyQt5.QtGui import QImage

# Fetch link
def fetchCat():
    #urlString = "http://thecatapi.com/api/images/get?"
    #urlString += "format=xml"
    #urlString += "&results_per_page=10"
    #urlString += "&type=gif"
    urlString = "https://cataas.com/cat"
    cat_response = ""

    # Get image
    content = ""
    try:
        content = requests.get(urlString).content
    except Exception as e:
        print("ERROR: The API on URL " + urlString + " is not answering!")
        print(e.message)
        return QImage()

    try:
        f, fname = tempfile.mkstemp()
        os.write(f, content)
        os.close(f)
        img = QImage(fname)
        os.remove(fname)
        return img
    except Exception as e:
        print(e.message)
        return QImage()
