"""Importing required modules for class to work."""
import unittest
import synchronization
import leaderboards
import os
import game


class SynchronizationTest(unittest.TestCase):
    """Testing that file reading and writing is handled correctly."""

    directory = "data/testing"
    f1 = "data/testing/test_users.pickle"
    f2 = "data/testing/test_leaderboards.pickle"

    def setUp(self):
        """Create variables for tests."""
        self.sync = synchronization.Sync()
        self.game = game.Game()
        self.leaderboards = leaderboards.Leaderboards()
        self.leaderboards.scoreboard = leaderboards.Leaderboards.scoreboard
        self.sync.file1 = self.f1
        self.sync.file2 = self.f2
        self.player1 = self.game.create_player("Drake testing")
        self.player2 = self.game.create_player("Benson testing")
        os.mkdir(self.directory)

    def test_self_write(self):
        """Test that writing happens correctly and a file is generated."""
        self.assertFalse(os.path.exists(self.f1))
        self.assertFalse(os.path.exists(self.f2))
        self.sync.pickle_write()
        self.assertTrue(os.path.exists(self.f1))
        self.assertTrue(os.path.exists(self.f2))

