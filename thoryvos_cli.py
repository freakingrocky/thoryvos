"""Command Line Interface for thoryvos."""
from termcolor import cprint
from os import get_terminal_size
import thoryvos_driver as thoryvos
import argparse
from thoryvos_errors import *


def credits():
    """Print Credits."""
    size = get_terminal_size()

    cprint('thor\N{MATHEMATICAL ITALIC SMALL PSI}vos'.center(
        size.columns, " "), 'red', attrs=['bold'])
    cprint("The all-in-one cryptography toolkit".center(size.columns,
                                                                   " "), 'red', attrs=['dark'])
    cprint("="*(size.columns-4), attrs=['dark'])
    cprint("Made by Rakshan Sharma, V1.0", 'blue')
    cprint("Use '-h' flag to get help.")
    cprint("="*(size.columns-4), attrs=['dark'])
    print()


def parse_cl():
    """CLI Argument Parser."""
    parser = argparse.ArgumentParser(description='thoryvos Command Line\
                                     Interface. Macros are available on GUI.')
    parser.add_argument('-i', '--infile',
                        help="The input filename.",
                        type=str,
                        required=False)
    parser.add_argument('-o', '--outfile',
                        help="The output filename.",
                        type=str,
                        required=False)
    parser.add_argument('-m', '--mode', '-operation', '-op',
                        help="Available Modes: encrypt/decrypt/hide/recover/\
                        upload/download",
                        type=str,
                        required=True)
    parser.add_argument('-u', '--url',
                        help="Anonfiles URL to download",
                        type=str,
                        required=False)
    parser.add_argument('-a', '--algorithm', '--algo',
                        help="The algorithm for encryption/decryption.\
                        Available algorithms are: AES/DES/Salsa20",
                        type=str,
                        required=False)
    parser.add_argument('-p', '--password',
                        help="Password",
                        type=str,
                        required=False)
    parser.add_argument('-df', '--datafile', '-d',
                        help="The data filename.",
                        type=str,
                        required=False)
    parser.add_argument('-l', '--lsb',
                        help="LSB used during hiding.",
                        type=int,
                        required=False)
    parser.add_argument('-nb', '--nbytes', '-n',
                        help="Number of bytes hidden.",
                        type=int,
                        required=False)

    args = parser.parse_args()
    credits()

    if args.mode == 'encrypt':
        if not args.password:
            exit("Password is required.")
        if not args.algorithm:
            raise InvalidEncryptionMode
        if not args.infile:
            raise FileDoesNotExist
        if not args.outfile:
            exit("Output file is required.")

        thoryvos.encryptor(args.infile, args.outfile, args.password,
                           args.algorithm.upper())

        exit("Successfully Ecrypted.")

    if args.mode == 'decrypt':
        if not args.password:
            exit("Password is required.")
        if not args.algorithm:
            raise InvalidEncryptionMode
        if not args.infile:
            raise FileDoesNotExist
        if not args.outfile:
            exit("Output file is required.")

        thoryvos.decryptor(args.infile, args.outfile, args.password,
                           args.algorithm.upper())

        exit("Successfully Decrypted.")

    if args.mode == 'hide':
        if not args.datafile:
            raise EmptyDataFile
        if not args.lsb:
            args.lsb = None
        if not args.infile:
            raise FileDoesNotExist
        if not args.outfile:
            exit("Output file is required.")

        thoryvos.hide_data(args.infile, args.outfile,
                           args.datafile, args.lsb)

        cprint(
    f"""YOU MUST REMEMBER THESE VALUES FOR DATA EXTRACTION:
    LSB: {code[0]}
    Bytes To Recover: {code[1]}""", 'red', attrs=['bold'])

        exit(0)

    if args.mode == 'recover':
        if not args.lsb:
            raise LSBError
        if not args.nbytes:
            raise NBytesError
        if not args.infile:
            raise FileDoesNotExist
        if not args.outfile:
            exit("Output file is required.")

        thoryvos.recover_data(args.infile, args.outfile, args.lsb,
                              args.nbytes)

        exit(0)

    if args.mode == 'upload':
        if not args.infile:
            raise FileDoesNotExist

        URL = thoryvos.anon_upload(args.infile)

        exit(f"URL: {URL}")

    if args.mode == 'download':
        if not args.url:
            raise URLError

        filename = thoryvos.anon_download(args.url)

        exit(f"Saved to {filename}")


if __name__ == '__main__':
    parse_cl()
