import glob
import json
import os
import shutil

import psutil

from animo.config import get_config



class GameEnvironmentError(Exception):
    pass

def create_dir(file):
    directory = os.path.dirname(file)
    if not os.path.exists(directory):
        os.makedirs(directory)

        
def create_and_link(src, dst):
    create_dir(dst)
    os.link(src, dst)
    

def kill_process():
    for proc in psutil.process_iter():
        if proc.name().lower() == "awesomenauts.exe":
            proc.kill()
            
            
def create_env():
    if os.path.isdir("_env"):
        shutil.rmtree("_env")
    
    config = get_config()
    game_paths = json.loads(config['env']['game_paths'])

    game_path = None
    for path in game_paths:
        if os.path.isfile(f"{path}\\awesomenauts.exe"):
            game_path = path
            break
            
    if game_path is None:
        raise GameEnvironmentError("Failed to find game directory.")
    else:
        print(f"Using {game_path}")
        
        
    file_structure = glob.glob(f"{game_path}/**", recursive=True)
    for path in file_structure:
        if not os.path.isfile(path):
            continue
        rel_path = os.path.relpath(path, game_path)
        create_and_link(path, f"_env\\{rel_path}")