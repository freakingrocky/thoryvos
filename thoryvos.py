# Importing Required Modules
import sys
import platform
from PySide2 import QtCore, QtWidgets, QtGui
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
import os
import fonts
from time import sleep

# GUI
from main_ui import Ui_MainWindow
from splash_screen_ui import Ui_SplashScreen

# Import UI Functions
from UI_Functions import *
from StyleSheets import *

# Importing thoryvos backend
import thoryvos_driver_gui as thoryvos
from thoryvos_errorcodes import *

# Definign Global Variables
Progress = 0
Infile = None
Datafile = None
Outfile = None
URL = None
ERRORCODES = range(1, 9)


class MainWindow(QMainWindow):
    """The main Window in the GUI Interface."""

    def __init__(self):
        """Configure the GUI interface."""
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.AppDesc.setText("Welcome...")

        self.fontDB = QFontDatabase()
        for font in os.listdir("fonts"):
            self.fontDB.addApplicationFont(f":/fonts/fonts/{font}")

        self.lsb = None
        self.nb = None

        # Toggle Menu Bar
        self.ui.ToggleMenu.clicked.connect(
            lambda: UIFunctions.toggleMenu(self, 180, True))
        QtCore.QTimer.singleShot(1500, lambda: self.ui.AppDesc.setText(
            "The all in one cryptographic toolkit"))

        # Left Menu Configuration
        self.ui.Home.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.HomePage))
        self.ui.Crypto.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.CryptoPage))
        self.ui.MarosMenuButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.MacroPage))
        self.ui.FileShare.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.TransferPage))
        self.ui.Stego.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.StegoPage))
        self.ui.Stego.clicked.connect(
            lambda: self.ui.StegoPage_2.setCurrentWidget(self.ui.StegoOptions))
        self.ui.MarosMenuButton.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.MacrosPage))
        self.ui.FileShare.clicked.connect(self.reset)
        self.ui.MarosMenuButton.clicked.connect(self.reset)
        self.ui.Home.clicked.connect(self.reset)
        self.ui.Crypto.clicked.connect(self.reset)
        self.ui.Stego.clicked.connect(self.reset)

        # Home Page Buttons Configuration
        self.ui.CryptoPageButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.CryptoPage))
        self.ui.MacroPageButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.MacroPage))
        self.ui.TransferPageButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.TransferPage))
        self.ui.StegoPageButton.clicked.connect(
            lambda: self.ui.Stack.setCurrentWidget(self.ui.StegoPage))
        self.ui.CryptoPageButton.clicked.connect(self.reset)
        self.ui.MacroPageButton.clicked.connect(self.reset)
        self.ui.TransferPageButton.clicked.connect(self.reset)
        self.ui.StegoPageButton.clicked.connect(self.reset)
        self.ui.StegoPageButton.clicked.connect(
            lambda: self.ui.StegoPage_2.setCurrentWidget(self.ui.StegoOptions))
        self.ui.MacroPageButton.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.MacrosPage))


        # Crypto Page Configuration
        self.ui.CryptoDragDrop.dropped.connect(self.crypto_add_file)
        self.ui.CryptoDragDrop.clicked.connect(self.crypto_add_dialog)

        self.ui.AlgoSelect.addItem("AES")
        self.ui.AlgoSelect.addItem("DES")
        self.ui.AlgoSelect.addItem("SALSA20")

        self.ui.CryptoSaveLocBrowse.clicked.connect(self.crypto_save_file)
        self.ui.Password.textChanged.connect(self.update_password)

        self.ui.Encrypt.clicked.connect(self.encrypt)
        self.ui.Decrypt.clicked.connect(self.decrypt)

        # Transfer Page
        self.ui.DragDropTransfer.dropped.connect(self.transfer_add_file)
        self.ui.DragDropTransfer.clicked.connect(self.transfer_file_dialog)

        self.ui.Url.textChanged.connect(self.update_transfer_label)

        self.ui.ButtonTransfer.clicked.connect(self.transfer)

        # Stego Page
        self.ui.HideButton.clicked.connect(
            lambda: self.ui.StegoPage_2.setCurrentWidget(self.ui.Hide))
        self.ui.HideButton.clicked.connect(self.reset)
        self.ui.RecoverButton.clicked.connect(
            lambda: self.ui.StegoPage_2.setCurrentWidget(self.ui.Recover))
        self.ui.RecoverButton.clicked.connect(self.reset)

        # Hide Page for Stego
        self.ui.InfileDragDrop.dropped.connect(self.stego_add_file)
        self.ui.InfileDragDrop.clicked.connect(self.stego_add_dialog)

        self.ui.DatafileDragDrop.dropped.connect(self.stego_add_datafile)
        self.ui.DatafileDragDrop.clicked.connect(self.stego_add_datadialog)

        self.ui.SaveLocBrowseStego.clicked.connect(self.stego_save_file)
        self.ui.lsb.textChanged.connect(self.update_lsb())
        self.ui.HideBtn.clicked.connect(self.hide)

        # Recover Page for Stego
        self.ui.InfileRedDragDrop.dropped.connect(self.stego_add_file)
        self.ui.InfileRedDragDrop.clicked.connect(self.stego_add_dialog)

        self.ui.OutfileRecBrowse.clicked.connect(self.stego_save_file_rec)
        self.ui.LSB.textChanged.connect(self.update_lsb_rec)
        self.ui.NBytes.textChanged.connect(self.update_nbytes)

        self.ui.RecButton.clicked.connect(self.recover)

        # Macros Page
        self.ui.EncSteg.clicked.connect(
            lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.EncryptStegoPage))
        self.ui.EncSteg.clicked.connect(self.reset)

        # EncSteg Page for Macros
        self.ui.MInfileDragDrop.dropped.connect(self.stego_add_file)
        self.ui.MInfileDragDrop.clicked.connect(self.stego_add_dialog)

        self.ui.MDatafileDragDrop.dropped.connect(self.stego_add_datafile)
        self.ui.MDatafileDragDrop.clicked.connect(self.stego_add_datadialog)

        self.ui.SaveLocationBrowse.clicked.connect(self.stego_save_file_rec)
        self.ui.LSBInput.textChanged.connect(self.update_lsb_cir)
        self.ui.NBytesInput.textChanged.connect(self.update_nbytes_cir)

        self.ui.Forward.clicked.connect(self.circuit_1)
        self.ui.Backward.clicked.connect(self.circuit_1_backward)

        self.show()

    def circuit_1_backward(self):
        """Macro Option 1 Backward Driver Code."""
        global Infile, Outfile

        password, start = QInputDialog.getText(self, "Password",
                                               "Enter Password:",
                                               QLineEdit.Password,
                                               flags=Qt.FramelessWindowHint)

        if not start:
            return

        steg = thoryvos.recover_data(Infile, "thoryvos_temp2217761.wav", self.lsb, int(self.nb))
        if steg in ERRORCODES:
            self.reset()
            self.ui.MInfileLabel.setStyleSheet("")
            self.ui.MInfileLabel.setText(Error[steg])
            os.remove("thoryvos_temp2217761.wav")
            return

        dec = thoryvos.decryptor("thoryvos_temp2217761.wav", Outfile, password, "AES")
        if dec in ERRORCODES:
            self.reset()
            self.ui.MInfileLabel.setStyleSheet("")
            self.ui.MInfileLabel.setText(f"{Error[dec]}")
            os.remove("thoryvos_temp2217761.wav")
            return

        self.reset()
        os.remove("thoryvos_temp2217761.wav")
        self.ui.MInfileLabel.setText("Circuit Succesfully Executed")

    def circuit_1(self):
        """Macro Option 1 Forward Driver Code."""
        global Infile, Outfile, Datafile

        password, start = QInputDialog.getText(self, "Password",
                                               "Enter Password:",
                                               QLineEdit.Password,
                                               flags=Qt.FramelessWindowHint)

        if not start:
            return

        enc = thoryvos.encryptor(Datafile, "thoryvos_temp2217761.wav", password, "AES")
        if enc in ERRORCODES:
            self.reset()
            self.ui.MInfileLabel.setStyleSheet("")
            self.ui.MInfileLabel.setText(f"{Error[enc]}")
            os.remove("thoryvos_temp2217761.wav")
            return

        steg = thoryvos.hide_data(
            Infile, Outfile, "thoryvos_temp2217761.wav", self.lsb)
        if steg in ERRORCODES:
            self.reset()
            self.ui.MInfileLabel.setStyleSheet("")
            self.ui.MInfileLabel.setText(f"{Error[steg]}")
            os.remove("thoryvos_temp2217761.wav")
            return

        self.reset()
        os.remove("thoryvos_temp2217761.wav")
        self.ui.MInfileLabel.setText("Circuit Succesfully Executed")
        self.ui.MDatafileLabel.setText(f"LSB: {steg[0]} \n NBytes: {steg[1]}")

    def recover(self):
        """Recover Driver Code."""
        global Infile, Outfile

        code = thoryvos.recover_data(Infile, Outfile, self.lsb, int(self.nb))
        self.reset()
        if code in ERRORCODES:
            self.ui.InfileRecLabel.setText(f"{Error[code]}")
        else:
            self.ui.InfileRecLabel.setText("Succesfully Recovered.")

    def update_lsb(self):
        """Update self.lsb according to lsb in the field."""
        lsb = self.ui.lsb.text()
        if lsb != "":
            self.lsb = lsb
        else:
            self.lsb = None

    def update_lsb_cir(self):
        """Update self.lsb according to lsb in the field."""
        lsb = self.ui.LSBInput.text()
        if lsb != "":
            self.lsb = lsb
        else:
            self.lsb = None
            self.ui.Backward.setEnabled(False)
            self.ui.Backward.setText("")

        if self.lsb is not None and self.nb is not None:
            self.ui.Backward.setEnabled(True)
            self.ui.Backward.setText("Backward Circuit [Rec -> Dec]")

    def update_lsb_rec(self):
        """Update self.lsb according to lsb in the field."""
        lsb = self.ui.LSB.text()
        if lsb != "":
            self.lsb = lsb
        else:
            self.lsb = None
            self.ui.RecButton.setEnabled(False)
            self.ui.RecButton.setText("")

        if self.lsb is not None and self.nb is not None:
            self.ui.RecButton.setEnabled(True)
            self.ui.RecButton.setText("Recover")

    def update_nbytes_cir(self):
        """Update self.nb according to nbytes in the field."""
        nb = self.ui.NBytesInput.text()
        if nb != "":
            self.nb = nb
        else:
            self.nb = None
            self.ui.Backward.setEnabled(False)
            self.ui.Backward.setText("")

        if self.lsb is not None and self.nb is not None:
            self.ui.Backward.setEnabled(True)
            self.ui.Backward.setText("Backward Circuit [Rec -> Dec]")

    def update_nbytes(self):
        """Update self.nb according to nbytes in the field."""
        nb = self.ui.NBytes.text()
        if nb != "":
            self.nb = nb
        else:
            self.nb = None
            self.ui.RecButton.setEnabled(False)
            self.ui.RecButton.setText("")

        if self.lsb is not None and self.nb is not None:
            self.ui.RecButton.setEnabled(True)
            self.ui.RecButton.setText("Recover")

    def hide(self):
        """Hiding Driver Code."""
        global Infile, Datafile, Outfile

        self.ui.InfileDragDropLabel.setText("Hiding...")


        lsb = self.lsb if self.lsb in range(1, 8) else None
        steg = thoryvos.hide_data(Infile, Outfile, Datafile, lsb)
        if steg in ERRORCODES:
            self.ui.InfileDragDropLabel.setText(Error[code])
            return

        self.ui.InfileDragDropLabel.setText("Hiding Complete")
        self.ui.DatafileDragDropLabel.setText(f"LSB -> {steg[0]}")
        self.ui.SaveLocBrowseStegoLabel.setText(f"No. of bytes hidden -> {steg[1]}")
        self.ui.lsb.setText(f"{steg}")

    def stego_add_datadialog(self):
        """Add data file dialog for Stagnography page."""
        file = QFileDialog.getOpenFileName(
            caption="Data File")[0]
        if not file:
            self.ui.DatafileDragDropLabel.setText("Invalid File.")
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.DatafileDragDropLabel.setText("Click To Browse Save Location"))
            self.reset()

        else:
            self.stego_add_datafile(file)

    def stego_save_file(self):
        """Get Save File location for steganography page."""
        global Outfile

        file = QFileDialog.getSaveFileName(
            caption="Save File", filter="*.wav")[0]

        if not file or not file.endswith(".wav"):
            self.ui.CryptoSaveLocBrowseL.setText("Invalid Save Filename.")
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.CryptoSaveLocBrowseL.setText("Drag & Drop/\
                                                                   \nClick To Add File"))
        else:
            Outfile = file
            Size = 15
            self.ui.lsb.setMaximumSize(QtCore.QSize(16777215, 35))
            self.ui.lsb.setEnabled(True)
            font = QFont()
            font.setFamily("Feast of Flesh BB")
            font.setPointSize(Size)
            font.setBold(True)
            font.setItalic(True)
            font.setWeight(75)
            self.ui.SaveLocBrowseStegoLabel.setFont(font)
            self.ui.SaveLocBrowseStegoLabel.setText("Save To: \n" +
                                                    os.path.basename(file))
            self.ui.SaveLocBrowseStegoLabel.setStyleSheet(DragDropLabelSS2)
            self.ui.HideBtn.setEnabled(True)
            self.ui.HideBtn.setText("Hide")

    def stego_save_file_rec(self):
        """Save File Location for Stagnography page."""
        global Outfile, Datafile

        file = QFileDialog.getSaveFileName(
            caption="Save File")[0]

        if not file:
            self.ui.OutfileRecLabel.setText("Invalid Save Filename.")
            self.ui.SaveLocationBrowseLabel.setText("Invalid Save Filename.")
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.OutfileRecLabel.setText("Click To Browse Save Location"))
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.SaveLocationBrowseLabel.setText("Click To Browse Save Location"))

        else:
            Outfile = file
            font = QFont()
            font.setFamily("Feast of Flesh BB")
            font.setPointSize(15)
            font.setBold(True)
            font.setItalic(True)
            font.setWeight(75)
            self.ui.OutfileRecLabel.setFont(font)
            self.ui.SaveLocationBrowseLabel.setFont(font)
            self.ui.OutfileRecLabel.setText("Save To: \n" +
                                            os.path.basename(file))
            self.ui.SaveLocationBrowseLabel.setText("Save To: \n" +
                                                    os.path.basename(file))
            self.ui.OutfileRecLabel.setStyleSheet(DragDropLabelSS2)
            self.ui.SaveLocationBrowseLabel.setStyleSheet(DragDropLabelSS2)
            self.ui.RecButton.setEnabled(True)
            self.ui.RecButton.setText("Recover")
            self.ui.LSBNB.setMinimumSize(QtCore.QSize(0, 72))
            self.ui.LSBNB.setMaximumSize(QtCore.QSize(16777215, 72))
            self.ui.LSBNbytes.setMinimumSize(QtCore.QSize(0, 60))
            self.ui.LSBNbytes.setMaximumSize(QtCore.QSize(16777215, 60))
            if Datafile:
                self.ui.Forward.setEnabled(True)
                self.ui.Forward.setText("Forward Circuit[Enc -> Hide]")


    def stego_add_datafile(self, file):
        """Add data file for Stagnography Page."""
        global Datafile, Outfile

        Size = 15
        Datafile = file
        if file is None:
            return
        self.ui.MDatafileLabel.setStyleSheet(DragDropLabelSS2)
        self.ui.DatafileDragDropLabel.setStyleSheet(DragDropLabelSS2)
        if len(file) > 105:
            file = file[:102] + '...'
        font = QFont()
        font.setFamily("Feast of Flesh BB")
        font.setPointSize(Size)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.ui.DatafileDragDropLabel.setFont(font)
        self.ui.MDatafileLabel.setFont(font)
        self.ui.DatafileDragDropLabel.setText("File Loaded:\n" +
                                            os.path.basename(file))
        self.ui.MDatafileLabel.setText("File Loaded:\n" +
                                       os.path.basename(file))
        self.ui.SaveLocBrowseStego.setEnabled(True)
        self.ui.SaveLocationBrowseLabel.setEnabled(True)
        self.ui.SaveLocBrowseStegoLabel.setEnabled(True)
        self.ui.SaveLocBrowseStegoLabel.setText(
            "Click To Browse Save Location")
        if Outfile:
            self.ui.Forward.setEnabled(True)
            self.ui.Forward.setText("Forward Circuit[Enc -> Hide]")

    def stego_add_dialog(self):
        """Open file dialog for stego page."""
        file = QFileDialog.getOpenFileName(
            caption="Audio File", filter="*.wav")[0]
        if not file.endswith('.wav'):
            file = None
        if not file:
            self.ui.InfileDragDropLabel.setText("Invalid Audio.")
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.InfileDragDropLabel.setText("Click To Browse Save Location"))
            self.reset()

        else:
            self.stego_add_file(file)

    def stego_add_file(self, file):
        """Add Input File for stego page."""
        global Infile

        Size = 15
        Infile = file
        if not file:
            self.ui.InfileDragDropLabel.setText("Invalid File.")
            self.ui.InfileRecLabel.setText("Invalid File.")
            self.ui.MInfileLabel.setText("Invalid File.")
            QtCore.QTimer.singleShot(
                8000, self.reset())
        self.ui.InfileDragDropLabel.setStyleSheet(DragDropLabelSS2)
        self.ui.InfileRecLabel.setStyleSheet(DragDropLabelSS2)
        self.ui.MInfileLabel.setStyleSheet(DragDropLabelSS2)
        if len(file) > 105:
            file = file[:102] + '...'
        font = QFont()
        font.setFamily("Feast of Flesh BB")
        font.setPointSize(Size)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.ui.MInfileLabel.setFont(font)
        self.ui.MInfileLabel.setText("File Loaded:\n" +
                                     os.path.basename(file))
        self.ui.MDatafileDragDrop.setEnabled(True)
        self.ui.InfileDragDropLabel.setFont(font)
        self.ui.InfileDragDropLabel.setText("File Loaded:\n" +
                                            os.path.basename(file))
        self.ui.InfileRecLabel.setFont(font)
        self.ui.InfileRecLabel.setText("File Loaded:\n" +
                                        os.path.basename(file))
        self.ui.DatafileDragDropLabel.setEnabled(True)
        self.ui.DatafileDragDrop.setEnabled(True)
        self.ui.DatafileDragDropLabel.setText(
            "(Data File)\nClick To Add/Drag & Drop Files")
        self.ui.OutfileRecLabel.setEnabled(True)
        self.ui.OutfileRecBrowse.setEnabled(True)
        self.ui.OutfileRecLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.OutfileRecLabel.setText("Click To Browse Save Location")
        self.ui.RecButton.setText("Browse Save Location First.")
        self.ui.DatafileDragDropLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.SaveLocBrowseStegoLabel.setText("Add Data File First")
        self.ui.SaveLocBrowseStegoLabel.setStyleSheet("")
        self.ui.MDatafileLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.MDatafileLabel.setText(
            "(Datafile)\nClick To Add/Drag&Drop Files")
        self.ui.SaveLocBrowseStegoLabel.setStyleSheet(
            DragDropLabelSS1)
        self.ui.SaveLocationBrowseLabel.setText(
            "Click To Browse Save Location")
        self.ui.SaveLocationBrowseLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.SaveLocationBrowse.setEnabled(True)

    def transfer(self):
        """Transfer Driver Code."""
        global URL, Infile

        if URL:
            self.ui.DragDropLabelTransfer.setText("Downloading...")

            location = thoryvos.anon_download(URL)
            self.ui.DragDropLabelTransfer.setStyleSheet(
                    DragDropLabelTransferSS2)
            if type(location) == int:
                self.reset()
                self.ui.DragDropLabelTransfer.setText(
                    f"{Error[location]}")
            else:
                self.reset()
                self.ui.DragDropLabelTransfer.setText(f"File Saved to: \n{location}")

        else:
            self.ui.DragDropLabelTransfer.setText("Uploading...")

            filename = thoryvos.anon_upload(Infile)
            if type(filename) == int:
                self.reset()
                self.ui.DragDropLabelTransfer.setText(
                    f"{Error[filename]}")
            else:
                self.reset()
                self.ui.DragDropLabelTransfer.setText(
                    f"Succesfully Uploaded")
                self.ui.Url.setText(filename)
                self.ui.Url.setEnabled(True)

    def transfer_add_file(self, file):
        """Add input file for transfer page."""
        global Infile

        Size = 14
        Infile = file
        self.ui.DragDropLabelTransfer.setStyleSheet(DragDropLabelSS2)
        if len(file) > 105:
            file = (file[:105] + '\n' + file[105:])
        if len(file) > 210:
            file = (file[:105] + '\n' + file[105:207] + '...')
        if len(file) < 80:
            Size = 25
        font = QtGui.QFont()
        font.setFamily("DEADLY KILLERS DEMO")
        font.setPointSize(Size)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ui.DragDropLabelTransfer.setFont(font)
        self.ui.DragDropLabelTransfer.setText("File Loaded:\n" +
                                              os.path.basename(file))
        self.ui.Url.setText("Click Transfer to get URL")
        self.ui.Url.setEnabled(False)
        self.ui.ButtonTransfer.setEnabled(True)
        self.ui.ButtonTransfer.setText("Transfer")

    def transfer_file_dialog(self):
        """Open File dialog for transfer page."""
        global Infile

        if not Infile:
            filename = QFileDialog.getOpenFileName(caption="Input File")
            if not filename[0]:
                self.ui.DragDropLabelTransfer.setText("Invalid File.")
                QtCore.QTimer.singleShot(
                    2000, lambda: self.ui.DragDropLabelTransfer.setText("Click To Add/\n"
                                                                      "Drag & Drop Files"))
            else:
                self.transfer_add_file(filename[0])

    def update_transfer_label(self):
        """Update transfer label according to the text."""
        global URL

        if Infile:
            return

        text = self.ui.Url.text()
        if thoryvos.verify(text):
            Size = 12
            self.ui.DragDropLabelTransfer.setStyleSheet(
                DragDropLabelTransferSS2)
            if len(text) > 87:
                text = (text[:87] + '\n' + text[87:])
            if len(text) > 174:
                text = (text[:174] + '\n' + text[174:258] + '...')
            if len(text) < 60:
                Size = 18
            URL = text
            font = QtGui.QFont()
            font.setFamily("Courgette")
            font.setPointSize(Size)
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(75)
            self.ui.DragDropLabelTransfer.setFont(font)
            self.ui.DragDropLabelTransfer.setText("Download From:\n" +
                                                  text)
            self.ui.ButtonTransfer.setEnabled(True)
            self.ui.ButtonTransfer.setText("Transfer")
        else:
            if not text:
                self.reset()
            else:
                font = QtGui.QFont()
                font.setFamily("Courgette")
                font.setPointSize(35)
                font.setBold(True)
                font.setItalic(False)
                font.setWeight(75)
                self.ui.DragDropLabelTransfer.setFont(font)
                self.ui.DragDropLabelTransfer.setText("Invalid URL.")
            self.ui.ButtonTransfer.setEnabled(False)
            self.ui.ButtonTransfer.setText("Add File/Url First")

    def decrypt(self):
        """Decryption Driver Code."""
        global Infile, Outfile
        self.ui.CryptoDragDropLabel.setText("Decrypting...")

        code = thoryvos.decryptor(Infile, Outfile, self.ui.Password.text(),
                                  self.ui.AlgoSelect.currentText())
        if code in ERRORCODES:
            self.ui.CryptoDragDropLabel.setText(Error[code])
        self.reset()
        self.ui.CryptoDragDropLabel.setText("Succesfully Decrypted")

    def encrypt(self):
        """Encryption Driver Code."""
        global Infile, Outfile
        self.ui.CryptoDragDropLabel.setText("Encrypting...")

        code = thoryvos.encryptor(Infile, Outfile, self.ui.Password.text(),
                                  self.ui.AlgoSelect.currentText())
        if code in ERRORCODES:
            self.ui.CryptoDragDropLabel.setText(Error[code])

        tmp = Outfile
        self.reset()
        self.ui.CryptoDragDropLabel.setText("Succesfully Encrypted")
        self.ui.CryptoSaveLocBrowseL.setText(f"File Saved as \n{tmp}")

    def update_password(self):
        """Toggle the button according to password field."""
        if self.ui.Password.text() not in [None, ""]:
            self.ui.Encrypt.setEnabled(True)
            self.ui.Encrypt.setText("Encrypt")
            self.ui.Decrypt.setEnabled(True)
            self.ui.Decrypt.setText("Decrypt")

        else:
            self.ui.Encrypt.setEnabled(False)
            self.ui.Encrypt.setText("")
            self.ui.Decrypt.setEnabled(False)
            self.ui.Decrypt.setText("")

    def crypto_add_file(self, file):
        """Add input file for crypto page."""
        global Infile

        Size = 15
        Infile = file
        self.ui.CryptoDragDropLabel.setStyleSheet(DragDropLabelSS2)
        if len(file) > 105:
            file = file[:102] + '...'
        font = QFont()
        font.setFamily("Cabin Sketch")
        font.setPointSize(Size)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.ui.CryptoDragDropLabel.setFont(font)
        self.ui.CryptoDragDropLabel.setText("File Loaded:\n" +
                                            os.path.basename(file))
        self.ui.CryptoSaveLocBrowse.setEnabled(True)
        self.ui.CryptoSaveLoc.setEnabled(True)
        self.ui.CryptoSaveLocBrowseL.setText(
            "Click To Browse Save Location"
        )
        self.ui.CryptoSaveLocBrowseL.setStyleSheet(
            SaveLocationLabelSS2)

    def crypto_add_dialog(self):
        """Open File Dialog for Crypto Page."""
        file = QFileDialog.getOpenFileName(
            caption="Input File")[0]
        if not file:
            self.ui.CryptoSaveLocBrowseL.setText("Invalid Save Filename.")
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.CryptoSaveLocBrowseL.setText("Click To Browse Save Location"))
            self.reset()

        else:
            self.crypto_add_file(file)

    def crypto_save_file(self):
        """Get the output file for Crypto Page."""
        global Outfile

        file = QFileDialog.getSaveFileName(
            caption="Save File")[0]

        if not file:
            self.ui.CryptoSaveLocBrowseL.setText("Invalid Save Filename.")
            QtCore.QTimer.singleShot(
                2000, lambda: self.ui.CryptoSaveLocBrowseL.setText("Drag & Drop/\
                                                                   \nClick To Add File"))
        else:
            Outfile = file
            Size = 15
            self.ui.Password.setMaximumSize(QtCore.QSize(16777215, 28))
            self.ui.AlgoSelect.setEnabled(True)
            self.ui.AlgoSelect.setMaximumSize(QtCore.QSize(16777215, 25))
            font = QFont()
            font.setFamily("Cabin Sketch")
            font.setPointSize(Size)
            font.setBold(True)
            font.setItalic(True)
            font.setWeight(75)
            self.ui.CryptoSaveLocBrowseL.setFont(font)
            self.ui.CryptoSaveLocBrowseL.setText("Save To: " +
                                                  os.path.basename(file))
            self.ui.CryptoSaveLocBrowseL.setStyleSheet(DragDropLabelSS2)

    def reset(self):
        """Reset the GUI to initial state."""
        global Infile, Outfile, URL, Datafile

        Infile = None
        Outfile = None
        URL = None
        Datafile = None
        self.lsb = None
        self.nb = None

        # Reserved for an update.
        self.ui.StegEnc.setEnabled(False)

        # Crypto Page
        self.ui.CryptoSaveLoc.setEnabled(False)
        self.ui.CryptoSaveLocBrowseL.setText("Add Input File First")
        self.ui.CryptoSaveLocBrowseL.setStyleSheet(SaveLocationLabelSS1)
        self.ui.Password.setMaximumSize(QtCore.QSize(0, 0))
        self.ui.Encrypt.setEnabled(False)
        self.ui.Encrypt.setText("")
        self.ui.Decrypt.setEnabled(False)
        self.ui.Decrypt.setText("")
        self.ui.CryptoDragDropLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.CryptoDragDropLabel.setText("Click To Add/\n"
                                            "Drag & Drop Files")
        self.ui.AlgoSelect.setEnabled(False)
        self.ui.AlgoSelect.setMaximumSize(QtCore.QSize(0, 0))
        font = QFont()
        font.setFamily("Cabin Sketch")
        font.setPointSize(15)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.ui.AlgoSelect.setFont(font)
        self.ui.Password.setText("")

        # Transfer Page
        self.ui.ButtonTransfer.setEnabled(False)
        self.ui.ButtonTransfer.setText("Add File/Url First")
        self.ui.Url.setEnabled(True)
        self.ui.Url.setText("")
        self.ui.DragDropLabelTransfer.setStyleSheet(DragDropLabelTransferSS1)
        font = QtGui.QFont()
        font.setFamily("DEADLY KILLERS DEMO")
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.ui.DragDropLabelTransfer.setFont(font)
        self.ui.DragDropLabelTransfer.setText("Click To Add/\n"
                                              "Drag & Drop Files")
        self.ui.Url.setPlaceholderText("Paste URL Here.")

        # Hide Page
        self.ui.InfileDragDropLabel.setText("(Audio File)\nClick To Add/Drag & Drop Files")
        self.ui.InfileDragDropLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.DatafileDragDrop.setEnabled(False)
        self.ui.DatafileDragDropLabel.setText("Add Input File First")
        self.ui.DatafileDragDropLabel.setStyleSheet("")
        self.ui.SaveLocBrowseStego.setEnabled(False)
        self.ui.SaveLocBrowseStegoLabel.setText("")
        self.ui.SaveLocBrowseStegoLabel.setStyleSheet("")
        self.ui.HideBtn.setEnabled(False)
        self.ui.HideBtn.setText("")
        self.ui.lsb.setMaximumSize(QtCore.QSize(0, 0))

        # Recover Page
        self.ui.InfileRecLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.InfileRecLabel.setText(
            "(Stego Audio)\n Drag&Drop/Click To Add File")
        self.ui.OutfileRecBrowse.setEnabled(False)
        self.ui.OutfileRecLabel.setText("Add Input File First.")
        self.ui.OutfileRecLabel.setStyleSheet("")
        self.ui.LSBNB.setMaximumSize(QtCore.QSize(0, 0))
        self.ui.RecButton.setEnabled(False)
        self.ui.RecButton.setText("")

        # Macro EncSteg Page
        self.ui.Backward.setEnabled(False)
        self.ui.MInfileLabel.setStyleSheet(DragDropLabelSS1)
        self.ui.Backward.setText("")
        self.ui.Forward.setEnabled(False)
        self.ui.Forward.setText("")
        self.ui.LSBNbytes.setMaximumSize(QtCore.QSize(0, 0))
        self.ui.SaveLocationBrowse.setEnabled(False)
        self.ui.SaveLocationBrowseLabel.setStyleSheet("")
        self.ui.SaveLocationBrowseLabel.setText("")
        self.ui.MDatafileDragDrop.setEnabled(False)
        self.ui.MDatafileLabel.setStyleSheet("border: 0px solid;")
        self.ui.MDatafileLabel.setText("Add Audio File First.")
        self.ui.MInfileDragDrop.setEnabled(True)
        self.ui.MInfileLabel.setText(
            "(Audiofile)\nClick To Add/Drag&Drop Files")


# Splash Screen
class SplashScreen(QMainWindow):
    """Splash Screen."""

    def __init__(self):
        """Set up the splash screen."""
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # Remove Window Frame & Make background translucent
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Set Drop Shadow
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(5)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 90))
        self.ui.DropShadowFrame.setGraphicsEffect(self.shadow)

        # Connecting The Progress Bar
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.load)
        self.timer.start(20)

        # Loading Screen Updates
        QtCore.QTimer.singleShot(
            1500, lambda: self.ui.LoadingStatus.setText("Importing Modules"))
        QtCore.QTimer.singleShot(
            2800, lambda: self.ui.LoadingStatus.setText("Almost Done..."))

        self.show()

    def load(self):
        """Update the progress bar."""
        global Progress

        # Updating Progress Bar
        self.ui.ProgressBar.setValue(Progress)
        # When Progress Bar Completes
        if Progress > 100:
            self.timer.stop()

            # Show Main Window
            self.main = MainWindow()
            self.close()

        if Progress > 80:
            QtCore.QTimer.singleShot(
                0, lambda: self.ui.AppDesc.setText("Made by Rakshan Sharma"))

        Progress += 1


# App Driver Code.
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
