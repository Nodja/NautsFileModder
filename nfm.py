import os
import psutil
import subprocess
import time

from animo.config import get_config, load_config
from animo.env import create_env
from animo.mods import mod_settings
from animo.patcher import patch_game


if __name__ == "__main__":

    load_config()
    get_config()
    
    create_env()
    
    mod_settings()

    game = subprocess.Popen(r"_env\awesomenauts.exe", cwd="_env")
    proc = psutil.Process(game.pid)
    proc.suspend()

    patch_game()

    proc.resume()

    input("press enter to kill awesomenauts...")
    proc.kill()
