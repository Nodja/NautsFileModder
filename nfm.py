import os
import psutil
import subprocess
import time

from animo.config import get_config, load_config
from animo.env import create_env, kill_process
from animo.mods import mod_settings, mod_simple_files
from animo.patcher import patch_game


if __name__ == "__main__":

    load_config()
    
    kill_process()
    create_env()
    
    mod_settings()
    mod_simple_files()

    game = subprocess.Popen(r"_env\awesomenauts.exe", cwd="_env")
    proc = psutil.Process(game.pid)
    proc.suspend()

    patch_game()

    proc.resume()

    input("press enter to kill awesomenauts...")
    proc.kill()
