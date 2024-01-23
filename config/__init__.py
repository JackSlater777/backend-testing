import sys
from config.setup_config import setup_config


def setup_arguments() -> dict:
    args = sys.argv
    for arg in args:
        if "--env=" in arg or "--env " in arg:
            config_name = arg[6:]
            return setup_config(zone=config_name)
    return setup_config(zone="localhost")


configuration = setup_arguments()
