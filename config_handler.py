import sys
import re
import yaml
from globalDefinitions import *
from yaml.loader import SafeLoader
# Handle the config-file
# Please
fileendings = 'configs/fileendings/files.yml'
theme = []
themes_files = 'configs/theme/'
#========================= Viables and paths =========================#
def getSyntax(filename):
    global theme
    config_file = 'configs/config.yml'
    language_files = 'configs/languages/'
    VI_mode_on = False
    language = ""
    ending = ""

    #========================= opening the files =========================#
    try:
        with open(config_file, 'r') as config:
            config = yaml.load(config, Loader=SafeLoader)
            VI_mode = config['VI_mode']
            theme = config['theme']
    except FileNotFoundError: 
        VI_mode = "n"
        language = []
        theme.append(None) # TODO: if no theme is set, don't run Themestuff.


    actualopperators = []
    opperators = []
    if re.search(".*\.py", filename): #TODO: Implement dictionary switch 
        language = "python"

    try: 
        with open(language_files + language + ".yml", 'r') as language_config:
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
    global theme
    myColors = Themergb(themes_files, theme)
    return myColors

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