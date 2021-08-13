import sys
import re
import yaml
from yaml.loader import SafeLoader
# Handle the config-file
# Please

config_file = 'config.yml'
language_files = 'configs/language'
themes_files = 'configs/theme'

VI_mode_on = False

with open(config_file, 'r') as config:
    config = yaml.load(config, Loader=SafeLoader)
    language = ""
    VI_mode = config['VI_mode']
    language = config['language']
    theme = config['theme']

    print("=== Configs ===")
    for i in VI_mode:
        if i is not None:
            if i == "n" and i == "y":
                VI_mode_on = False
                break
            elif i == "y" and i != "n":
                print("VI mode? yes")
                VI_mode_on = True

            elif i == "n" and i != "y":
                print("VI mode? no")
                VI_mode_on = False

    for i in language:
        if i is not None:
            print(i)

    for i in theme:
        if i is not None:
            print(i)
