import yaml

def load_config():
    with open("hitch.yaml", "r") as f:
        return yaml.safe_load(f)