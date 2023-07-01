# Credits to stackoverflow users for dynamic progress bar and distros

# Imports #

from tqdm.auto import tqdm  # For progressbar
import sys  # For stderr, stdout, checking specs, etc.
import os  # For creating folders
import argparse  # For CLI
import requests  # For getting manifest, code, etc.
from requests.exceptions import HTTPError  # For get errors

# Constants #

# Variables #

# Functions #

# Get OS #


def getOS():
    if sys.platform == "darwin":
        return "MacOS"
    elif sys.platform == "linux" or sys.platform == "linux2":
        return "Linux"
        import distro # Import to get what it is based off of
    elif sys.platform == "win32":
        return "Windows"

# Manifest Decoder #


def getManifest(packageName):
    manifest = requests.get(
        f"https://raw.githubusercontent.com/To-Code-Or-Not-To-Code/PyGet-Packages/main/{getOS()}/{packageName}/manifest.json")

    if manifest.status_code == 404:
        raise HTTPError("404: Package not Found. Maybe you typed the wrong package? The app could also not be ported to your enivorment yet")
    elif manifest.status_code == 400:
        raise HTTPError("400: Bad Request")
    elif manifest.status_code == 503:
        raise HTTPError("503: Internal Server Error")
    elif manifest.status_code == 204:
        raise HTTPError(
            "204: Manifest is empty. Maybe the app is still in development?")
    elif manifest.status_code != 200:
        raise HTTPError(f"Unknown error. Status Code: {manifest.status_code}")
    else:
        return manifest.json()

# Install Functions #


def installWindows(manifest):
    scriptURL = manifest["source"]
    size = int(requests.head(scriptURL).headers["Content-Length"])
    filename = scriptURL.split("/")[-1]

    with requests.get(scriptURL) as r, open(f"{os.path.expanduser('~')}\\PyGet-Packages\\{filename}") as f, tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        total=size,
        file=sys.stdout,
        desc=filename,
        size=25
    ) as progress:
        for chunk in r.iter_content(chunk_size=1024):
            datasize = f.write(chunk)
            progress.update(datasize)

def installMac(manifest):
    pass

def installLinux(manifest):
    basedOff = distro.like().lower()
    if basedOff == "slackware":
        pass
    elif basedOff == "debian":
        os.path.expanduser("~")
    elif basedOff == "arch":
        pass
    elif basedOff == "redHat":
        pass
    else:
        sys.stderr.write("Distro Not Supported")
        sys.stderr.flush()

def install(manifest, os):
    if os == "win":
        installWindows(manifest)
    elif os == "mac":
        installMac(manifest)
    elif os == "linux":
        installLinux(manifest)


# Uninstall Function #
def uninstall(packageName):
    pass

# Combined function for CLI #


def CLI(packageName, operation, options):
    pass


# Check if packages directory exists if not #
if os.path.isdir(f"{os.path.expanduser('~')}\\PyGet-Packages"):
    os.mkdir(f"{os.path.expanduser('~')}\\PyGet-Packages")

# CLI initater #
parser = argparse.ArgumentParser(description="Cross-platform package manager")
parser.add_argument("packageName", type=str, default="",
                    help="What is your package name?")
parser.add_argument("operation", type=str, default="",
                    help="What is your operation?")
parser.add_argument("--", type=str, default="", help="What are the options?")

# Get Arguments #
args = parser.parse_args()

# Execute CLI #

CLI(args.packageName, args.operation)
