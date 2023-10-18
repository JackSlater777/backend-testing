from config.setup_config import setup_config
import sys


default_config_name = "test_zone"


def pytest_addoption(parser):
    parser.addoption('--env', default=default_config_name)


def setup_configuration():
    args = sys.argv
    for arg in args:
        if "--env=" in arg or "--env " in arg:
            config_name = arg[6:]
            return setup_config(config_name=config_name)
    return setup_config(config_name=default_config_name)


configuration = setup_configuration()
