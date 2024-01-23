import requests
import allure
import json
from http import HTTPStatus
from config import configuration


class WiremockApi:
    def __init__(self):
        self.url = configuration.get("wiremock").get("address")

    def create_mapping(self, mock: dict):
        url = "/__admin/mappings"
        with allure.step(f"Creating a mock {mock.get('scenarioName')}"):
            with allure.step("POST request to the wiremock server"):
                response = requests.post(url=self.url+url, json=mock)
            with allure.step(f"Checking the mock creation: {response.status_code}"):
                assert response.status_code == HTTPStatus.CREATED, f"Unexpected status received: {response.status_code}"
            allure.attach(json.dumps(mock, ensure_ascii=False, indent=1), f"Mock {mock.get('scenarioName')}",
                          allure.attachment_type.JSON)

    def get_mapping_list(self):
        url = "/__admin/mappings"
        return requests.get(url=self.url+url).json()

    def delete_mapping_by_scenario_name(self, mock):
        url = "/__admin/mappings"
        mapping_list = self.get_mapping_list()['mappings']
        for mapping in mapping_list:
            if mapping.get('scenarioName') == mock['scenarioName'] and mapping.get('id'):
                with allure.step(f"Deleting the mock {mock['scenarioName']}"):
                    response = requests.delete(url=f'{self.url}{url}/{mapping["id"]}')
                with allure.step(f"Checking the mock deletion: {response.status_code}"):
                    assert response.status_code == HTTPStatus.OK, \
                        f"Unexpected status received: {response.status_code}"

    def get_requests_history_by_scenario_name(self, mock):
        url = "/__admin/requests"
        mapping_list = self.get_mapping_list()['mappings']
        for mapping in mapping_list:
            if mapping.get('scenarioName') == mock['scenarioName'] and mapping.get('id'):
                response = requests.get(url=f'{self.url}{url}?matchingStub={mapping["id"]}')
                return response.json()
