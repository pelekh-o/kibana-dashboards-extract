from configparser import RawConfigParser, NoSectionError
import os


def get_config_section(section, config_file):
    config = RawConfigParser()
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config_file))
    config.read(path)
    try:
        configs_dict = dict(config.items(section))
    except NoSectionError:
        print(f'The {section} section cannot be found in the {config_file} config file.')
        exit(1)
    return configs_dict
