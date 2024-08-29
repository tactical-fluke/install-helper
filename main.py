import requests
from concurrent.futures import ThreadPoolExecutor
from enum import Enum

class Download:
    class DownloadType(Enum):
        INSTALLER = 1
        ZIP = 2
        TARFILE = 3

    download_type = DownloadType.INSTALLER
    name = None
    url = None
    file_destination = None


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
    return subprocess.call(file)

def extract_zipfile(file: str, end_path: str):
    from zipfile import ZipFile
    try:
        with ZipFile(file) as zip:
            zip.extractall(path=end_path)
        return 0
    except:
        return 1
        
def install_tool(download: Download):
    print(f"Beginning download of {download.name}")
    file = download_file(download.url)
    print(f"download of {download.name} complete. Moving to installation with file {file}")
    match download.download_type:
        case Download.DownloadType.INSTALLER:
            print(f"Running installer for {download.name}")
            success = run_installer(file)
        case Download.DownloadType.ZIP:
            print(f"Unzipping {download.name} to \"{download.file_destination}\"")
            success = extract_zipfile(file, download.file_destination)
    print(f"installation of {download.name} completed with exit code={success}.")

tools = [
    Download(
        url='https://c2rsetup.officeapps.live.com/c2r/downloadVS.aspx?sku=community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030:8e0a127f6b34482599782b1911928b9f',
        name="Visual Studio"
    ),
    Download(
        url='https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user',
        name="Visual Studio Code"
    ),
    Download(
        url='https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.4.2.32922.exe',
        name="Jetbrains Toolbox"
    ),
    Download(
        url='https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe',
        name="Steam"
    ),
    Download(
        url='https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US',
        name="Firefox"
    ),
    Download(
        url='https://github.com/goatcorp/FFXIVQuickLauncher/releases/latest/download/Setup.exe',
        name="XIVLauncher"
    ),
    Download(
        url='https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64',
        name="Discord"
    ),
    Download(
        url='https://downloads.malwarebytes.com/file/mb-windows',
        name="Malwarebytes"
    ),
    Download(
        url='https://r2-app.eagle.cool/releases/Eagle-4.0-x64-build2.exe',
        name="Eagle"
    ),
    Download(
        url='https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian-1.6.7.exe',
        name="Obsidian"
    ),
    Download(
        url='https://vault.bitwarden.com/download/?app=desktop&platform=windows',
        name="Bitwarden"
    ),
    Download(
        url='https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent_4.6.6_x64_setup.exe',
        name="qbittorrent"
    ),
    Download(
        url='https://international.download.nvidia.com/Windows/broadcast/1.4.0.29/NVIDIA_Broadcast_v1.4.0.29.exe',
        name="NVIDIA Broadcast"
    ),
    Download(
        url='https://rzr.to/synapse-new-pc-download-beta',
        name="Razer Synapse"
    ),
    Download(
        url='https://www.7-zip.org/a/7z2408-x64.exe',
        name="7-Zip"
    ),
    Download(
        url='https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe',
        name="Rustup"
    ),
    Download(
        url='https://cdn-fastly.obsproject.com/downloads/OBS-Studio-30.2.3-Windows-Installer.exe',
        name="OBS Studio"
    ),
    Download(
        url='https://gitlab.com/CalcProgrammer1/OpenRGB/-/jobs/artifacts/master/download?job=Windows%2064',
        download_type=Download.DownloadType.ZIP,
        file_destination='C:\\Program Files\\',
        name="OpenRGB"
    ),
    Download(
        url='https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_11.1.2_build/ghidra_11.1.2_PUBLIC_20240709.zip',
        download_type=Download.DownloadType.ZIP,
        file_destination="C:\\ProgramFiles\\",
        name="Ghidra"
    ),
]

if __name__ == "__main__":
    print("starting downloads")
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(install_tool, tools)
