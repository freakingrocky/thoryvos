from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import os

class DragDropWidget(QWidget):
    dropped = Signal(str)
    clicked = Signal()
    def __init__(self, parent=None):
        super(DragDropWidget, self).__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            if len(event.mimeData().urls()) != 1:
                event.ignore()
            else:
                event.setDropAction(Qt.CopyAction)
                event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            if len(event.mimeData().urls()) != 1:
                event.ignore()
            else:
                url = event.mimeData().urls()[
                    0].toLocalFile()
                if os.path.exists(url):
                    self.dropped.emit(url)

        else:
            event.ignore()

    def mousePressEvent(self, event):
        self.clicked.emit()