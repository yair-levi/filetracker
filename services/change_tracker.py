import time
from os import listdir
from os import stat
from os.path import isfile, join
from services.producer import Producer
import json
import copy
import logging
import pickle
import hashlib
from pathlib import Path


class ChangeTracker:
    def __init__(self, tracked_dir: str, producer: Producer):
        self.tracked_dir = tracked_dir
        self.tracked_dir_md5 = hashlib.md5(self.tracked_dir.encode('utf-8')).hexdigest()
        self.path = Path(self.tracked_dir_md5)
        self.producer = producer
        self.last_snapshot: dict = self._start_app_snapshot()

    def _start_app_snapshot(self):
        if self.path.is_file():
            with open(self.path.resolve(), "rb") as f:
                state = pickle.load(f)
        else:
            state = {}
            self._create_snapshot_file(state)
        return state

    def _create_snapshot_file(self, state):
        with open(self.path.resolve(), "wb") as f:
            pickle.dump(state, f)

    def _directory_snapshot(self) -> dict:
        """
        snapshot is dictionary with file name as key and last modify timestamp as value.
        :return:
        snapshot(dict)
        """
        return {file_name: stat(join(self.tracked_dir, file_name)).st_mtime for file_name in listdir(self.tracked_dir)
                if isfile(join(self.tracked_dir, file_name))}

    def _get_changes(self) -> tuple:
        """
        Returns file changes in directory,
        snapshot is dictionary with file name as key and last modify timestamp as value,
        the function using last directory snapshot and current snapshot to track if there are any changes,
        1. modified - going over current snapshot and check if file exist in last snapshot and change time is not same
        2. added - going over current snapshot and check if file are not exist in last snapshot
        3. removed - going over last snapshot and check if file are not exist in current snapshot

        # we're filtering out all the changes on files with "_DUP_#"

        :return:
        changes(tuple): added, modified, removed
        """

        modified = []
        added = []

        current_snapshot = self._directory_snapshot()

        for k, v in current_snapshot.items():
            if (self.last_snapshot.get(k, None) is not None) and (self.last_snapshot.get(k, None) != v):
                modified.append(k)

            elif self.last_snapshot.get(k, None) is None:
                added.append(k)

        removed = [f for f in self.last_snapshot.keys() if f not in current_snapshot.keys()]

        self.last_snapshot = copy.copy(current_snapshot)
        self._create_snapshot_file(self.last_snapshot)

        # filtering out all files with "_DUP_#"
        added = [f for f in added if "_DUP_#" not in f]
        modified = [f for f in modified if "_DUP_#" not in f]
        removed = [f for f in removed if "_DUP_#" not in f]

        return added, modified, removed

    def start(self):
        """
        here we start the main loop that tracking the changes every 1 sec,
        if there are any changes message will produce with all changes
        produce: dictionary with added, modified, removed as a key and list of file name that change as a value
        """
        while True:
            time.sleep(1)
            added, modified, removed = self._get_changes()
            if len(added) == 0 and len(modified) == 0 and len(removed) == 0: continue
            changes = {
                "added": added,
                "modified": modified,
                "removed": removed
            }
            logging.info(changes)
            print(changes)
            self.producer.send(json.dumps(changes))
