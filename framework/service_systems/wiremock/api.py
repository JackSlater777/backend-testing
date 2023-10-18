import requests
import allure
import json
from http import HTTPStatus
from env_vars import WIREMOCK_BASE_URL


class WiremockApi:
    @staticmethod
    def create_mapping(mock: dict):
        url = "/__admin/mappings"
        with allure.step(f"Creating a mock {mock.get('scenarioName')}"):
            with allure.step("POST request to the wiremock server"):
                response = requests.post(url=WIREMOCK_BASE_URL+url, json=mock)
            with allure.step(f"Checking the mock creation: {response.status_code}"):
                assert response.status_code == HTTPStatus.CREATED, f"Unexpected status received: {response.status_code}"
            allure.attach(json.dumps(mock, ensure_ascii=False, indent=1), f"Mock {mock.get('scenarioName')}",
                          allure.attachment_type.JSON)

    @staticmethod
    def get_mapping_list():
        url = "/__admin/mappings"
        return requests.get(url=WIREMOCK_BASE_URL+url).json()

    @staticmethod
    def delete_mapping_by_scenario_name(mock):
        url = "/__admin/mappings"
        mapping_list = WiremockApi.get_mapping_list()['mappings']
        for mapping in mapping_list:
            if mapping.get('scenarioName') == mock['scenarioName'] and mapping.get('id'):
                with allure.step(f"Deleting the mock {mock['scenarioName']}"):
                    response = requests.delete(url=f'{WIREMOCK_BASE_URL}{url}/{mapping["id"]}')
                with allure.step(f"Checking the mock deletion: {response.status_code}"):
                    assert response.status_code == HTTPStatus.OK, \
                        f"Unexpected status received: {response.status_code}"

    @staticmethod
    def get_requests_history_by_scenario_name(mock):
        url = "/__admin/requests"
        mapping_list = WiremockApi.get_mapping_list()['mappings']
        for mapping in mapping_list:
            if mapping.get('scenarioName') == mock['scenarioName'] and mapping.get('id'):
                response = requests.get(url=f'{WIREMOCK_BASE_URL}{url}?matchingStub={mapping["id"]}')
                return response.json()
