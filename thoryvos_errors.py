class UnexpectedError(Exception):
    """Uneforseen Error."""
    def __init__(self, message=None):
        ErrorMsg = ("An Unexpected Error has occured.")
        self.message = (ErrorMsg + " " + message) if message is not None else ErrorMsg
        super().__init__(self.message)


class InvalidEncryptionMode(Exception):
    """The encryption mode entered is invalid."""
    
    def __init__(self, mode):
        self.ErrorMsg = f"Unsupported Encryption Mode: {mode}"
        AvailableModes = "AES, DES, Salsa20"
        super().__init__(self.ErrorMsg + "\n Currently Supported Modes are: (Case Insensitive): \n  " + AvailableModes)


class EmptyDataFile(Exception):
    """The Data File provided is empty."""
    def __init__(self, path=None):
        self.ErrorMsg = "Data File Provided is empty." if not path else f"{path} is empty."
        super().__init__(self.ErrorMsg)


class NotAWAVFile(Exception):
    """The file provided is not a WAV file."""
    def __init__(self, path=None):
        self.ErrorMsg = "The file provided must be a WAV file." if not path else f"{path} is not a WAV File."
        super().__init__(self.ErrorMsg)


class URLError(Exception):
    """The URL provided is invalid."""
    def __init__(self):
        super().__init__("Invalid URL.")


class FileDoesNotExist(Exception):
    """The path provided is invalid."""
    def __init__(self, path=None):
        self.ErrorMsg = "File does not exist." if not path else f"{path} is invalid."
        super().__init__(self.ErrorMsg)
    

class LSBError(Exception):
    """LSB must be specified for extraction."""
    def __init__(self):
        super().__init__("The LSB value must be specified for extraction/retrieval.")


class NBytesError(Exception):
    """NBytes must be specified during extraction/retrieval."""
    def __init__(self):
        super().__init__("The number of bytes to extract must be specified for extraction/retrieval.")

if __name__ == "__main__":
    raise NBytesError()
