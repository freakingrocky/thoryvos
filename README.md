# ***thor𝜓vos***
***The all in one cryptographic toolkit.***\
<img src="https://i.imgur.com/NvivAey.gif" width=2500 />

You can use thor𝜓vos as a module, from the command line or through a GUI.

\
**Simply use [pip](https://pypi.org/project/thoryvos/) to install by calling the following command**.\
`pip install thoryvos`


> Currently Available Features:  \
&nbsp;&nbsp;&nbsp;Encryption & Decryption  [Pycryptodome used]\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AES256, DES3, Salsa20  \
&nbsp;&nbsp;&nbsp;Stegography using LSB\
&nbsp;&nbsp;&nbsp;Anonymous File Sharing\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;The files are completely vulnerable during uploading/downloading. They are anonymous once uploaded.\
&nbsp;&nbsp;&nbsp;Macros (GUI Only)

To use the GUI, simply execute the following command:\
&nbsp;&nbsp;&nbsp;```thoryvos```

[![Demo Video](https://i.imgur.com/hgJ50EK.png)]()

To use the Command Line Interface, simply execute the following
&nbsp;&nbsp;&nbsp;```thoryvos [options]```

![Command Line Usage Demo](https://i.imgur.com/jhptGz2.png)

To use as a module, simply import thoryvos.\
&nbsp;&nbsp;&nbsp;```import thoryvos```

# Documentation for the module
### Start by importing the module.
```
import thoryvos
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
lsb, nbytes = thoryvos.hide_data(infile, outfile, datafile, lsb=None)
thoryvos.recover_data(infile, outfile, lsb=None, nbytes=None)
```
infile -> Path to the input file (file to be hidden in)\
datafile -> Path to the data file (data file to be hidden)\
outfile -> Path to the output file (name of the output file)\
On succesful hiding, returns a tuple containing lsb & nbytes values respectively. `(lsb, nbytes)`.

### Made by Rakshan Sharma
### Instagram: freakingrocky
