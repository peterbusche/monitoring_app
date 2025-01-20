# config.py
import yaml

def load_config(path):
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


def print_yaml():
    config_path = r"C:\Users\peter\Dropbox\LunaTest\monitoring_app\config\1.yaml"
    loaded_config = load_config(config_path)
    print("======YAML Loaded======")
    print(loaded_config)
    print("========================")

    