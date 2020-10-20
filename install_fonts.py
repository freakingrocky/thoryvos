from fontTools.ttLib import TTFont
import os


def install():
    try:
        for font in os.listdir('fonts'):
            print(font)
            Font = TTFont(os.path.join('fonts', font))
            Font.save('C:\\Windows\\Fonts')
    except:
        pass


if __name__ == '__main__':
    install()
