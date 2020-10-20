"""thoryvos backend for encryption & decryption."""
# Importing Dependenciess
from Crypto.Cipher import AES, Salsa20, DES3
from Crypto import Random
from Crypto.Protocol.KDF import scrypt
from hashlib import sha512
from Crypto.Util.Padding import pad, unpad
import PyWave as PW


def get_key(password: str, length: int):
    """Generate the key according to password."""
    salt = sha512(password.encode()).hexdigest()
    return scrypt(password, salt, length, N=2**20, r=8, p=1)


class Encrypt:
    """Encrypts data."""

    def __init__(self, infile: str) -> None:
        """Open the data in the infile."""
        self.data = open(infile, 'rb').read()

    def AES(self, password: str) -> bytes:
        """Encrypt data according to AES algorithm."""
        # Generating the key according to password
        key = get_key(password, 32)

        # Generating random IV for encryption.
        iv = Random.new().read(AES.block_size)

        # Encrypting the data.
        cipher_object = AES.new(key, AES.MODE_CBC, IV=iv)
        return (iv + cipher_object.encrypt(pad(self.data, 16)))

    def Salsa20(self, password: str) -> bytes:
        """Encrypt data according to Salsa20 algorithm."""
        # Generating the key according to password
        key = get_key(password, 32)

        # Encrypting the data.
        cipher_object = Salsa20.new(key)
        return (cipher_object.nonce + cipher_object.encrypt(self.data))

    def DES(self, password: str) -> bytes:
        """Encrypt data according to DES3 algorithm."""
        # Generating the key according to password
        key = DES3.adjust_key_parity(get_key(password, 24))

        # Encrypting the data
        cipher_object = DES3.new(key, DES3.MODE_CBC)
        return (cipher_object.iv + cipher_object.encrypt(pad(self.data, 8)))


class Decrypt:
    """Decrypts Data."""

    def __init__(self, infile: str) -> None:
        """Open the data in the infile and sets the IV."""
        data = PW.open(infile, 'r').read()
        self.data = data

    def AES(self, password: str) -> bytes:
        """Decrypt data according to AES algorithm."""
        # Generating the key according to password
        key = get_key(password, 32)

        # Splitting data into IV & Data
        iv = self.data[:16]
        data = self.data[16:]

        # Decrypting the data
        cipher_object = AES.new(key, AES.MODE_CBC, IV=iv)
        return unpad(cipher_object.decrypt(data), 16)

    def Salsa20(self, password: str) -> bytes:
        """Decrypt data according to Salsa20 algorithm."""
        # Generating the key according to password
        key = get_key(password, 32)

        # Splitting data into nonce & Data
        nonce = self.data[:8]
        data = self.data[8:]

        # Decrypting the data. Here the 'IV' is the nonce
        cipher_object = Salsa20.new(key, nonce)
        return cipher_object.decrypt(data)

    def DES(self, password: str) -> bytes:
        """Decrypt data according to DES algorithm."""
        # Generating the key according to password
        key = DES3.adjust_key_parity(get_key(password, 24))

        # Splitting data into IV & Data
        iv = self.data[:8]
        data = self.data[8:]

        # Decrypting the data
        cipher_object = DES3.new(key, DES3.MODE_CBC, IV=iv)
        return unpad(cipher_object.decrypt(data), 8)
