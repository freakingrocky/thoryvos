import os

for font in os.listdir("fonts"):
    pyFont.font.add_file(os.path.join(os.getcwd(), "fonts", font))
