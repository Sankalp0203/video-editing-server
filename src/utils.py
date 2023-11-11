from yaml import load

def load_config_file():
    with open('resources/app.yaml', 'r') as file:
        config = load(file, Loader=yaml.FullLoader)
    return config
