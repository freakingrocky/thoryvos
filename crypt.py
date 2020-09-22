"""It encrypts and decrypts file data."""


def generate_salt(password):
    """
    Generate a salt, which is the sha512 hash of the password.

    The salt in this case, is not meant for added security.
    In a database, when there are many passwords, an attacker
    would need to rehash a bruteforce with each unique salt but here,
    that added layer of security would be meaningless.
    Thus, the salt is dependent on the password and
    is thus not meant for additional security.
    It is there as scrypt requires a salt value.
    """
    from hashlib import sha512
    return sha512(password.encode()).hexdigest()


# Generates the scrypt hash of the password
def generate_key(password, mode):
    """Generate the scrypt hash value of the password as per mode."""
    from Crypto.Protocol.KDF import scrypt
    salt = generate_salt(password)

    if mode == "AES":
        return scrypt(password, salt, 32, N=2**20, r=8, p=1)
    return scrypt(password, salt, 24, N=2**20, r=8, p=1)


# Encrypts/Decrypts file using AES256
def AES(data, password, enc):
    """AES Algorithm."""
    # Importing libraries
    from Crypto.Cipher import AES
    from Crypto import Random

    # Generates the key according to password
    key = generate_key(password, "AES")

    # Encryption
    if enc:
        from Crypto.Util.Padding import pad
        iv = Random.new().read(AES.block_size)
        cipher_object = AES.new(key, AES.MODE_CBC, IV=iv)
        return (iv + cipher_object.encrypt(pad(data, 16)))
        # iv is precatenaed in the return value, 16 bytes

    # Decryption
    iv = data[44:60]
    # The first 44 bytes are the WAV header file, so they are ignored
    cipher_object = AES.new(key, AES.MODE_CBC, IV=iv)
    return cipher_object.decrypt(data[60:])


def Salsa20(data, password, enc):
    """Salsa20 algorithm."""
    pass
    # TODO

# Encrypts/Decrypts file using DESTriple
def DES(data, password, enc):
    """DES Algorithm."""
    # Importing libraries
    from Crypto.Cipher import DES3
    from Crypto.Util.Padding import pad, unpad

    # Generates the key according to password
    key = DES3.adjust_key_parity(generate_key(password, "DES"))

    # Encryption
    if enc:
        cipher_object = DES3.new(key, DES3.MODE_CBC)
        return (cipher_object.iv + cipher_object.encrypt(pad(data, 8)))
        # iv is precatenaed in the return value, 8 bytes

    # Decryption
    iv = data[44:52]
    # The first 44 bytes are the WAV header file, so they are ignored
    cipher_object = DES3.new(key, DES3.MODE_CBC, IV=iv)
    return unpad(cipher_object.decrypt(data[52:]), 8)


# Encryption Function
def encrypt_data(infile, mode, password):
    """Read & Send data to encryption functions."""
    with open(infile, "rb") as input_file:
        with open("temp.bin", "wb") as temp_data_file:
            data = input_file.read()
            if mode == "AES":
                encrypted_data = AES(data, password, True)
                temp_data_file.write(encrypted_data)
            else:
                encrypted_data = DES(data, password, True)
                temp_data_file.write(encrypted_data)


# Decryption Function
def decrypt_data(infile, mode, password):
    """Read & Send data to decryption functions."""
    from time import sleep
    sleep(0.3)
    """Since anyone can remove any line in this file,
    sleep function is just here as an aadded 'bonus' defense
    against bruteforce."""

    with open((infile+".wav"), "rb") as input_file:
        with open("temp.wav", "wb") as temp_data_file:
            data = input_file.read()
            if mode == "AES":
                decrypted_data = AES(data, password, False)
                temp_data_file.write(decrypted_data)
            else:
                decrypted_data = DES(data, password, False)
                temp_data_file.write(decrypted_data)
