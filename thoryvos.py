"""thóryvos"""
from os import get_terminal_size
from os.path import exists
from converter import file2wave, wave2file
from sys import exit, argv
from crypt import encrypt_data, decrypt_data
from termcolor import cprint
from stego_concept import *
from anonfile.anonfile import AnonFile


def credits():
    """Prints Credits"""
    size = get_terminal_size()

    cprint('thor\N{MATHEMATICAL ITALIC SMALL PSI}vos'.center(
        size.columns, " "), 'red', attrs=['bold'])
    cprint("The all-in-one audio based cryptography toolkit".center(size.columns,
                                                                   " "), 'red', attrs=['dark'])
    cprint("="*(size.columns-4), attrs=['dark'])
    cprint("Made by Rakshan Sharma, V0.8", 'blue')
    cprint("DEVELOPMENT IS IN PROGRESS, NOT READY FOR PUBLISHING",
        'blue', attrs=['bold', 'underline', 'dark'])
    cprint("Refer to the LICENSE file to see what is allowed and what is not.", 'red', attrs=['bold'])
    cprint("_"*(size.columns-4), attrs=['dark'])
    cprint('Current Features Are:')
    cprint('(1) Data Encryption/Decryption Using AES256/DES3',
        'yellow')
    cprint('(2) File Encoding/Decoding to/from WAV',
        'yellow')
    cprint('(3) Audio Steganography',
           'yellow')
    cprint('(4) AnonFiles Upload/Download',
           'yellow')    
    cprint("MORE FEATURES COMING SOON", 'red',
           attrs=['bold', 'underline', 'dark'])
    cprint("="*(size.columns-4), attrs=['dark'])
    print()



def usage():
    """Print the usage."""
    cprint("""
    Usage:
        1. Only convert a file to noise in .wav (NO ENCRYPTION)
            Usage: python thoryvos.py encode
        2. Only convert a file from .wav (NO ENCRYPTION)
            Usage: python thoryvos.py decode
        3. Convert a file to .wav with encryption
            mode(s) available = AES, DES [PyCryptoDome used]
            Usage: python thoryvos.py encrypt mode
        4. Converts a file from .wav with decryption
            mode(s) available = AES, DES [PyCryptoDome used]
            Usage: python thoryvos.py encrypt mode
        5. Hides a file inside a WAV file
            Usage: python thoryvos.py stego hide
        6. Retrieves data from a stego file
            Usage: python thoryvos.py stego retrieve
        7. Uploads a file anonymously to anonfiles.com (Once Uploaded it is anonymous, Vulnerable During Transfer)
            NOTE: The transfer is only anonymous if your connection allows.
            Usage: python thoryvos.py upload anonfiles
        8. Downloads a file from anonfiles.com
            Usage: python thoryvos.py download anonfiles
            """, 'blue', attrs=['bold'])
    exit(1)


def verify_type(filename, Type):
    return filename.endswith("." + Type.replace(".", ""))


def get_file(statement, Type=None, must_exist=False, required=False):
    file = str(input(f"Enter {statement} filename: "))
    if not required and Type is None:
        return file
    # verify_type(file, Type)
    if must_exist:
        if not exists(file):
            cprint(f"{file} DOES NOT EXIST.", 'red', attrs=['bold'])
            get_file(statement, Type=Type, required=required,
                     must_exist=must_exist)
    if Type is not None:
        if not verify_type(file, Type):
            cprint(f"{file} NOT OF CORRECT TYPE. MUST BE {Type}.", 'red', attrs=['bold'])
            get_file(statement, Type=Type, required=required,
                     must_exist=must_exist)
    if required:
        if not file:
            cprint(f"{statement} file is required.", 'red', attrs=['bold'])
            get_file(statement, Type=Type, required=required, must_exist=must_exist)
    return file


