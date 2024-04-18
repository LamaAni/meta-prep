from datetime import datetime
import random
import time
import pika
import threading
import json
import uuid
import pika.credentials
from logs import create_logger


queue = "tester"
run_id = str(uuid.uuid1())[:5]


class Message(dict):
    @property
    def run_id(self) -> str:
        return self.get("run_id", None)

    @property
    def idx(self) -> int:
        return self.get("idx", -1)

    @property
    def val(self) -> float:
        return self.get("val", None)

    @property
    def ts(self) -> datetime:
        return datetime.fromtimestamp(self.get("ts", 0))

    @property
    def uuid(self) -> str:
        return self.get("uuid", "?")


def delay(min, max, name="producer"):
    sleep_time = random.random() * (max - min) + min
    # print(f"{thread_name()}:{name}:sleep", sleep_time)
    time.sleep(sleep_time)


def producer_thread(queue=queue):
    log = create_logger(f"{threading.current_thread().name}", log_level="INFO")
    log.info("Started")

    idx = 0

    def post_message():
        nonlocal idx
        val = Message(
            val=random.random(),
            idx=idx,
            run_id=run_id,
            ts=datetime.now().timestamp(),
        )
        channel.basic_publish(
            "",
            queue,
            body=json.dumps(val),
        )
        log.info(f"Published {val}")
        idx += 1

    with pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            credentials=pika.credentials.PlainCredentials(
                username="admin",
                password="password",
            ),
        )
    ) as conn:
        channel = conn.channel()
        channel.queue_declare(queue)
        while True:
            delay(0.1, 2)
            for i in range(10):
                post_message()


recived = set()


def consumer_thread(queue=queue):
    log = create_logger(f"{threading.current_thread().name}", log_level="INFO")
    log.info("Started")
    with pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            credentials=pika.credentials.PlainCredentials(
                username="admin",
                password="password",
            ),
        )
    ) as conn:
        channel = conn.channel()
        channel.queue_declare(queue)
        for method, properties, body in channel.consume(queue=queue, auto_ack=True):
            message = Message(**json.loads(body))
            is_old = run_id != message.run_id
            if not is_old:
                if message.idx in recived:
                    log.error(f"DUPLICATE {message.idx}")
                else:
                    recived.add(message.idx)

            log.info(f"{'OLD' if is_old else 'cur'}-> {message}")
            delay(0.01, 0.2)


if __name__ == "__main__":
    threads = [
        threading.Thread(target=producer_thread, name="Prod 1"),
        threading.Thread(target=consumer_thread, name="Cons 1"),
        threading.Thread(target=consumer_thread, name="Cons 2"),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
