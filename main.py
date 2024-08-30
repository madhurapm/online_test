import os
import json
import yaml
import configparser

class ConfigParser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = {}

    def read_yaml(self):
        with open(self.file_path, 'r') as f:
            self.config = yaml.safe_load(f)

    def read_cfg(self):
        config = configparser.ConfigParser()
        config.read(self.file_path)
        self.config = {section: dict(config.items(section)) for section in config.sections()}

    def read_conf(self):
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                self.config[key] = value

    def generate_flat_dict(self):
        flat_dict = {}
        for key, value in self.config.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flat_dict[f"{key}.{sub_key}"] = sub_value
            else:
                flat_dict[key] = value
        return flat_dict

    def write_env(self, flat_dict):
        with open('.env', 'w') as f:
            for key, value in flat_dict.items():
                f.write(f"{key}={value}\n")

    def write_json(self, flat_dict):
        with open('config.json', 'w') as f:
            json.dump(flat_dict, f)

    def set_os_env(self, flat_dict):
        for key, value in flat_dict.items():
            os.environ[key] = value

def main():
    parser = ConfigParser('config.yaml')
    parser.read_yaml()
    flat_dict = parser.generate_flat_dict()
    parser.write_env(flat_dict)
    parser.write_json(flat_dict)
    parser.set_os_env(flat_dict)

if __name__ == '__main__':
    main()
    
