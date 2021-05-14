"""Importing needed modules."""
import unittest
import player
import dice


class TestPlayerClass(unittest.TestCase):
    """Tests the player class."""

    def setUp(self):
        """Create instance of player for every test."""
        self.mock_player = player.Player("Drake", "testing")
        self.assertIsInstance(self.mock_player, player.Player)

    def test_constructor(self):
        """Test to see if constructor instanciates player object correctly."""
        res = player.Player("Drake", "testing")
        exp = player.Player
        self.assertIsInstance(res, exp)
        self.assertEqual(res.username, "Drake")
        self.assertEqual(res.password, "testing")

    def test_username_password(self):
        """Test for checking variable username."""
        res1 = self.mock_player.username
        res2 = self.mock_player.password
        self.assertEqual(res1, "Drake")
        self.assertEqual(res2, "testing")

    def test_is_cheating(self):
        """Test for checking variable is_cheating is default False."""
        res = self.mock_player.is_cheating
        self.assertEqual(res, False)

    def test_losses(self):
        """Test for checking variable losses is default 0."""
        res = self.mock_player.losses
        self.assertEqual(res, False)

    def test_cheat(self):
        """Testing if cheating is switched to True."""
        self.assertEqual(self.mock_player.is_cheating, False)
        self.mock_player.cheat()
        self.assertTrue(self.mock_player.is_cheating, True)

    def test_add_losses(self):
        """Testing if player instance losses is updated."""
        self.assertEqual(self.mock_player.losses, 0)
        self.mock_player.add_losses()
        self.assertEqual(self.mock_player.losses, 1)
        self.mock_player.add_losses()
        self.mock_player.add_losses()
        self.assertEqual(self.mock_player.losses, 3)

    def test_show_statistics(self):
        """Testing if method returns corrent statistics."""
        mock = self.mock_player.show_statistics()

        self.assertEqual(mock[0], "John")
        self.assertEqual(mock[1], (0, 0, 0, 0, 0))
        self.assertEqual(mock[2], 0)
        self.assertEqual(mock[3], 0)

        self.mock_player.points_held = 150
        self.mock_player.set_highscore()
        self.mock_player.points_held = 140
        self.mock_player.set_highscore()
        self.mock_player.points_held = 130
        self.mock_player.set_highscore()
        self.mock_player.points_held = 120
        self.mock_player.set_highscore()
        self.mock_player.points_held = 110
        self.mock_player.set_highscore()

        self.mock_player.add_win()
        self.mock_player.add_win()
        self.mock_player.add_losses()

        mock = self.mock_player.show_statistics()

        self.assertEqual(mock[0], "John")
        self.assertEqual(mock[1], (150, 140, 130, 120, 110))
        self.assertEqual(mock[2], 2)
        self.assertEqual(mock[3], 1)

    def test_reset(self):
        """Testing if method resets points_held and is_cheating."""
        self.assertEqual(self.mock_player.points_held, 0)
        self.assertFalse(self.mock_player.is_cheating)

        self.mock_player.cheat()
        self.mock_player.points_held = 10

        self.assertEqual(self.mock_player.points_held, 10)
        self.assertTrue(self.mock_player.is_cheating)

        self.mock_player.reset()

        self.assertEqual(self.mock_player.points_held, 0)
        self.assertFalse(self.mock_player.is_cheating)


