# import required libraries
from colorama import Fore as Colour
import os

def fatal(text: str, i: int = 1) -> None:
    print(Colour.RED + text + Colour.RESET)
    exit(i)

def error(text: str) -> None:
    print(Colour.LIGHTRED_EX + text + Colour.RESET)

def exp(path: str) -> str:
    return os.path.expanduser(path)

# get correct download directory
downloads = exp("~/downloads")
if not os.path.isdir(downloads):
    downloads = exp("~/Downloads") if os.path.isdir(exp("~/Downloads")) else ""
    if downloads == "":
        fatal("no download folder found.")
os.chdir(downloads) # change current directory to downloads

# get all files in downloads
files = os.listdir(downloads)
for x in files.copy():
    if os.path.isdir(f"{downloads}/{x}"):
        files.remove(x)
mapping: dict[str, list[str]] = {}
for f in files:
    ext = f.split(".")[-1]
    if mapping.get(ext) == None:
        mapping[ext] = []
    mapping[ext].append(f)

# move files and create appropriate directories
for extension, fs in mapping.items():
    if not os.path.isdir(extension):
        os.mkdir(extension)
    for file in fs:
        while file in os.listdir(f"{downloads}/{extension}"):
            error(f"file of name '{file}' already present in {extension}. enter a new name:")
            name = input("> ")
            if name != "":
                file = name
        os.rename(f"{downloads}/{file}", f"{downloads}/{extension}/{file}")

# correct any files that are in their wrong folders
for dir in os.listdir(downloads):
    for file in os.listdir(dir):
        if not file.endswith("."+dir):
            ext = file.split(".")[-1]
            if "." in file:
                if not os.path.isdir(f"{downloads}/{ext}"):
                    os.mkdir(f"{downloads}/{ext}")
                os.rename(f"{downloads}/{dir}/{file}", f"{downloads}/{ext}/{file}")
                error(f"'{file}' in '{dir}'; moved to '{downloads}/{ext}'.")
            else:
                os.rename(f"{downloads}/{dir}/{file}", f"{downloads}/{file}")
                error(f"'{file}' in '{dir}'; moved to '{downloads}'.")
            