"""Transfer files to/from anonfiles.com using AnonFile API."""
from anonfile.anonfile import AnonFile
from os import getcwd


def upload(infile):
    """Upload the output file to anonfiles and returns a link."""
    anon = AnonFile()
    status, file_url = anon.upload_file(infile)
    return file_url


def download(url):
    """Download a file from anonfiles."""
    anon = AnonFile()
    location = getcwd()
    anon.download_file(url, location)
    return location


def verify(text):
    """Verify that the url is valid in a very simple manners."""
    if 'anonfiles.com' in text:
        return True
    return False
