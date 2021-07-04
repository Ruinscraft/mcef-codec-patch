import sys
import os
from pathlib import Path

def find_minecraft():
    home_dir = str(Path.home())
    minecraft_path = ""

    if sys.platform == "linux":
        if os.path.isdir(os.path.join(home_dir, ".minecraft")):
            minecraft_path = os.path.join(home_dir, ".minecraft")
    elif sys.platform == "darwin":
        if os.path.isdir(os.path.join(home_dir, "Library", "Application Support", "minecraft")):
            minecraft_path = os.path.join(home_dir, "Library", "Application Support", "minecraft")
    elif sys.platform == "win32":
        app_data_dir = os.getenv("APPDATA")
        if app_data_dir:
            if os.path.isdir(os.path.join(app_data_dir, ".minecraft")):
                minecraft_path = os.path.join(app_data_dir, ".minecraft")
    
    return minecraft_path
