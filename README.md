# ***thor𝜓vos***
The all in one cryptographic toolkit.

You can use thor𝜓vos as a module, from the command line or through a GUI.

\
**Simply use pip to install by calling the following command**.\
`pip install thoryvos`


> Currently Available Features:  \
&nbsp;&nbsp;&nbsp;Encryption & Decryption  [Pycryptodome used]\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AES256, DES3, Salsa20  \
&nbsp;&nbsp;&nbsp;Stegography using LSB\
&nbsp;&nbsp;&nbsp;Anonymous File Sharing\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The files are completely vulnerable during uploading/downloading. They are anonymous once uploaded.\
&nbsp;&nbsp;&nbsp;Macros (GUI Only)

To use the GUI, simply execute the following command:\
&nbsp;&nbsp;&nbsp;```python -m thoryvos```
[![Demo Video](https://i.imgur.com/BynAEz0.png)](https://www.youtube.com/watch?v=uIFjztawVHM&feature=youtu.be)

To use the Command Line Interface, simply execute the following
&nbsp;&nbsp;&nbsp;```python -m thoryvos [options]```

![](https://i.imgur.com/8TsifwV.png)

To use as a module, import the driver code.\
&nbsp;&nbsp;&nbsp;```import thoryvos_driver as thoryvos```

The error codes and their meanings are in a seperate file called "thoryvos_errorcodes.py"

To interpret the error codes in your program:
```
from thoryvos_errorcodes import Error

raise Exception(Error[code])
```

# Documentation for the module
### Start by importing the main module and the errors.
```
import thoryvos_driver as thoryvos
```

### For encryption/decryption:
```
thoryvos.encryptor(infile, outfile, password, mode)
thoryvos.decryptor(infile, outfile, password, mode)
```
infile -> Path to the input file (file to be encrypted)\
outfile -> Path to the output file \
password -> Must be a string\
mode -> Algorithm to be used. Must be one of these: "AES/DES/Salsa20". These are AES256, DES3 specifically.

### For file transfer:
```
location = thoryvos.anon_download(url)
url = thoryvos.anon_upload(file)
```
The input must be strings.\
On succesful upload, returns the location of the file downloaded.\
On succesful download, returns the url of the uploaded file.

### For steganography:
```
steg = thoryvos.hide_data(infile, outfile, datafile, lsb=None)
thoryvos.recover_data(infile, outfile, lsb=None, nbytes=None)
```
infile -> Path to the input file (file to be hidden in)\
datafile -> Path to the data file (data file to be hidden)\
outfile -> Path to the output file (name of the output file)\
On succesful hiding, returns a tuple containing lsb & nbytes values respectively. `(lsb, nbytes)`.

### Made by Rakshan Sharma
### Instagram: freakingrocky
