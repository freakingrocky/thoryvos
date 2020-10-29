from UI_Functions import *
from thoryvos import *
from thoryvos_cli import parse_cl


def main():
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())


if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        parse_cl()
