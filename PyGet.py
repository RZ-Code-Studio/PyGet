# Credits to stackoverflow users for dynamic progress bar and distros

# Imports #

import sys  # For stderr, stdout, checking specs, etc.
import os  # For creating folders
import argparse  # For CLI
from shutil import rmtree  # Deleting things
from tqdm.auto import tqdm  # For progressbar
import requests  # For getting manifest, code, etc.
from requests.exceptions import HTTPError  # For get errors
from charset_normalizer import detect  # Encodings

# Constants #

# Variables #

CURRENTVERSION = 1.0

# Functions #

# Get OS #


def get_os():
    """Gets Operating System

    Returns:
        str: OS
    """
    if sys.platform == "darwin":
        return "MacOS"
    if sys.platform == "linux" or sys.platform == "linux2":
        return "Linux"
    if sys.platform == "win32":
        return "Windows"


# Manifest Decoder #


def get_manifest(package_name):
    """Gets the manifest of a package

    Args:
        package_name (str): The name of the package

    Raises:
        HTTPError: 404
        HTTPError: 400
        HTTPError: 503
        HTTPError: 400
        HTTPError: Other

    Returns:
        dict: The json manifest transformed into a python object
    """
    if (
        requests.get(
            "https://raw.githubusercontent.com/To-Code-Or-Not-To-Code/"
            + f"PyGet-Packages/main/{get_os()}/PyGet/manifest.json",
            timeout=180,
        ).json()["version"]
        > CURRENTVERSION
    ):
        print(
            "There is a new version of PyGet now. You can update it with"
            + " pyget install pyget"
        )

    manifest = requests.get(
        "https://raw.githubusercontent.com/To-Code-Or-Not-To-Code" +
        f"/PyGet-Packages/main/{get_os()}/{package_name}/manifest.json",
        timeout=180
    )

    if manifest.status_code == 404:
        raise HTTPError(
            "404: Package not Found. Maybe you typed the wrong package?" +
            " The app could also not be ported to your enivorment yet"
        )
    if manifest.status_code == 400:
        raise HTTPError("400: Bad Request. That's my problem." +
                        " Try updating PyGet.")
    if manifest.status_code == 503:
        raise HTTPError("503: Internal Server Error")
    if manifest.status_code == 204:
        raise HTTPError(
            "204: Manifest is empty. Maybe the app is still in development?"
        )
    if manifest.status_code != 200:
        raise HTTPError(f"Unknown error. Status Code: {manifest.status_code}")
    else:
        return manifest.json()


# Install Function #


def install(manifest):
    """Installs a package

    Args:
        manifest (dict): The manifest
    """
    sources = manifest["sources"]
    priorities = []
    for i in sources:
        priorities.insert(i["priority"], i)

    for i in priorities:
        script_url = i["source"]
        size = int(requests.head(script_url, timeout=180).headers[
            "Content-Length"
        ])
        filename = script_url.split("/")[-1]

        if i["compile"] is False:
            with requests.get(script_url, timeout=180) as req, open(
                f"{os.path.expanduser('~')}/PyGet-Packages/{filename}",
                "wb",
                encoding=detect(req)["encoding"]
            ) as file, tqdm(
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                total=size,
                file=sys.stdout,
                desc=filename,
                size=25,
            ) as progress:
                for chunk in req.iter_content(chunk_size=1024):
                    datasize = file.write(chunk)
                    progress.update(datasize)
        else:
            with requests.get(script_url, timeout=180) as req, open(
                f"{os.path.expanduser('~')}/PyGet-Packages/{filename}",
                "w",
                encoding=detect(req)["encoding"]
            ) as file, tqdm(
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                total=size,
                file=sys.stdout,
                desc=filename,
                size=25,
            ) as progress:
                for chunk in req.iter_content(chunk_size=1024):
                    datasize = file.write(chunk)
                    progress.update(datasize)


# Uninstall Function #
def uninstall(package_name):
    """Uninstalls a package

    Args:
        package_name (str): Name of the package
    """
    rmtree(f"{os.path.expanduser('~')}/{package_name}")


# Combined function for CLI #


def CLI(package_name, operation):
    if operation == "install":
        install(get_manifest(package_name))
    else:
        uninstall(package_name)


# Check if packages directory exists if not #
if os.path.isdir(f"{os.path.expanduser('~')}/PyGet-Packages"):
    os.mkdir(f"{os.path.expanduser('~')}/PyGet-Packages")

# CLI initater #
parser = argparse.ArgumentParser(description="Cross-platform package manager")
parser.add_argument(
    "package_name", type=str, default="", help="What is your package name?"
)
parser.add_argument(
    "operation",
    type=str,
    default="",
    help="What is your operation?"
)

# Get Arguments #
args = parser.parse_args()

# Execute CLI #

CLI(args.package_name, args.operation)
