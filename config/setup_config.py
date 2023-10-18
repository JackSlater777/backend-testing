from os.path import abspath, dirname, exists
from vyper import v as configuration, Vyper


def setup_config(config_name="test_zone", config_path=f"{dirname(abspath(__file__))}/", config_type="yaml"):
    config_file = f"{config_path}{config_name}.{config_type}"

    if not exists(config_file):
        raise FileNotFoundError(f"Configuration file does not exist: {config_file}")

    configuration.set_config_file(config_file)
    configuration.read_in_config()

    setup_logger()
    setup_clients()
    setup_databases()
    setup_vault_credentials()

    return configuration


def setup_logger():
    pass


def get_team_extra_headers(config: Vyper) -> dict:
    # headers = {"app-name": "team-autotest"}
    # extra_headers = config.get("team.extra_headers")
    # if extra_headers:
    #     extra_headers.dict(item.split(":", 1) for item in extra_headers.lower().split(";"))
    #     headers.update(extra_headers)
    # return headers
    pass


def setup_clients():
    # SERVICE_URL_MAP = {}
    # SERVICE_URL_MAP.update(
    #     {
    #         "QueriesServiceOne": configuration.get("db.team.service_one")
    #     }
    # )
    pass


def setup_databases():
    # CLASS_DBNAME_MAP = {}
    # CLASS_DBNAME_MAP.update(
    #     {
    #         "QueriesServiceOne": configuration.get("db.team.service_one")
    #     }
    # )
    pass


def setup_vault_credentials():
    # environ["secret_test_zone_path"] = os.getenv("secret_test_zone_path") or configuration.get("project_path")
    pass
