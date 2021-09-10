import sys
import re
import yaml
import os 
from globalDefinitions import *
from yaml.loader import SafeLoader
# Handle the config-file
# Please
fileendings = os.path.expanduser('~/.config/edi/files.yml')
#========================= Viables and paths =========================#
def getSyntax(filename):
    config_file = os.path.expanduser('~/.config/edi/config.yml')
    language_files = os.path.expanduser('~/.config/edi/languages/')
    VI_mode_on = False
    language = ""
    ending = ""

    #========================= opening the files =========================#
    try:
        with open(config_file, 'r') as config:
            config = yaml.load(config, Loader=SafeLoader)
            VI_mode = config['VI_mode']
    except FileNotFoundError: 
        VI_mode = "n"
        language = []


    actualopperators = []
    opperators = []
    if re.search(".*\.py", filename): #TODO: Implement dictionary switch 
        language = "python"

    try: 
        with open(os.path.expanduser("~/.config/edi/languages/python.yml"), 'r') as language_config: # ~/.config/edi/files.ymlpython
            language_config = yaml.load(language_config, Loader=SafeLoader)
            opperators = language_config['opperators']
            #print("=== Language ===")
            #print(language_files + i)
    except FileNotFoundError:
        pass 
    if len(opperators) != 0:
        for o in opperators:
            o = o + " "
            actualopperators.append(re.sub("^-{3}", " ", o))
        return actualopperators
    else: 
        opperators.append(None)
        return opperators

def Themestuff():
    myColors = Themergb(os.path.expanduser('~/.config/edi/theme.yml')) # The argument passed into theme rgb is the path to the theme file. Should be ~/.config/edi/theme.yml once everything has been adjusted
    return myColors
    # configs/theme/theme.yml

def Endings():
    with open(fileendings, 'r') as endings:
        endings = yaml.load(endings, Loader=SafeLoader)
        files = endings['files']


#========================= Setting VI mode =========================#
def vimode():
    for i in VI_mode:
        if i is not None:
            #print("=== VI mode ===")
            if i == "y" and i != "n":
                #print("VI mode? yes")
                VI_mode_on = True

            elif i == "n" and i != "y":
                #print("VI mode? no")
                VI_mode_on = False

            elif i == "n" and i == "y":
                VI_mode_on = False
                break
Themestuff()