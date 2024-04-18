import sys
import signal

global WAS_STOPPED
WAS_STOPPED = False


def handle(sig, frame):
    global WAS_STOPPED
    WAS_STOPPED = True


signal.signal(signal.SIGTERM, handle)
# signal.signal(signal.SIGKILL, handle)s

signal.pause()
print("Exited")
