"""Converts files to WAV files and vice versa."""
import wave


# Converts any file to WAV with a .wav header
def file2wave(infile, outfile):
    """Take input a file, any format, and gives output a WAV file."""
    with open(infile, "rb") as input_file:
        with wave.open((outfile+".wav"), "wb") as output_file:
            output_file.setnchannels(1)
            output_file.setsampwidth(4)
            output_file.setframerate(96000*4)
            # output_file.setnchannels(2)
            # output_file.setsampwidth(2)            
            # output_file.setframerate(14000*4)
            data = input_file.read()
            output_file.writeframesraw(data)


# Converts any wav file to an output file
def wave2file(infile, outfile):
    """Take a WAV file as input and convert it into a different file format."""
    with open(outfile, "wb") as output_file:
        with open((infile+".wav"), "rb") as input_file:
            data = input_file.read()
            output_file.write(data)
