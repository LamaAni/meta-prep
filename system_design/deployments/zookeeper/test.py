from datetime import datetime
import random
import threading
import time
from kazoo.client import KazooClient
from utils.logs import create_logger

zk = KazooClient(hosts="localhost:2181", read_only=False)
zk.start()


def delay(min, max, name="producer"):
    sleep_time = random.random() * (max - min) + min
    # print(f"{thread_name()}:{name}:sleep", sleep_time)
    time.sleep(sleep_time)


# Key value paid
def lock_thread(paths=["/test/a", "/test/b", "/test/c"]):
    # Zookeeper key value pair storage.
    log = create_logger(threading.current_thread().name)
    log.info("Started")
    for path in paths:
        zk.ensure_path(path)
    while True:

        path = random.choice(paths)
        ts = datetime.now()
        log.info("? Getting lock on " + path)
        with zk.Lock(path):
            log.info(f"Got lock on {path} in {datetime.now()-ts}")
            val = str(random.random())
            zk.set(path, val.encode("utf-8"))
            delay(0.1, 0.5)
            if zk.get(path)[0].decode("utf-8") != val:
                log.error("Invalid locked key get " + path)
            else:
                log.info("Set and get ok " + path)


if __name__ == "__main__":
    threads = [
        threading.Thread(target=lock_thread),
        threading.Thread(target=lock_thread),
        threading.Thread(target=lock_thread),
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
