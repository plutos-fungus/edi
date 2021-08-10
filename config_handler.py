import yaml
from yaml.loader import SafeLoader
# Handle the config-file
# please

config_file = 'config.yml'
themes = 'configs/theme'
language_files = 'config/language'

with open(config_file, 'r') as config:
    config = yaml.load(config, Loader=SafeLoader)
    language = config['language']
    theme = config['theme']

with open()

    print(config)
    print(language)
    print(theme)
