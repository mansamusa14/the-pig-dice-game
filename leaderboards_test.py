"""Test scoreboard properties and behaviours."""

import unittest
import leaderboards
import player


class TestLeaderboards(unittest.TestCase):
    """Testing class for leaderboards."""

    def setUp(self):
        """Create five mock scores for scoreboard."""
        self.leaderboards = leaderboards.Leaderboards()
        self.p1 = player.Player("a", "test")
        self.p2 = player.Player("b", "test")
        self.p3 = player.Player("c", "test")
        self.p4 = player.Player("d", "test")
        self.p5 = player.Player("e", "test")

        """ Testing score """
        self.s1 = self.p1.points_held = 180
        self.s2 = self.p2.points_held = 170
        self.s3 = self.p3.points_held = 160
        self.s4 = self.p4.points_held = 150
        self.s5 = self.p5.points_held = 140

    def test_scoreboard(self):
        """Testing scoreboard variable."""
        self.assertEqual(self.leaderboards.scoreboard, (
            player.Player,
            player.Player,
            player.Player,
            player.Player,
            player.Player
        ))

        for i in self.leaderboards.scoreboard:
            self.assertEqual(i.points_held, 0)


