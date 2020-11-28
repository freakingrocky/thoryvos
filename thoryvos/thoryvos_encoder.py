"""Converts files to WAV files and vice versa."""
import wave


# Converts any file to WAV with a .wav header
def file2wave(infile, outfile):
    """Take input a file, any format, and gives output a WAV file."""
    with open(infile, "rb") as input_file:
        with wave.open(outfile, "wb") as output_file:
            output_file.setnchannels(1)
            output_file.setsampwidth(4)
            output_file.setframerate(96000*4)
            data = input_file.read()
            output_file.writeframesraw(data)


# Converts any wav file to an output file
def wave2file(infile, outfile):
    """Take a WAV file as input and convert it into a different file format."""
    with open(outfile, "wb") as output_file:
        with open(infile, "rb") as input_file:
            data = input_file.read()
            output_file.write(data)


# Encodes data into wav file
def encwave(data, outfile):
    """Take input a file, any format, and gives output a WAV file."""
    with wave.open(outfile, "wb") as output_file:
        output_file.setnchannels(1)
        output_file.setsampwidth(4)
        output_file.setframerate(96000*4)
        output_file.writeframesraw(data)


def write_data(data, outfile):
    """Write data to a file."""
    with open(outfile, "wb") as output_file:
        output_file.write(data)


if __name__ == '__main__':
    exit("This is a helper function for thoryvos.")
