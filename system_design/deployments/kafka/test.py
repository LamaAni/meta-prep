import json
import threading
import kafka
import kafka.consumer
import kafka.producer
import random
import time
from datetime import datetime

from uuid import uuid1
import kafka.record
import kafka.record.default_records
import kafka.record.legacy_records
import kafka.record.memory_records

# import logging
# logging.basicConfig(level=logging.DEBUG)

kafka_server_params = dict(
    bootstrap_servers=["localhost:9092"],
)

topic = "test-queue2"

run_id = str(uuid1())


def thread_name():
    return threading.current_thread().name


def delay(min, max, name="producer"):
    sleep_time = random.random() * (max - min) + min
    # print(f"{thread_name()}:{name}:sleep", sleep_time)
    time.sleep(sleep_time)


def producer_thread(topic=topic):
    producer = kafka.KafkaProducer(
        **kafka_server_params,
        value_serializer=lambda x: json.dumps(x).encode("utf-8"),
        request_timeout_ms=1001,
    )
    idx = 0
    print("Started producer", thread_name())
    while True:
        try:
            key = ("a" if random.random() < 0.5 else "b").encode("utf-8")
            val = {
                "val": random.random(),
                "ts": datetime.now().timestamp(),
                "idx": idx,
                "uid": run_id,
            }
            idx += 1
            print(f"-> producing {topic}:{key.decode('utf-8')} {val}")
            producer.send(
                topic=topic,
                # key=key,
                value=val,
            )
        except Exception as ex:
            print("Failed to produce", ex)
            raise ex

        delay(0.1, 3, "producer")


processed = set()


def consumer_thread(topic=topic):
    id = thread_name()

    print("Started consumer", thread_name())

    consumer = kafka.KafkaConsumer(
        **kafka_server_params,
        auto_offset_reset="latest",  # Read from where we left off.
        group_id=topic,
        max_poll_records=1,
        enable_auto_commit=False,
        # max_poll_interval_ms=10,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    consumer.subscribe([topic])

    while True:
        delay(0.01, 0.1, "consumer")
        topics_and_messages = consumer.poll(1000)
        # consumer.commit(topics_and_messages)
        for topic, messages in topics_and_messages.items():
            for message in messages:
                meta = consumer.partitions_for_topic(message.topic)
                partition = kafka.TopicPartition(message.topic, message.partition)
                offsets = kafka.OffsetAndMetadata(message.offset + 1, meta)
                options = {partition: offsets}
                consumer.commit(offsets=options)

                if message is None:
                    raise Exception(f"Timeout on thread {id}")
                is_old = (
                    "current" if message.value.get("uid", None) == run_id else "OLD"
                )
                ts = datetime.fromtimestamp(message.value.get("ts", 0))
                idx = message.value.get("idx", -1)
                if idx in processed:
                    print("ERROR: Multi processed")
                processed.add(idx)
                val = message.value.get("val", None)
                key = "" if message.key is None else message.key.decode("utf-8")
                print(
                    "<-",
                    f"Consumer {id}, got {is_old}:",
                    f"{message.topic}:{key} idx:{idx} val:{val} ts:{ts}",
                )

    print(f"Consumer {idx} ended")


if __name__ == "__main__":
    threads = [
        threading.Thread(target=producer_thread),
        threading.Thread(target=consumer_thread),
        threading.Thread(target=consumer_thread),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
