from fbs_runtime.application_context import ApplicationContext, cached_property
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import os
#sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import kitty

def update(pixmap, label):
    img = kitty.fetchCat()
    pixmap.convertFromImage(img)
    label.setPixmap(pixmap)

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
        button = QPushButton('I wan\'t more!')
        button.clicked.connect(lambda: update(pixmap, label))
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button)
        layout.setAlignment(button, Qt.AlignHCenter)
        self.setLayout(layout)
        update(pixmap, label)
    def closeEvent(self, event):
        exit()

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
