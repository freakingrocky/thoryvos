"""Transfer files to/from anonfiles.com using AnonFile API."""
from anonfile.anonfile import AnonFile
from os import getcwd


def upload(infile):
    """Upload the output file to anonfiles and returns a link."""
    anon = AnonFile()
    upload_obj = anon.upload_file(infile, progressbar=False)
    return upload_obj.geturl()


def download(url):
    """Download a file from anonfiles."""
    anon = AnonFile()
    location = getcwd()
    filename = anon.download_file(url, path=location)
    return location + filename


def verify(text):
    """Verify that the url is valid in a very simple manner."""
    if 'anonfiles.com' in text:
        return True
    return False
