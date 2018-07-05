import configparser
import os

config = None

class ConfigError(Exception):
    pass

def load_config():
    cfg_path = "nfm.cfg"
    if not os.path.isfile(cfg_path):
        raise ConfigError("No config file found.")
    
    _config = configparser.ConfigParser(delimiters='=')
    _config.optionxform=str
    _config.read(cfg_path)
    
    global config
    config = _config
    
def get_config():
    return config