import configparser
import glob
import os
import re

from animo.filetools import decrypt, encrypt, deflate, createandwrite
from animo.config import get_config


def mod_all():
    mod_files = glob.glob(f"mods/**/*.nfm", recursive=True)
    
    settings_files = {}
    simple_files = {}
    
    for file in mod_files:
        print(f"Parsing mod {file}")
        _config = configparser.ConfigParser(delimiters='=')
        _config.optionxform=str
        _config.read(file)
        
        
        for section in _config.sections():
            if section.startswith("settings="):
                file_path = section.split("=")[1]

                for key in _config[section]:
                    _setting = [key, _config[section][key]]
                    settings_files.setdefault(file_path, []).append(_setting)
                

                

            if section.startswith("file="):
                file_path = section.split("=")[1]
                replace_with = _config[section]['replace_with']
                encrypt_data = True 
                if _config[section].get('encrypt', 'yes').lower() in ['no', '0', 'false']:
                    encrypt_data = False
                    
                simple_files[file_path] = [replace_with, encrypt_data]
    
    for file in settings_files:
        file_path = file
        settings = settings_files[file]
        mod_settings_file(file_path, settings)
    
    for file in simple_files:
        file_path = file
        replace_with = simple_files[file][0]
        encrypt_data = simple_files[file][1]
        
        mod_simple_file(file_path, replace_with, encrypt_data)

def mod_settings_file(file_path, settings):
    real_path = f"_env\\{file_path}"
    print(f"Modding {real_path}")
    data_in = open(real_path, "rb").read()
    decrypt_path = file_path.lower()
    data_out = decrypt(data_in, decrypt_path)
    
    for setting in settings:
        expression = str.encode(f"^({setting[0]}) = (.*)$")
        replace_with = str.encode(f"{setting[0]} = {setting[1]}")
        data_out = re.sub(expression, replace_with, data_out, flags=re.I|re.M)
    
    data_encrypted = encrypt(data_out, decrypt_path)
    
    os.remove(real_path)
    open(real_path, 'wb').write(data_encrypted)
    
    
            
def mod_simple_file(file_path, replace_with, encrypt_data=True):
    real_path = f"_env\\{file_path}"
    print(f"Modding {real_path}")
    decrypt_path = file_path.lower()
    
    file_data = open(replace_with, "rb").read()
    if encrypt_data:
        data_out = encrypt(file_data, decrypt_path)
    else:
        data_out = deflate(file_data)
    
    os.remove(real_path)
    open(real_path, 'wb').write(data_out)
    