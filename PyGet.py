# Imports #

from tqdm.auto import tqdm # For progressbar
import sys # For stderr, stdout, checking specs, etc.
import os # For creating folders
import argparse # For CLI
import requests # For getting manifest, code, etc.
from requests.exceptions import HTTPError # For get errors

# Constants #

# Variables #

# Functions #

# Get OS #
def getOS():
    if sys.platform == "darwin":
        return "MacOS"
    elif sys.platform == "linux" or sys.platform == "linux2":
        return "Linux"
    elif sys.platform == "win32":
        return "Windows"

# Manifest Decoder #
def getManifest(packageName):
    manifest = requests.get(f"https://raw.githubusercontent.com/RZ-Code-Studio/PyGet-Packages/main/{getOS()}/{packageName}/manifest.json")

    if manifest.status_code == 404:
        raise HTTPError("404: Package not Found")
    elif manifest.status_code == 400:
        raise HTTPError("400: Bad Request")
    elif manifest.status_code == 503:
        raise HTTPError("503: Internal Server Error")
    elif manifest.status_code == 204:
        raise HTTPError("204: Manifest is empty. Maybe the app is still in development?")
    elif manifest.status_code != 200:
        raise HTTPError(f"Unknown error. Status Code: {manifest.status_code}")
    else:
        return manifest.json()

# Install Function #
def install(manifest):
    pass

# Uninstall Function #
def uninstall(packageName):
    pass

# Combined function for CLI #
def CLI(packageName, operation, options):
    pass

# Check if packages directory exists if not #
if os.path.isdir(f"{os.environ['userprofile']}\\PyGet-Packages"):
    os.mkdir(f"{os.environ['userprofile']}\\PyGet-Packages")
    
# CLI initater #
parser = argparse.ArgumentParser(description="Cross-platform package manager")
parser.add_argument("packageName", type=str, default="", help="What is your package name?")
parser.add_argument("operation", type=str, default="", help="What is your operation?")
parser.add_argument("--", type=str, default="", help="What are the options?")

# Get Arguments #
args = parser.parse_args()

# Excute CLI #

CLI(args.packageName, args.operation)