import yaml
from yaml.loader import SafeLoader
#Handle the config-file


with open('config.yml', 'r') as file:
    config = yaml.load(file, Loader=SafeLoader)
    print(config)
