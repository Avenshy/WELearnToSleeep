import os

NAME = "WELearnToSleeep"
VERSION = "0.3.0"

os.system(f"pyinstaller -F --name {NAME}.{VERSION} ./src/main.py  ")
