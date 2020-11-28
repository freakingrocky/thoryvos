from .UI_Functions import *
from .thoryvos import *
from .thoryvos_cli import parse_cl
import sys


def gui():
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())


def main():
    if len(sys.argv) == 1:
        gui()
    else:
        parse_cl()

if __name__ == "__main__":
    main()
