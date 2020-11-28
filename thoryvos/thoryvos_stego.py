"""
Steganography Backend for thoryvos.

The LSB algorithm is taken from:
 https://github.com/pavanchhatpar/wav-steg-py
"""
# Importing Dependencies
from os import stat
from math import ceil
from struct import pack, unpack
from array import array

import PyWave
import soundfile as sf


class Stego:
    """Steganographer Class."""

    def __init__(self, infile: str, lsb=None) -> None:
        """Set the required data from the infile."""
        # Opening the files.
        data, samplerate = sf.read(infile)
        self.audio = PyWave.open(infile, 'r')
        sf_object = sf.SoundFile(infile)

        # Saving the parameters of the infile for later.
        self.params = {
            'channels': self.audio.channels,
            'frequency': self.audio.frequency,
            'bitrate': self.audio.bitrate,
            'format': self.audio.format,
            'bits_per_sample': self.audio.bits_per_sample
        }

        # Setting the required parameters for lsb algorithm.
        self.nframes = len(data)
        self.nsamples = self.nframes * sf_object.channels
        self.type = sf_object.subtype
        self.lsb = lsb

        # Closing the soundfile object.
        sf_object.close()

    def prepeare_hide(self, datafile: str) -> None:
        """Compatibility Check & Sets required parameters."""
        # Getting the size of the datafile
        self.datasize = stat(datafile).st_size

        # If we are not provided with a lsb, we set it to optimal value.
        if not self.lsb:
            self.lsb = self.get_lsb()

        # Required for the lsb algorithm.
        self.fmt, self.mask, self.smallest_byte = self.get_req_data()

        # Checking if there is enough space in the infile to hide data.
        max_bytes = (self.nsamples * self.lsb) // 8
        if self.datasize > max_bytes:
            self.raise_exception()

    def raise_exception(self) -> None:
        """Raise errors."""
        # Getting the minimum number of lsb required
        req_lsb = self.get_lsb()
        # Since, there are only 8 lsb in the infile
        if req_lsb >= 8:
            raise ValueError("Datafile is too large for this audio file.")

        raise ValueError(f"{req_lsb} required to hide datafile in audio file")

    def hide(self, datafile: str, outfile: str) -> tuple:
        """Hide data in the audio file."""
        # Setting the required parameters for hiding the data.
        self.prepeare_hide(datafile)

        # Storing the plain audio data for processing in an array.
        plain_audio_data = array('i', unpack(self.fmt, self.audio.read()))
        self.audio.close()

        # Getting a pointer to the buffer to the data
        data = memoryview(open(datafile, 'rb').read())

        # Keeps track of position in the audio & data file.
        data_index = 0
        audio_index = 0

        # Initializing an array to store the stego data.
        stego_audio_data = []

        # Initializng some more variables for the lsb algorithm.
        buffer = 0
        buffer_length = 0
        complete = False

        # The actual lsb algorithm.
        while not complete:
            while (buffer_length < self.lsb and data_index // 8 < len(data)):

                buffer += (data[data_index // 8] >> (data_index % 8)
                           ) << buffer_length
                data_added = 8 - (data_index % 8)
                buffer_length += data_added
                data_index += data_added

            current_bit = buffer % (1 << self.lsb)
            buffer >>= self.lsb
            buffer_length -= self.lsb

            while (audio_index < len(plain_audio_data) and
                   plain_audio_data[audio_index] == self.smallest_byte):

                stego_audio_data.append(pack(self.fmt[-1],
                                             plain_audio_data[audio_index]))
                audio_index += 1

            if audio_index < len(plain_audio_data):
                current_sample = plain_audio_data[audio_index]
                audio_index += 1

                sign = 1

                if current_sample < 0:
                    current_sample = -current_sample
                    sign = -1

                stego_sample = sign * ((current_sample & self.mask) |
                                       current_bit)
                stego_audio_data.append(pack(self.fmt[-1], stego_sample))

            if (data_index // 8 >= len(data) and buffer_length <= 0):
                complete = True

        # Append the rest of the data from plain audio to stego audio
        while audio_index < len(plain_audio_data):
            stego_audio_data.append(pack(self.fmt[-1],
                                         plain_audio_data[audio_index]))
            audio_index += 1

        # Save stego file.
        with PyWave.open(outfile,
                         mode="w",
                         channels=self.params["channels"],
                         frequency=self.params["frequency"],
                         bits_per_sample=self.params["bits_per_sample"],
                         format=self.params["format"]) as out_file:
            out_file.write(b"".join(stego_audio_data))

        # Needed for retrieval.
        return (self.lsb, self.datasize)

    def prepeare_recover(self) -> None:
        """Set the parameters required for retrieval."""
        # The default lsb value for retrieval is 1
        if not self.lsb:
            self.lsb = 1

        # Required for the lsb recovery algorithm.
        self.fmt, _, self.smallest_byte = self.get_req_data()

        self.mask = (1 << self.lsb) - 1

    def recover(self, outfile: str, nbytes: int) -> bool:
        """Recover data from the audio file."""
        # Setting the required parameters for retrieval the data.
        self.prepeare_recover()

        # Storing the audio data in an array for processing.
        stego_audio_data = array('i', unpack(self.fmt, self.audio.read()))
        self.audio.close()

        # Initializng the variables and data structures for retrieval.
        data = bytearray()
        index = 0
        buffer = 0
        buffer_length = 0

        # The actual lsb algorithm.
        while nbytes > 0:
            current_sample = stego_audio_data[index]

            if current_sample != self.smallest_byte:

                buffer += (abs(current_sample) & self.mask) << buffer_length
                buffer_length += self.lsb

            index += 1

            while (buffer_length >= 8 and nbytes > 0):

                current_sample = buffer % (1 << 8)
                buffer >>= 8
                buffer_length -= 8
                data += pack('1B', current_sample)
                nbytes -= 1

        # Writing data to the file.
        with open(outfile, 'wb+') as out_file:
            out_file.write(bytes(data))

        return True

    def get_lsb(self) -> int:
        """Get the optimal lsb for the data & audio file."""
        return ceil(self.datasize * 8 / self.nsamples)

    def get_req_data(self) -> tuple:
        """Return the fmt, mask & smallest byte based on the filetype."""
        if self.type == "PCM_U8":
            """Samples are unsigned 8-bit integers."""
            fmt = f"{self.nsamples}B"
            mask = (1 << 8) - (1 << self.lsb)
            smallest_byte = -(1 << 8)

        elif self.type == "PCM_S8":
            """Samples are signed 8-bit integers."""
            fmt = f"{self.nsamples}b"
            mask = (1 << 8) - (1 << self.lsb)
            smallest_byte = -(1 << 8)

        elif self.type == 'PCM_16':
            """Samples are signed 16-bit integers."""
            fmt = f"{self.nsamples}h"
            mask = (1 << 15) - (1 << self.lsb)
            smallest_byte = -(1 << 15)

        elif self.type == 'PCM_24':
            """Samples are signed 24-bit integers."""
            fmt = f"{self.nsamples * 3}B"
            mask = (1 << 23) - (1 << self.lsb)
            smallest_byte = -(1 << 23)

        elif self.type == 'PCM_32':
            """Samples are signed 32-bit integers."""
            fmt = f"{self.nsamples}i"
            mask = (1 << 31) - (1 << self.lsb)
            smallest_byte = -(1 << 31)

        elif self.type == 'PCM_64':
            """Samples are signed 64-bit integers."""
            fmt = f"{self.nsamples}q"
            mask = (1 << 63) - (1 << self.lsb)
            smallest_byte = -(1 << 63)

        else:
            raise Exception(f"Unsupported WAV file.\
                            {self.type} is not supported.")
            exit(1)

        return (fmt, mask, smallest_byte)


if __name__ == '__main__':
    exit("""

          DIRECT COMMAND LINE INTERFACE NOT AVAILABLE
          USE thoryvos_cli.py INSTEAD

          To use as a module:
            import thoryvos_stego as st
            x = st.Stego(infile, lsb)
            x.hide(datafile, outfile)

            y = st.Stego(infile, lsb)
            y.recover(datafile, bytes_hidden)
          """)
