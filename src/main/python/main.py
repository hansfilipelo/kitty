from fbs_runtime.application_context import ApplicationContext, cached_property
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QKeyEvent
import sys
# import os

#sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import kitty.kitty as kitty

def update(pixmap, label, widget):
    qimage = QImage()
    errorMsg = ""
    if kitty.fetchCat(qimage, errorMsg):
        pixmap.convertFromImage(qimage)
        label.setPixmap(pixmap)
        widget.resize(pixmap.width(), pixmap.height())
    else :
        if (errorMsg):
            label.setText("Failed: " + errorMsg)
        else :
            label.setText("Failed to fetch image!")

def updateKeyboard(pixmap, label, widget, event):
    if event.key() != Qt.Key_Escape :
        update(pixmap, label, widget)
    else :
        sys.exit(0)

class AppContext(ApplicationContext):
    def run(self):
        stylesheet = self.get_resource('style.qss')
        self.app.setStyleSheet(open(stylesheet).read())
        self.window.show()
        return self.app.exec_()
    @cached_property
    def window(self):
        return MainWindow()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        label = QLabel()
        label.setWordWrap(True)
        pixmap = QPixmap()

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.setAlignment(label, Qt.AlignHCenter)
        self.setLayout(layout)
        self.mousePressEvent=lambda event : update(pixmap, label, self)
        self.keyPressEvent=lambda event : updateKeyboard(pixmap, label, self, event)

        update(pixmap, label, self)

    def closeEvent(self, event):
        sys.exit(0)

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
