import os
import yaml
from os.path import abspath, dirname, exists
from dotenv import load_dotenv
from framework.models.exceptions.common import FileNotFound


# config.env
# USERNAME=admin
# PASSWORD=password123
# PAYLOAD=client_id=myid&password=abcd1234&grant_type=password&client_secret=mysecret&username=myname

# !!! WARNING !!!
# The string located above is used only for familiarization with login-types
# Don't keep the secrets in the .py-files!!!
# Information about credentials is located in config.env file and should be protected!
# Don't forget to add config.env-file to .gitignore


def get_config_path() -> str:
    return os.path.join(os.path.dirname(__file__), 'config.env')


def get_credentials_for_token() -> dict:
    """json login-type"""
    dotenv_path = get_config_path()
    load_dotenv(dotenv_path=dotenv_path)

    if os.path.exists(dotenv_path):
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD')
        return {
            "username": username,
            "password": password
        }
    else:
        raise FileNotFound(file_name=dotenv_path)


def get_credentials_for_bearer_token() -> str:
    """x-www-form-urlencoded login-type"""
    dotenv_path = get_config_path()
    load_dotenv(dotenv_path=dotenv_path)

    if os.path.exists(dotenv_path):
        return os.environ.get('PAYLOAD')
    else:
        raise FileNotFound(file_name=dotenv_path)


def setup_config(
        config_name: str = "config",
        config_path: str = f"{dirname(abspath(__file__))}/",
        config_type: str = "yaml",
        zone: str = "localhost"
) -> dict:
    """Считывание всех путей для запрошенной зоны из конфига"""
    config_file = f"{config_path}{config_name}.{config_type}"

    if not exists(config_file):
        raise FileNotFoundError(f"Configuration file does not exist: {config_file}")

    with open(config_file, "r") as file:
        configuration = yaml.safe_load(file)

    return configuration.get(zone)
