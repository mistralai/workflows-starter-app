import signal
import sys


def main():
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))
    print("discover worker started", flush=True)
    signal.pause()
