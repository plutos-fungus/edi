import yaml
from yaml.loader import SafeLoader
# Handle the config-file
# Please
class config_handling:
    config_file = 'config.yml'
    themes_files = 'configs/theme'
    language_files = 'configs/language'

    with open(config_file, 'r') as config:
        config = yaml.load(config, Loader=SafeLoader)
        language = config['language']
        theme = config['theme']

        print("=== string ===")
        print(config)
        print(language)
        print(theme)
