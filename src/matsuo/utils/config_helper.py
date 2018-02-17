import yaml

DEFAULT_CONFIG_FILE_PATH = "config/config.yaml"


def change_config_file_pat(file_path):
    global DEFAULT_CONFIG_FILE_PATH
    DEFAULT_CONFIG_FILE_PATH = file_path


def get_configs():
    with open(DEFAULT_CONFIG_FILE_PATH) as mf:
        return yaml.load(mf)
