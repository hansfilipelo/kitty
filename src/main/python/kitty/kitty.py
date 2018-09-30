import os
import sys
import time
import platform
import requests
from PyQt5.QtGui import QImage

# Fetch link
def fetchCat(qimage, errorMsg):
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
