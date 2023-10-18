import allure
import requests
import json
from http import HTTPStatus


class RabbitMqApi:
    def __init__(self, url: str, auth: tuple, vhost: str = None, queue: str = None, exchange: str = None):
        self.url = url
        self.auth = auth
        self.vhost = vhost
        self.queue = queue
        self.exchange = exchange

    @allure.step("Сreate instances in definitions")
    def create_instances(self, definitions: dict):
        """Сreate instances in definitions"""
        requests.post(
            url=f"{self.url}/api/definitions",
            json=definitions,
            auth=self.auth
        )

    @allure.step("Delete the queue")
    def delete_queue(self):
        """Delete the queue: /api/queues/vhost/name"""
        requests.delete(
            url=f"{self.url}/api/queues/{self.vhost}/{self.queue}",
            auth=self.auth
        )

    @allure.step("Delete the exchange")
    def delete_exchange(self):
        """Delete the exchange: /api/exchanges/vhost/name"""
        requests.delete(
            url=f"{self.url}/api/exchanges/{self.vhost}/{self.exchange}",
            auth=self.auth
        )

    @allure.step("Purge the queue")
    def purge_queue(self):
        """Purge the queue: /api/queues/vhost/name/contents"""
        requests.delete(
            url=f"{self.url}/api/queues/{self.vhost}/{self.queue}/contents",
            auth=self.auth
        )

    @allure.step("Publish a message")
    def publish_message_to_exchange(self, body: dict or list):
        """Publish a message: /api/exchanges/vhost/name/publish"""
        encoded_message = json.dumps(body["payload"])
        body["payload"] = encoded_message
        with allure.step("Check the exchange existance"):
            response = requests.get(
                url=f"{self.url}/api/exchanges/{self.vhost}/{self.exchange}",
                auth=self.auth
            )
            if response.status_code == HTTPStatus.OK:
                response = requests.post(
                    url=f"{self.url}/api/exchanges/{self.vhost}/{self.exchange}/publish",
                    json=body,
                    auth=self.auth
                )
                return response.json()

    @allure.step("Get a message from the queue")
    def get_message_from_queue(self, searching_params: dict):
        """Get a message from the queue: /api/queues/vhost/name/get"""
        response = requests.post(
            url=f"{self.url}/api/queues/{self.vhost}/{self.queue}/get",
            json={
                "count": 5,  # Maximum message count
                "ackmode": "ack_requeue_true",  # ackmod: true - returns a message into the queue, false - removes a message
                "encoding": "auto"  # Encoding: auto - utf-8, else - "base64"
                # "truncate": 50000  # Optional. If a message weight is bigger than 50000 bytes, it's cut down
            },
            auth=self.auth
        )
        if len(response.json()) == 0:
            return None
        else:
            for message in response.json():
                decoded_message = json.loads(message["payload"])
                message["payload"] = decoded_message
                for key, value in searching_params.items():
                    print(key, value)
                    if message["payload"].get(key) == value:
                        return message["payload"]
