"""
Based on https://github.com/pavanchhatpar/wav-steg-py

This script is based closelt on the reference mentioned above.
Goals:
    (1) Add support for 24, 32 bit WAV integer files [See soundfile, wavio module]
    (2) Pad input data
    (3) Calculate best possible lsb
"""
from os import stat
from math import ceil
from struct import pack, unpack
import wave
from termcolor import cprint


def get_sound_data(infile, lsb):
    "Return Audio Data required for LSB Steganography."
    global sound, params, nframes, nsamples, fmt, mask, smallest_byte

    sound = wave.open(infile, 'r')

    params = sound.getparams()
    nframes = sound.getnframes()
    nsamples = nframes * sound.getnchannels()

    sample_width = sound.getsampwidth()

    if sample_width == 1:
        """
        Samples are unassigned 8-bit integers.
        """
        fmt = f"{nsamples}B"
        mask = (1 << 8) - (1 << lsb)
        smallest_byte = -(1 << 8)

    elif sample_width == 2:
        """
        Samples are unassigned 16-bit integers.

        The least possible value for a sample in audio is 0.
        However, we skip the zero value as it helps preserve the audio quality.
        """
        fmt = f"{nsamples}h"
        mask = (1 << 15) - (1 << lsb)
        smallest_byte = -(1 << 15)

    else:
        """Python's wave mdoule does not support higer than 16 bit wav files."""
        cprint("This WAV file has an unsupported bit depth.", 'red', attrs=['bold'])
        cprint("Support for 24-bit & 32-bit WAV files coming soon.", 'red', attrs=['bold'])
        exit(1)


def get_lsb(infile, datafile):
    with wave.open(infile, 'r') as indata:
        nsamples = indata.getnframes() * indata.getnchannels()
        datasize = stat(datafile).st_size
        return ceil(datasize * 8 / nsamples)


def stego(infile, outfile, datafile, lsb=None):
    """Hide data file in infile using LSB Steganography Algorithm."""
    global sound, params, nframes, nsamples, fmt, mask, smallest_byte
    if not lsb:
        lsb = get_lsb(infile, datafile)
    get_sound_data(infile, lsb)

    # The maximum data we can hide is lsb(specified by user,) bits in each sample.
    # lsb determines the quality of stego audio.
    # We are using floor divison here as it always rounds down to the nearest whole number.
    max_bytes_to_hide = (nsamples * lsb) // 8
    datasize = stat(datafile).st_size

    if datasize > max_bytes_to_hide:
        required_lsb = ceil(datasize * 8 / nsamples)
        if required_lsb >= 8:
            cprint(f"""Data file is to large to hide in this audio file.""", 'red', attrs=['bold'])
            exit(1)
        cprint(f"""Data file is too large to hide,
               You can try using a greater lsb value.
               Remember, the bigger the lsb, lower the quality.
               Atleast {required_lsb} lsb is required.""",
               'red', attrs=['bold'])
        exit(1)

    cprint(f"Using {datasize}B out of {max_bytes_to_hide}B possible.", 'green')

    # Putting all the data from the audio file into a list, using struct module for that.
    plain_audio_data = list(unpack(fmt, sound.readframes(nframes)))
    sound.close()

    # This allows for a safe way into python's buffer protocol
    data = memoryview(open(datafile, 'rb').read())

    # [data index, audio index]
    index = [0, 0]

    # This list will hold the stego audio data
    stego_audio_data = []

    buffer = 0
    buffer_length = 0
    complete = False

    while not complete:
        # while (buffer_length < lsb) and ((index[0] // 8) < len(data)):
        while buffer_length < lsb:
            # If buffer does not already have enough data, add next byte from data to it.
            buffer += ((data[index[0] // 8] >> (index[0] % 8)) << buffer_length)
            data_added = (8 - (index[0] % 8))
            buffer_length += data_added
            index[0] += data_added

        # Get next lsb from buffer to hide
        tmp = (buffer % (1 << lsb))
        buffer >>= lsb
        buffer_length -= lsb

        while (index[1] < len(plain_audio_data)) and (plain_audio_data[index[1]] == smallest_byte):
            # We skip the smallest byte as altering it can cause an overflow.
            stego_audio_data.append(pack(fmt[-1], plain_audio_data[index[1]]))
            index[1] += 1

        if index[1] < len(plain_audio_data):
            tmp_1 = plain_audio_data[index[1]]
            index[1] += 1
            # We alter the LSB's absolute value of the sample to avoid issues with two's complement operation.
            sign = 1

            if tmp_1 < 0:
                tmp_1 = -tmp_1
                sign = -1

            # Bitwise manipulations:
            # AND with mask turns the lsb of current sample to 0.
            # OR with current data replaces the lsb with next lsb of data.
            stego_sample = sign * ((tmp_1 & mask) | tmp)
            stego_audio_data.append(pack(fmt[-1], stego_sample))

        if (index[0] // 8 >= len(data)) and (buffer_length <= 0):
            complete = True

    with wave.open(outfile, "w") as out_file:
        out_file.setparams(params)
        out_file.writeframes(b"".join(stego_audio_data))
    
    cprint(
f"""YOU MUST REMEMBER THESE VALUES FOR DATA EXTRACTION:
    LSB: {lsb}
    Bytes To Recover: {datasize}""", 'red', attrs=['bold'])


def get_data(infile, outfile, lsb, nbytes):
    """Recover data file in infile using LSB Steganography Algorithm."""
    global sound, nframes, nsamples, fmt, smallest_byte
    get_sound_data(infile, lsb)

    # Putting all the data from the audio file into a list, using struct module for that.
    stego_audio_data = list(unpack(fmt, sound.readframes(nframes)))
    # This mask is used to extract the lsb of an integer
    mask = (1 << lsb) - 1

    data = bytearray()
    index = 0
    buffer = 0
    buffer_length = 0
    sound.close()

    while nbytes > 0:
        tmp = stego_audio_data[index]

        if tmp != smallest_byte:
            # We skip the smallest byte as it can cause an overflow.
            buffer += ((abs(tmp) & mask) << buffer_length)
            buffer_length += lsb

        index += 1

        while (buffer_length >= 8) and (nbytes > 0):
            tmp = buffer % (1 << 8)
            buffer >>= 8
            buffer_length -= 8
            data += pack('1B', tmp)
            nbytes -= 1

    with open(outfile, 'wb') as out_file:
        out_file.write(bytes(data))

def confirm_working():
    print("TESTING...")
    stego("huge_test.wav", "temporary.wav", "test.webm", 4)
    print("Hide Complete")
    get_data("temporary.wav", "tested.webm", 4, 73173252)
    print("Recover Complete.")
    print("Done.")
    print("Auto Checking...")
    with open('tested.webm', 'rb') as file_1:
        with open('test.webm', 'rb') as file_2:
            if file_1.read() == file_2.read():
                print("Checked...OK")
            else:
                print("Corrupted File!!!")

if __name__ == '__main__':
    confirm_working()
