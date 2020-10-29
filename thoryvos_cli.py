"""Command Line Interface for thoryvos."""
from termcolor import cprint
from os import get_terminal_size
import thoryvos_driver as thoryvos
import argparse
from thoryvos_errorcodes import *


ERRORCODES = range(1, 9)


def credits():
    """Print Credits."""
    size = get_terminal_size()

    cprint('thor\N{MATHEMATICAL ITALIC SMALL PSI}vos'.center(
        size.columns, " "), 'red', attrs=['bold'])
    cprint("The all-in-one audio based cryptography toolkit".center(size.columns,
                                                                   " "), 'red', attrs=['dark'])
    cprint("="*(size.columns-4), attrs=['dark'])
    cprint("Made by Rakshan Sharma, V1.0", 'blue')
    cprint("Use 'help' command to get commands.")
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
            exit("Algorithm must be specified.")
        if not args.infile:
            exit("Input file is required.")
        if not args.outfile:
            exit("Output file is required.")

        code = thoryvos.encryptor(args.infile, args.outfile, args.password,
                                  args.algorithm.upper())
        if code in ERRORCODES:
            exit(Error[code])

        exit("Successfully Ecrypted.")

    if args.mode == 'decrypt':
        if not args.password:
            exit("Password is required.")
        if not args.algorithm:
            exit("Algorithm must be specified.")
        if not args.infile:
            exit("Input file is required.")
        if not args.outfile:
            exit("Output file is required.")

        code = thoryvos.decryptor(args.infile, args.outfile, args.password,
                                  args.algorithm.upper())
        if code in ERRORCODES:
            exit(Error[code])

        exit("Successfully Decrypted.")

    if args.mode == 'hide':
        if not args.datafile:
            exit("Datafile is required.")
        if not args.lsb:
            args.lsb = None
        if not args.infile:
            exit("Input file is required.")
        if not args.outfile:
            exit("Output file is required.")

        code = thoryvos.hide_data(args.infile,
                                  args.outfile,
                                  args.datafile,
                                  args.lsb)

        if type(code) == int:
            exit(Error[code])

        cprint(
    f"""YOU MUST REMEMBER THESE VALUES FOR DATA EXTRACTION:
    LSB: {code[0]}
    Bytes To Recover: {code[1]}""", 'red', attrs=['bold'])

        exit(0)

    if args.mode == 'recover':
        if not args.lsb:
            exit(Error[7])
        if not args.nbytes:
            exit(Error[8])
        if not args.infile:
            exit("Input file is required.")
        if not args.outfile:
            exit("Output file is required.")

        code = thoryvos.recover_data(args.infile, args.outfile, args.lsb,
                                     args.nbytes)
        if code in ERRORCODES:
            exit(Error[code])

        exit(0)

    if args.mode == 'upload':
        if not args.infile:
            exit("Input file is required.")

        code = thoryvos.anon_upload(args.infile)

        if type(code) == int:
            exit(Error[code])

        exit(f"URL: {code}")

    if args.mode == 'download':
        if not args.url:
            exit("URL is required.")

        code = thoryvos.anon_download(args.url)

        if type(code) == int:
            exit(Error[code])

        exit(f"Saved to {code}")


if __name__ == '__main__':
    parse_cl()
