import hashlib
import unittest
from services.change_tracker import ChangeTracker
from pathlib import Path


class TestChangeTracker(unittest.TestCase):

    def setUp(self) -> None:
        self.directory = Path('temp')
        self.directory.mkdir()
        self.change_tracker = ChangeTracker(tracked_dir=str(self.directory.resolve()))

    def tearDown(self):
        self.directory = Path('temp')
        self.directory.rmdir()
        Path(hashlib.md5(str(self.directory.resolve()).encode('utf-8')).hexdigest()).unlink()

    def test_added(self):
        file = Path(self.directory.resolve(), 'testFile1')
        file.touch()
        file.write_text('test1')
        added, modified, removed = self.change_tracker._get_changes()
        file.unlink()
        # Assert
        self.assertEqual(added[0], 'testFile1')

    def test_removed(self):
        file = Path(self.directory.resolve(), 'testFile1')
        file.touch()
        self.change_tracker._get_changes()
        file.unlink()
        added, modified, removed = self.change_tracker._get_changes()
        # Assert
        self.assertEqual(removed[0], 'testFile1')

    def test_modified(self):
        file = Path(self.directory.resolve(), 'testFile1')
        file.touch()
        self.change_tracker._get_changes()
        file.write_text('test1')
        added, modified, removed = self.change_tracker._get_changes()
        file.unlink()
        # Assert
        self.assertEqual(modified[0], 'testFile1')