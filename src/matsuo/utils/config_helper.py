import yaml

DEFAULT_CONFIG_FILE_PATH = "config/config.yaml"


def change_config_file_pat(file_path):
    global DEFAULT_CONFIG_FILE_PATH
    DEFAULT_CONFIG_FILE_PATH = file_path


def get_configs():
    with open(DEFAULT_CONFIG_FILE_PATH) as mf:
        return yaml.load(mf)


def get_config(*arg_path):
    config = get_configs()
    for arg in arg_path:
        arg = arg.lower()
        if arg not in config:
            raise ValueError('Arg {} not in {}. Arg path is {}'.format(arg, config, ','.join(arg_path)))
        config = config[arg]
    return config
