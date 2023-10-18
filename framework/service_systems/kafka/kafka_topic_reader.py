from framework.library.service_systems.kafka.kafka_reader import KafkaReader
from framework.models.kafka.message import some_topic
from retrying import retry


class KafkaTopicReader:
    def __init__(self, model, topic: str, max_message_count: int = 800, read_all_messages: bool = False):
        self.model = model
        self.topic = topic
        self.messages = None
        self.max_message_count = max_message_count
        self.read_all_messages = read_all_messages
        self.reader = KafkaReader(topic=self.topic, max_count=self.max_message_count)

    def get_messages(self) -> list:
        self.messages = self.reader.get_messages(model=self.model, read_all_messages=self.read_all_messages)
        return self.messages

    @retry(retry_on_result=lambda x: x == [], stop_max_attempt_number=2, wait_fixed=1000)
    def get_messages_by_param(self, param, with_reading: bool = True) -> list:
        if with_reading:
            return [message for message in self.get_messages() if message.param == param]
        else:
            return [message for message in self.messages if message.param == param]


if __name__ == "__main__":
    # Пример создания экземпляра топика
    some_topic_reader = KafkaTopicReader(
        model=some_topic,
        topic="some_topic",
        read_all_messages=True
    )