def encode():
    """Convert any file to a WAV file."""
    try:
        infile = get_file('input', must_exist=True, required=True)
        outfile = get_file('output')
        if not outfile:
            outfile = "output.wav"
            while exists(outfile):
                outfile.replace('.wav', "_new.wav")
            print(f"Output is given as {outfile}")
        cprint("WORKING".center(get_terminal_size().columns -
                                4, "-"), 'yellow', attrs=['dark'])

        file2wave(infile, outfile.replace(".wav", ""))
        cprint("Operation Completed Successfuly".center(
            get_terminal_size().columns - 4, "+"), 'green', attrs=['dark'])
    except:
        cprint("Error!".center(get_terminal_size() - 4, "-"),
               'red', attrs=['dark'])
        exit(1)
    exit(0)


def decode():
    """Convert any WAV file to a file."""
    try:
        infile = get_file('WAV', must_exist=True, Type='wav', required=True)
        outfile = get_file('output')
        if not outfile:
            outfile = "output.bin"
            while exists(outfile):
                outfile.replace('.bin', '_new.bin')
            print(f"Output is given as {outfile}")
        cprint("WORKING".center(get_terminal_size().columns -
                                4, "-"), 'yellow', attrs=['dark'])
        wave2file(infile.replace(".wav", ""), outfile)
        cprint("Operation Completed Successfuly".center(
            get_terminal_size().columns - 4, "+"), 'green', attrs=['dark'])
    except:
        cprint("Error!".center(get_terminal_size() - 4, "-"),
               'red', attrs=['dark'])
        exit(1)
    exit(0)


def encrypter(mode):
    """Encrypt a file."""
    from os import remove
    try:
        infile = get_file('input', must_exist=True, required=True)
        outfile = get_file('output')
        if not outfile:
            outfile = "output.wav"
            while exists(outfile):
                outfile.replace('.wav', '_new.wav')
            print(f"Output is given as {outfile}")
        password = str(input("Enter password: "))
        while not password:
            print("Password is required.")
            password = str(input("Enter password:"))
        cprint("WORKING".center(get_terminal_size().columns - 4, "-"), 'yellow', attrs=['dark'])
        encrypt_data(infile, mode, password)
        file2wave("temp.bin", outfile.replace(".wav", ""))
        remove("temp.bin")
        cprint("Operation Completed Successfuly".center(
            get_terminal_size().columns - 4, "+"), 'green', attrs=['dark'])
    except:
        cprint("Error!".center(get_terminal_size() - 4, "-"),
               'red', attrs=['dark'])
        if exists("temp.bin"):
            remove("temp.bin")
        exit(1)
    exit(0)


def decrypter(mode):
    """Decrypt a file."""
    from os import remove
    try:
        infile = get_file('input', must_exist=True, Type='wav', required=True)
        outfile = get_file('output')
        if not outfile:
            outfile = "output.bin"
            while exists(outfile):
                outfile.replace('.bin', '_new.bin')
            print(f"Output is given as {outfile}")
        password = str(input("Enter password: "))
        while not password:
            print("Password is required.")
            password = str(input("Enter password:"))
        cprint("WORKING".center(get_terminal_size().columns -
                                4, "-"), 'yellow', attrs=['dark'])
        decrypt_data(infile, mode, password)
        wave2file("temp", outfile)
        remove("temp.wav")
        cprint("Operation Completed Successfuly".center(
            get_terminal_size().columns - 4, "+"), 'green', attrs=['dark'])
    except:
        cprint("Error!".center(get_terminal_size() - 4, "-"),
               'red', attrs=['dark'])
        if exists("temp.wav"):
            remove("temp.wav")
        exit(1)
    exit(0)


