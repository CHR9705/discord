import sqlite3
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config


class DBWatcher:
    def __init__(self, on_new_keys_callback):
        """on_new_keys_callback: a function to call with a list of new keys."""
        self.on_new_keys_callback = on_new_keys_callback
        self.last_seen_key = self._get_max_existing_key()
        self.observer = None

    def _get_max_existing_key(self):
        conn = sqlite3.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute(f"SELECT MAX({config.KEY_COLUMN}) FROM {config.TABLE_NAME}")
        result = cur.fetchone()[0]
        conn.close()
        return result if result is not None else 0

    def _get_new_keys(self):
        conn = sqlite3.connect(config.DB_PATH)
        cur = conn.cursor()
        cur.execute(
            f"SELECT {config.KEY_COLUMN} FROM {config.TABLE_NAME} WHERE {config.KEY_COLUMN} > ? ORDER BY {config.KEY_COLUMN} ASC",
            (self.last_seen_key,)
        )
        rows = cur.fetchall()
        conn.close()
        return [row[0] for row in rows]

    def check_for_updates(self):
        new_keys = self._get_new_keys()
        if new_keys:
            self.last_seen_key = new_keys[-1]
            self.on_new_keys_callback(new_keys)

    def start(self):
        print(f"Starting from key: {self.last_seen_key}")
        handler = _FileChangeHandler(self.check_for_updates)
        watch_dir = os.path.dirname(os.path.abspath(config.DB_PATH)) or "."
        self.observer = Observer()
        self.observer.schedule(handler, path=watch_dir, recursive=False)
        self.observer.start()
        print("Watching database for new records...")


class _FileChangeHandler(FileSystemEventHandler):
    def __init__(self, on_change_callback):
        self.on_change_callback = on_change_callback

    def on_modified(self, event):
        db_name = os.path.basename(config.DB_PATH)
        if event.src_path.endswith(db_name) or event.src_path.endswith(db_name + "-wal"):
            self.on_change_callback()