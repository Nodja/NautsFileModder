import os
import re

from animo.filetools import decrypt, encrypt, createandwrite
from animo.config import get_config

def mod_settings_file(file_path, settings):
    real_path = f"_env\\{file_path}"
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
    
    
def mod_settings():
    config = get_config()
    for section in config.sections():
        if section.startswith("settings="):
            file_path = section.split("=")[1]
            settings = []
            for key in config[section]:
                settings.append([key, config[section][key]])
            mod_settings_file(file_path, settings)
            
    