def steg(hide=True):
    """Hide Data in Audio File."""
    from os.path import exists
    try:
        if hide:
            infile = get_file('audio', must_exist=True, Type='wav', required=True)
            outfile = get_file('output/stego', Type='wav', required=True)
            data_file = get_file('data', required=True)
            lsb = input("ENTER LSB (range 0-7):")
            if not lsb:
                cprint("WORKING".center(get_terminal_size().columns -
                                        4, "-"), 'yellow', attrs=['dark'])
            stego(infile, outfile, data_file)
            if lsb:
                cprint("WORKING".center(get_terminal_size().columns -
                                        4, "-"), 'yellow', attrs=['dark'])
            stego(infile, outfile, data_file, int(lsb))

        else:
            infile = get_file('stego', must_exist=True, Type='wav')
            outfile = get_file('output', required=True)
            lsb = int(input("ENTER LSB (given during hiding):"))
            while not lsb:
                print("LSB value is required.")
                lsb = int(input("ENTER LSB (given during hiding):"))
            nbytes = int(
                input("Enter Bytes To Recover (given during hiding):"))
            while not nbytes:
                print("Bytes To Recover is required.")
                nbytes = int(
                    input("Enter Bytes To Recover (given during hiding):"))
            cprint("WORKING".center(get_terminal_size().columns - 4, "-"), 'yellow', attrs=['dark'])
            get_data(infile, outfile, lsb, nbytes)
        cprint("Operation Completed Successfuly".center(get_terminal_size().columns - 4, "+"), 'green', attrs=['dark'])
    except:
        cprint("Error!".center(get_terminal_size() - 4, "-"),
               'red', attrs=['dark'])
        exit(1)
    exit(0)


def anonfiles_transfer(upload=True):
    """Upload the output file to anonfiles and returns a link."""
    anon = AnonFile()
    try:
        if upload:
            infile = get_file('input', required=True)
            cprint("Uploading...", 'yellow', attrs=['dark'])
            status, file_url = anon.upload_file(infile)
            cprint("Uploaded.", 'green', attrs=['dark'])
            cprint(f"File URL: {file_url}", attrs=['bold'])
        else:
            url = str(input("Enter url: "))
            print("Downloading...", 'yellow', attrs=['dark'])
            anon.download_file(url)
            print("Downloaded.", 'green', attrs=['dark'])
    except:
        cprint("Error!".center(get_terminal_size() - 4, "-"), 'red', attrs=['dark'])
        exit(1)
    exit(0)




def onion_share(upload=True):
    # TODO
    # https://github.com/micahflee/onionshare/tree/develop/onionshare
    pass


def  md5_hash():
    # TODO
    # Produces a MAC to verify message integrity.
    pass


def main():
    try:
        credits()
        if argv[1].lower() == "encode":
            encode()
        if argv[1].lower() == "decode":
            decode()
        if argv[1].lower() == "encrypt":
            if argv[2].upper() == "AES":
                print("AES256 will be used for this encryption process.")
                encrypter("AES")
            if argv[2].upper() == "DES":
                print("DES3 will be used for this encryption process.")
                encrypter("DES")
        if argv[1].lower() == "decrypt":
            if argv[2].upper() == "AES":
                print("It will decrypt according to AES256 algorithm, if DES was used this will generate bad results.")
                decrypter("AES")
            if argv[2].upper() == "DES":
                print("It will be decrypted using DES3 algorithm, if AES was used this will generate bad results.")
                decrypter("DES")
        if (argv[1].lower() == "stego") or ("steganograph" in argv[1].lower()):
            if argv[2].upper() == "HIDE":
                steg()
            if argv[2].upper() == "RETRIEVE":
                steg(hide=False)
        if argv[1].lower() == "upload":
            if argv[2].upper() == "ANONFILES":
                anonfiles_transfer()
        if argv[1].lower() == "download":
            if argv[2].upper() == "ANONFILES":
                anonfiles_transfer(False)
    except IndexError:
        cprint("""\
        There must be atleast 2 arguments.
        Here's the manual:\
        """, 'red', attrs=['bold'])
        usage()
    usage()


if __name__ == "__main__":
    main()

