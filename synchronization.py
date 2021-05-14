"""Synchronize pickle files with the player_list and static scoreboard."""

import pickle
import leaderboards
import game


class Sync():
    """Dynchronization for objects when writing to/reading from."""

    file1 = "data/test_users.pickle"
    file2 = "data/test_leaderboards.pickle"

    def pickle_write(self):
        """Write to bin."""
        with open(self.file1, 'wb') as file:
            pickle.dump(game.Game.list_players, file)
        with open(self.file2, 'wb') as file:
            pickle.dump(leaderboards.Leaderboards.scoreboard, file)

    def pickle_read(self):
        """Read and initiates from bin."""
        with open(self.file1, 'rb') as file:
            content = pickle.load(file)
            game.Game.list_players = content
        with open(self.file2, 'rb') as file:
            content = pickle.load(file)
            leaderboards.Leaderboards.scoreboard = content
