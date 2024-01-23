# import pytest
# from config.setup_config import setup_config


def pytest_addoption(parser) -> None:
    """Declaring the command-line options for test run"""
    parser.addoption("--env", default="localhost")


# Пример парсинга аргументов командной строки в фикстуре
# @pytest.fixture(scope="session")
# def setup_arguments(request) -> dict:
#     zone = request.config.getoption("--env")
#     if not zone or zone == "":
#         pytest.exit("Не указан параметр --env")
#     return setup_config(zone=zone)
