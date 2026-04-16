"""Watch src/ for .py changes and auto-restart the workflow worker."""

import os
import signal
import subprocess
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

WATCH_DIR = os.path.join(os.path.dirname(__file__))
DEBOUNCE_SECONDS = 1.0


class _RestartHandler(FileSystemEventHandler):
    def __init__(self) -> None:
        self._last_trigger = 0.0
        self._needs_restart = False

    def on_any_event(self, event) -> None:  # type: ignore[override]
        if event.is_directory:
            return
        if any(part == "__pycache__" for part in event.src_path.split(os.sep)):
            return
        if getattr(event, "event_type", None) not in {"modified", "created", "deleted", "moved"}:
            return
        if not event.src_path.endswith(".py"):
            dest_path = getattr(event, "dest_path", "")
            if not dest_path.endswith(".py"):
                return
        now = time.monotonic()
        if now - self._last_trigger < DEBOUNCE_SECONDS:
            return
        self._last_trigger = now
        self._needs_restart = True

    def consume_restart(self) -> bool:
        if self._needs_restart:
            self._needs_restart = False
            return True
        return False


def _start_worker() -> subprocess.Popen:
    return subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(__file__), "discover.py")],
    )


def _stop_worker(proc: subprocess.Popen) -> None:
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def main() -> None:
    handler = _RestartHandler()
    observer = Observer()
    observer.schedule(handler, WATCH_DIR, recursive=True)
    observer.start()

    proc = _start_worker()
    print(f"[dev] Worker started (pid {proc.pid}). Watching {WATCH_DIR} for changes...")

    try:
        while True:
            time.sleep(0.3)
            if handler.consume_restart():
                print("[dev] Change detected, restarting worker...")
                _stop_worker(proc)
                proc = _start_worker()
                print(f"[dev] Worker restarted (pid {proc.pid}).")
            # If the worker crashed, stop and wait for a file change
            if proc.poll() is not None:
                print(f"[dev] Worker exited (code {proc.returncode}). Waiting for file changes to restart...")
                while not handler.consume_restart():
                    time.sleep(0.3)
                proc = _start_worker()
                print(f"[dev] Worker restarted (pid {proc.pid}).")
    except KeyboardInterrupt:
        print("\n[dev] Shutting down...")
        _stop_worker(proc)
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
