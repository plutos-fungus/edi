import sys
import re
import yaml
from yaml.loader import SafeLoader
# Handle the config-file
# Please

#========================= Viables and paths =========================#
def getOperators():
    config_file = 'configs/config.yml'
    language_files = 'configs/languages/'
    themes_files = 'configs/theme/'
    VI_mode_on = False
    language = ""

    #========================= opening the files =========================#
    try:
        with open(config_file, 'r') as config:
            config = yaml.load(config, Loader=SafeLoader)
            VI_mode = config['VI_mode']
            language = config['language']
            theme = config['theme']
    except FileNotFoundError: 
        VI_mode = "n"
        language = []
        theme = None # TODO: if no theme is set, don't run Themestuff.


    actualopperators = []
    opperators = []
    for i in language:
        if i is not None:
            #print(i)
            try: 
                with open(language_files + i, 'r') as language_config:
                    language_config = yaml.load(language_config, Loader=SafeLoader)
                    opperators = language_config['opperators']
                    #print("=== Language ===")
                    #print(language_files + i)
                    language = i
            except FileNotFoundError:
                pass 
    if len(opperators) != 0:
        for o in opperators:
            o = o + " "
            actualopperators.append(re.sub("^-{3}", " ", o))
        return actualopperators
    else: 
        return None 

def Themestuff():
    for i in theme:
        if i is not None:
            with open(themes_files + i, 'r') as themes:
                themes = yaml.load(themes, Loader=SafeLoader)
                colors = themes['colors']
                #print("=== theme ===")
                #print(themes_files + i)

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
