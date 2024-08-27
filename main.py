import requests
import subprocess
from concurrent.futures import ThreadPoolExecutor

def download_file(url: str) -> str:
    response = requests.get(url, stream=True)
    if "content-disposition" in response.headers:
        content_disposition = response.headers['content-disposition']
        filename = content_disposition.split("filename=")[1]
        filename.replace(';', '')
    else:
        filename = url.split("/")[-1]
    
    print(f'beginning download of {filename=}')
    with open(filename, mode='wb') as file:
        for chunk in response.iter_content(chunk_size=10*1024):
            file.write(chunk)

    return filename

def install_tool(url: str):
    file = download_file(url)
    print(f"download of {file=} complete, moving to installation")
    process_return = subprocess.call(file)
    if process_return != 0:
        print(f"Error installing {file}")
    else:
        print(f"installation of {file=} complete")


urls = [
    'https://c2rsetup.officeapps.live.com/c2r/downloadVS.aspx?sku=community&channel=Release&version=VS2022&source=VSLandingPage&cid=2030:8e0a127f6b34482599782b1911928b9f', # Visual Studio
    'https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user', # VS Code
    'https://download.jetbrains.com/toolbox/jetbrains-toolbox-2.4.2.32922.exe', # JetBrains Toolbox
    'https://cdn.akamai.steamstatic.com/client/installer/SteamSetup.exe', # Steam
    'https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US', # Firefox
    'https://github.com/goatcorp/FFXIVQuickLauncher/releases/latest/download/Setup.exe', # XIVLauncher
    'https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x64', # Discord
    'https://downloads.malwarebytes.com/file/mb-windows', # MBAM
    'https://r2-app.eagle.cool/releases/Eagle-4.0-x64-build2.exe', # Eagle
    'https://github.com/obsidianmd/obsidian-releases/releases/latest/download/Obsidian-1.6.7.exe', # Obsidian
    'https://vault.bitwarden.com/download/?app=desktop&platform=windows', # Bitwarden
    'https://www.fosshub.com/qBittorrent.html?dwl=qbittorrent_4.6.6_x64_setup.exe', # qbittorrent
    'https://international.download.nvidia.com/Windows/broadcast/1.4.0.29/NVIDIA_Broadcast_v1.4.0.29.exe', # NVIDIA broadcast
    'https://rzr.to/synapse-new-pc-download-beta', # Razer Synapse
    'https://www.7-zip.org/a/7z2408-x64.exe', # 7-Zip
    'https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe', # Rust
] 

if __name__ == "__main__":
    print("starting downloads")
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(install_tool, urls)
