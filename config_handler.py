import sys
import re
import yaml
from yaml.loader import SafeLoader
# Handle the config-file
# Please

config_file = 'config.yml'
language_files = 'configs/languages/'
themes_files = 'configs/theme/'

VI_mode_on = False

with open(config_file, 'r') as config:
    config = yaml.load(config, Loader=SafeLoader)
    VI_mode = config['VI_mode']
    language = config['language']
    theme = config['theme']

    print("=== Configs ===")
    for i in VI_mode:
        if i is not None:

            if i == "y" and i != "n":
                #print("VI mode? yes")
                VI_mode_on = True

            elif i == "n" and i != "y":
                #print("VI mode? no")
                VI_mode_on = False

            elif i == "n" and i == "y":
                VI_mode_on = False
                break

for i in language:
    if i is not None:
        #print(i)
        with open(language_files + i, 'r') as language_config:
            language_config = yaml.load(language_config, Loader=SafeLoader)
            print(language_files + i)
            opperators = language_config['opperators']

for i in theme:
    if i is not None:
        pass
        #print(i)
