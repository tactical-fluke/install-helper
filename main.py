import requests
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
import os
import tomllib
import argparse

class DownloadType(Enum):
        INSTALLER = "INSTALLER"
        ZIP = "ZIP"
        TARFILE = "TARFILE"

class Download:
    download_type = DownloadType.INSTALLER
    name = None
    url = None
    file_destination = None

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.download_type = kwargs.get('download_type', DownloadType.INSTALLER)
        self.url = kwargs['url']
        self.file_destination = kwargs.get('file_destination', None)


def download_file(url: str) -> str:
    response = requests.get(url, stream=True)
    if "content-disposition" in response.headers:
        content_disposition = response.headers['content-disposition']
        filename = content_disposition.split("filename=")[1]
        filename.replace(';', '')
    else:
        filename = url.split("/")[-1]
    
    with open(filename, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10*1024):
            file.write(chunk)

    return filename

def run_installer(file: str):
    import subprocess
    try:
        return subprocess.call(file)
    except:
        return 1

def extract_zipfile(file: str, destination_path: str):
    from zipfile import ZipFile
    try:
        with ZipFile(file) as zip:
            zip.extractall(path=destination_path)
        return 0
    except:
        return 1
        
def install_tool(download: Download):
    print(f"Beginning download of {download.name}")
    file = download_file(download.url)
    print(f"download of {download.name} complete. Moving to installation with file {file}")
    match download.download_type:
        case DownloadType.INSTALLER:
            print(f"Running installer for {download.name}")
            success = run_installer(file)
        case DownloadType.ZIP:
            print(f"Unzipping {download.name} to \"{download.file_destination}\"")
            success = extract_zipfile(file, download.file_destination)
    print(f"installation of {download.name} completed with exit code={success}.")
    if success == 0:
        print(f"removing {file}")
        os.remove(file)

def is_user_admin():
    import ctypes
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def __main__():
    if is_user_admin():
        print("Must be run as administrator!")
        return
    parser = argparse.ArgumentParser(
        prog="QuickInstaller",
        description="Concurrent downloader and installer for batch installing programs",
    )
    parser.add_argument('-f', '--file', default="downloads.toml")
    parser.add_argument('-j', '--jobs', default=5)
    args = parser.parse_args()

    filename = args.file
    with open(filename, 'br') as file:
        download_info = tomllib.load(file)
    downloads = [Download(name=download.replace("_", " "), **download_info[download]) for download in download_info]

    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        executor.map(install_tool, downloads)

if __name__ == "__main__":
    __main__()
    
