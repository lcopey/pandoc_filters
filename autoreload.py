import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Handler(FileSystemEventHandler):
    def __init__(self, root: str, patterns: str | list[str]):
        if isinstance(patterns, str):
            patterns = [patterns]
        self.root = root
        self.patterns = patterns
        self.last_modified = datetime.now()

    def in_patterns(self, src_path: str):
        abs_path = [Path(self.root) / filter_ for filter_ in self.patterns]
        for pattern in abs_path:
            if Path(src_path).match(str(pattern)):
                return True
        return False

    def on_modified(self, event):
        delta = datetime.now() - self.last_modified
        if delta > timedelta(seconds=1) and self.in_patterns(event.src_path):
            self.last_modified = datetime.now()
            _in = "./docs/source/base.md"
            _f = "markdown"
            _filter = "./src/filter.py"
            _out = "./docs/builds/test"
            _r = "../docs/source/"

            pandoc_exec(_in, _f, "json", _filter, _out, _r)
            pandoc_exec(_in, _f, "html", _filter, _out, _r)


def pandoc_exec(
    _in: str, _f: str, _t: str, _filter: str, _out: str, _resource: str = None
):
    os.system(
        f"pandoc {_in} -f {_f} -t {_t} --filter={_filter} --resource-path={_resource} -s -o {_out}.{_t}"
    )


class Watcher:
    def __init__(self, root=".", filters: str | list[str] | None = None):
        self.observer = Observer()
        self.handler = Handler(root=root, patterns=filters)
        self.directory = root

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


if __name__ == "__main__":
    source_watcher = Watcher("./", filters=["src/*.py", "docs/source/*.*"])
    source_watcher.run()
