import os
from dotenv import load_dotenv
from framework.models.exceptions.common import FileNotFound


# User for bearer_token token receiving

# config.env
# PAYLOAD=client_id=myid&password=abcd1234&grant_type=password&client_secret=mysecret&username=myname

# !!! WARNING !!!
# The string located above is used only for familiarization with x-www-form-urlencoded login-type
# Don't keep the secrets in the .py-files!!!
# Information about credentials is located in config.env file and should be protected!
# Don't forget to add config.env-file to .gitignore


def get_config_path() -> str:
    return os.path.join(os.path.dirname(__file__), 'config.env')


def get_credentials_for_token() -> dict:
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
    dotenv_path = get_config_path()
    load_dotenv(dotenv_path=dotenv_path)

    if os.path.exists(dotenv_path):
        return os.environ.get('PAYLOAD')
    else:
        raise FileNotFound(file_name=dotenv_path)


if __name__ == "__main__":
    print(get_credentials_for_token())
