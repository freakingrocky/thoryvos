""" Python 3 Windows font installer

Script must be run with the privileges in order to access Windows fonts directory. System reboot is not necessary.
This will install the font and will inform programs that a new font has been added.

Python3 Windows font installer is a free python script: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See COPYING for a copy of the GNU General Public License.
If not, see <http://www.gnu.org/licenses/>.

Copyright (C) 2017  Lahiru Pathirage <lpsandaruwan@gmail.com> 20/02/17
"""
"""
I've just configure the above package to install all the fonts in the fonts directory.
All credits for the script go to Lahiru Pathirage.
"""
import ctypes
import os
import shutil
import sys

from ctypes import wintypes

try:
    import winreg
except ImportError:
    import _winreg as winreg

user32 = ctypes.WinDLL('user32', use_last_error=True)
gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)

FONTS_REG_PATH = r'Software\Microsoft\Windows NT\CurrentVersion\Fonts'

HWND_BROADCAST = 0xFFFF
SMTO_ABORTIFHUNG = 0x0002
WM_FONTCHANGE = 0x001D
GFRI_DESCRIPTION = 1
GFRI_ISTRUETYPE = 3

if not hasattr(wintypes, 'LPDWORD'):
    wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

user32.SendMessageTimeoutW.restype = wintypes.LPVOID
user32.SendMessageTimeoutW.argtypes = (
    wintypes.HWND,   # hWnd
    wintypes.UINT,   # Msg
    wintypes.LPVOID,  # wParam
    wintypes.LPVOID,  # lParam
    wintypes.UINT,   # fuFlags
    wintypes.UINT,   # uTimeout
    wintypes.LPVOID  # lpdwResult
)

gdi32.AddFontResourceW.argtypes = (
    wintypes.LPCWSTR,)  # lpszFilename

# http://www.undocprint.org/winspool/getfontresourceinfo
gdi32.GetFontResourceInfoW.argtypes = (
    wintypes.LPCWSTR,  # lpszFilename
    wintypes.LPDWORD,  # cbBuffer
    wintypes.LPVOID,  # lpBuffer
    wintypes.DWORD)   # dwQueryType


def install_font(src_path):
    # copy the font to the Windows Fonts folder
    dst_path = os.path.join(
        os.environ['SystemRoot'], 'Fonts', os.path.basename(src_path)
    )
    shutil.copy(src_path, dst_path)

    # load the font in the current session
    if not gdi32.AddFontResourceW(dst_path):
        os.remove(dst_path)
        raise WindowsError('AddFontResource failed to load "%s"' % src_path)

    # notify running programs
    user32.SendMessageTimeoutW(
        HWND_BROADCAST, WM_FONTCHANGE, 0, 0, SMTO_ABORTIFHUNG, 1000, None
    )

    # store the fontname/filename in the registry
    filename = os.path.basename(dst_path)
    fontname = os.path.splitext(filename)[0]

    # try to get the font's real name
    cb = wintypes.DWORD()
    if gdi32.GetFontResourceInfoW(
            filename, ctypes.byref(cb), None, GFRI_DESCRIPTION
    ):
        buf = (ctypes.c_wchar * cb.value)()
        if gdi32.GetFontResourceInfoW(
                filename, ctypes.byref(cb), buf, GFRI_DESCRIPTION
        ):
            fontname = buf.value

    is_truetype = wintypes.BOOL()
    cb.value = ctypes.sizeof(is_truetype)
    gdi32.GetFontResourceInfoW(
        filename, ctypes.byref(cb), ctypes.byref(is_truetype), GFRI_ISTRUETYPE
    )

    if is_truetype:
        fontname += ' (TrueType)'

    with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, FONTS_REG_PATH, 0, winreg.KEY_SET_VALUE
    ) as key:
        winreg.SetValueEx(key, fontname, 0, winreg.REG_SZ, filename)


def installer(font):
    if font.endswith('.otf') or font.endswith('.ttf'):
        print('Installing ' + font)
        try:
            install_font(font)
            print(f"Font '{font}' installed successfully.")
        except PermissionError:
            print(f'You must run this script as administrator.')
        except:
            print(f"Failed to '{font}'install font. Please install it manually.")


if __name__ == '__main__':
    for font in os.listdir('tmp'):
        installer(os.path.join(os.getcwd(), 'tmp', font))
