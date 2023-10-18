import collections
import json
from dacite import from_dict
from vyper import v as configuration
from kafka import KafkaConsumer, TopicPartition

KafkaRecord = collections.namedtuple("KafkaRecord", "key message timestamp")


class KafkaReader:
    def __init__(self, topic, bootstrap_servers=None, max_records=100, timeout_ms=2000, max_count=3000):
        bootstrap_servers = bootstrap_servers or configuration.get("kafka_servers")
        self._consumer = KafkaConsumer(
            bootstrap_servers=bootstrap_servers, auto_offset_reset="latest", consumer_timeout_ms=timeout_ms
        )
        partitions = self._consumer.partitions_for_topic(topic)
        if not partitions:
            raise RuntimeError(f"There is no partitions found for: {topic}")
        self._parts = [TopicPartition(topic, p) for p in partitions]
        self._consumer.assign(self._parts)
        self.max_records = max_records
        self.timeout_ms = timeout_ms
        self.max_count = max_count

    def seek_back(self):
        begins = self._consumer.beginning_offsets(self._parts)
        for part in self._parts:
            desired = self._consumer.position(part) - self.max_records
            self._consumer.seek(part, desired if desired > begins[part] else begins[part])

    def poll_messages(self, raw: bool = False, read_all_messages: bool = False) -> list:
        self.seek_back()
        records = []
        while True:
            print(f"Polling kafka messages for '{self._parts[0].topic}'...")
            answer = self._consumer.poll(timeout_ms=self.timeout_ms)
            if not answer:
                break
            if raw:
                records += [KafkaRecord(rec.key, rec.value, rec.timestamp) for recs in answer.values() for rec in recs]
            else:
                records += [
                    KafkaRecord(rec.key, json.loads(rec.value.decode()), rec.timestamp)
                    for recs in answer.values()
                    for rec in recs
                ]
            if len(records) > self.max_count:
                break
        res = sorted(records, key=lambda x: x.timestamp, reverse=True)
        if read_all_messages:
            return res
        return res[:self.max_records]

    def get_messages(self, model, read_all_messages: bool = False) -> list:
        messages = []
        records = self.poll_messages(read_all_messages=read_all_messages)
        for record in records:
            messages.append(model.Message(**record.message))
        return messages

    def get_messages_from_dict(self, model, read_all_messages: bool = False) -> list:
        """Allow to parse messages with skipping corrupting fields (e.g. '$type')"""
        messages = []
        records = self.poll_messages(read_all_messages=read_all_messages)
        for record in records:
            messages.append(from_dict(data_class=model.Message, data=record.message))
        return messages

    def get_keys(self) -> list:
        return [int(record.key.decode()) for record in self.poll_messages() if record.key]

    def get_messages_by_key(self, model, key) -> list:
        messages = self.poll_messages()
        return [
            model.Mesage(**record.message) for record in messages if record.key and int(record.key.decode()) == key
        ]

    def get_messages_by_keys(self, model, keys: list[int]) -> list:
        messages = self.poll_messages()
        return [
            model.Mesage(**record.message) for record in messages if record.key and int(record.key.decode()) in keys
        ]
