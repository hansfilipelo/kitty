from fbs_runtime.application_context import ApplicationContext, cached_property
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
import sys

#sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import kitty.kitty as kitty

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
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._kitty = kitty.Kitty(self)
        self._kitty.start()
        self._kitty.update()

    def closeEvent(self, event):
        sys.exit(0)

if __name__ == '__main__':
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
