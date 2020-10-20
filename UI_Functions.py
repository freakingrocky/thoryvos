from thoryvos import *

class UIFunctions(MainWindow):
    def toggleMenu(self, maxWidth, enable):
        if not enable:
            return
        # Get Current Width
        Width = self.ui.LeftMenu.width()
        default = 80

        # Switch b/w open & close
        if Width == default:
            NewWidth = maxWidth
        else:
            NewWidth = default

        # Animation
        self.animation = QPropertyAnimation(self.ui.LeftMenu,
                                            b"minimumWidth")
        self.animation.setDuration(500)  # Animation Duration (in ms)
        self.animation.setStartValue(Width)
        self.animation.setEndValue(NewWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
