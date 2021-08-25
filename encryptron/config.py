# Note: File currently not included in installation

import os.path
from configparser import ConfigParser

def default_config():
    config = ConfigParser()
    config["Preferences"] = {
        "PyperclipIntegration": 'true'
    }
    config["Terminal"] = {
        "Prompt": 'default',
        "ClipboardModeDefault": 'off',
        "HISTORY_MAX_SIZE": 1000
    }
    config["whitespace_encryption"] = {
        "DefaultMixer": 'tribonacci'
    }
    return config


script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.dirname(script_dir)+"/crypt.ini"
if not os.path.isfile(config_path):
    default_config().write(config_path)

config = ConfigParser()

def load_config():
    config.read(config_path)

def save_config():
    config.write(config_path)
