import toml
from sailor.utils.dirscan import find_path

config_name = "config.toml"
config_path = find_path(config_name)
config = toml.load(config_path)
