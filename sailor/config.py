import toml
from utils import dirscan

config_name = "config.toml"
config_path = dirscan.find_path(config_name)
config = toml.load(config_path)
