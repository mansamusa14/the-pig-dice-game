"""Testing the logic of the game."""

from error_handling.already_exists import AlreadyExists
from error_handling.user_not_found import UserNotFound
from unittest.mock import patch
import unittest
import player
import computer
import dice
import leaderboards
import synchronization
import game
import os


class TestGame(unittest.TestCase):
    """Ensure everything works perfectly."""

    def setUp(self):
        """Run on every test."""
        self.game = game.Game()
        self.dice = dice.Dice()
        self.computer = computer.Computer()
        self.leaderboards = leaderboards.Leaderboards()
        self.player1 = player.Player("Drake", "testing")
        self.player2 = player.Player("Benson", "testing")

    def test_init(self):
        """Mock sync instance."""
        sync = synchronization.Sync()
        self.assertTrue(os.path.exists(sync.file1))
        self.assertTrue(os.path.exists(sync.file2))
        os.remove(sync.file1)
        os.remove(sync.file2)
        self.assertFalse(os.path.exists(sync.file1))
        self.assertFalse(os.path.exists(sync.file2))

    def test_help(self):
        """Help Menu Test."""
        res = self.game.help()
        self.assertIsInstance(res, str)

    def test_create_player(self):
        """Test Player Creation."""
        """ensure object instantiates correctly."""
        self.assertEqual(self.player1.username, "Drake")
        self.assertEqual(self.player1.password, "testing")
        self.assertEqual(self.player1.wins, 0)
        self.assertEqual(self.player1.points_held, 0)
        self.assertEqual(self.player1.top_scores, (0, 0, 0, 0, 0))
        with self.assertRaises(IndexError):
            self.player1.top_scores[6]

        """test for some of the invalid names."""
        self.assertFalse(self.game.create_player("Dice test"))
        self.assertFalse(self.game.create_player("Computer test"))
        self.assertFalse(self.game.create_player("Pig test"))
        self.assertFalse(self.game.create_player("USeR test"))
        self.assertFalse(self.game.create_player("SAMPLE test"))

        """test for duplicate error handling."""
        self.game.list_players.append(self.player1)
        info = self.player1.username + " " + self.player1.password
        with self.assertRaises(AlreadyExists):
            self.game.create_player(info)
        self.game.list_players.clear()
        self.assertTrue(self.game.create_player("Benson testing"))

    def test_show_menu(self):
        """Test main menu is of type String."""
        res = self.game.show_menu()
        self.assertIsInstance(res, str)
        self.assertIs(self.game.position, "menu")

    def test_show_rules(self):
        """Test Show_rules()."""
        res = self.game.show_rules()
        self.assertIsInstance(res, str)
        self.assertIs(self.game.position, "rules")

    def test_login(self):
        """Test login."""
        info = "Drake Testing"
        info2 = "Benson Testing"
        info = info.split(" ")
        info2 = info2.split(" ")

        with self.assertRaises(TypeError):
            self.game.login(3)

        """Test login with an invalid account."""
        with self.assertRaises(UserNotFound):
            self.game.login(info)

        """Create mock players."""
        self.game.create_player(info)
        self.game.create_player(info2)

        self.assertTrue(len(self.game.list_players), 2)

        """Test login with newly added account."""
        self.assertTrue(self.game.login(info))
        self.assertTrue(self.game.login(info2))
        self.assertEqual(self.game.player_1.username, "Drake")
        self.assertEqual(self.game.player_2.username, "Benson")

    def test_namechange(self):
        """Test namechange."""
        self.game.list_players.append(self.player1)
        self.game.list_players.append(self.player2)
        self.assertEqual(len(self.game.list_players), 2)

        """Test error handling on already exists."""
        self.game.curr_player = self.player1
        with self.assertRaises(AlreadyExists):
            self.game.namechange("Drake")
        self.game.curr_player = self.player2
        with self.assertRaises(AlreadyExists):
            self.game.namechange("Benson")

        """Test namechange again with b now available."""
        self.game.list_players.remove(self.player2)  # remove Jane
        self.assertIs(len(self.game.list_players), 1)
        self.game.curr_player = self.player1
        self.game.namechange("Drake")
        self.assertIs(self.game.curr_player.username, "Benson")

    def test_quit(self):
        """Test quitting."""
        with self.assertRaises(SystemExit):
            self.game.quit()

    def test_start_reset_restart(self):
        """Test behaviours under pre-determined conditions."""
        self.game.player_1 = self.player1
        self.game.player_2 = self.player2
        self.game.player_1.points_held = 99
        self.game.player_1.cheat()
        self.game.player_2.points_held = 103
        self.game.player_2.cheat()

        self.game.start_reset_restart()

        """player 1."""
        self.assertEqual(self.player1.points_held, 0)
        self.assertFalse(self.player1.is_cheating)
        """player 2 is player."""
        self.assertEqual(self.player2.points_held, 0)
        self.assertFalse(self.player2.is_cheating)
        """player 2 is computer."""
        self.game.player_2 = computer.Computer
        self.game.player_2.points_held = 89
        self.assertIs(self.game.player_2.points_held, 89)
        self.game.start_reset_restart()
        self.assertIs(self.game.player_2.points_held, 0)

    def test_has_won(self):
        """Test if the player has won after holding."""
        self.player1.points_held = 101
        self.game.curr_player = self.player1
        self.assertTrue(self.game.has_won())
        self.player2.points_held = 99
        self.game.curr_player = self.player2
        self.assertFalse(self.game.has_won())

    def test_hold_points(self):
        """Test to see if points are held correctly."""
        self.game.curr_player = self.player1
        self.game.curr_points = 25
        self.game.hold()
        self.assertEqual(self.game.curr_player.points_held, 25)

    def test_next_player(self):
        """Tests that switching players happens correctly."""
        self.game.player_1 = self.player1
        self.game.player_2 = self.player2
        self.game.curr_player = self.player1
        self.assertEqual(self.game.next_player(), self.player2)
        self.assertEqual(self.game.next_player(), self.player1)
        """Test reset on action pool is done correctly on computer."""
        name = self.game.curr_player.username
        self.assertTrue(name == self.game.player_1.username)
        self.game.player_2 = self.computer
        """Reverse action pool."""
        self.computer.action_pool = list(reversed(self.computer.action_pool))
        final_ap = list(self.computer.final_action_pool)
        self.assertNotEqual(self.computer.action_pool, final_ap)
        """ Test next_player resets it."""
        self.assertIsInstance(self.game.next_player(), computer.Computer)
        self.game.next_player()
        self.computer = computer.Computer
        self.assertEqual(self.computer.action_pool, final_ap)

    def test_reset_curr_points(self):
        """Test if resetting current points behaves correctly."""
        self.assertEqual(self.game.curr_points, 0)
        self.game.curr_points = 89
        self.assertEqual(self.game.curr_points, 89)
        self.game.reset_curr_points()
        self.assertEqual(self.game.curr_points, 0)

    def test_create_screen(self):
        """Testi create_screen()."""
        msg = "Enter <create> followed by a username and password"
        self.assertEqual(self.game.create_screen(), msg)

    def test_set_computer(self):
        """Test set_computer()."""
        self.assertFalse(isinstance(self.game.player_2, computer.Computer))
        self.game.set_computer()
        self.assertEqual(self.game.player_2, computer.Computer)

    def test_computer_choice(self):
        """Testing computer_choice()."""
        self.game.player_2 = computer.Computer()
        for _ in range(0, 2):
            self.game.curr_player = self.game.player_2
            self.game.curr_player.points_held = 0
            self.assertNotEqual(self.game.comp_choice(), "")

    def test_writer(self):
        """Test sync writer."""
        self.assertEqual(
                self.game.writer(), synchronization.Sync().pickle_write()
            )

    def test_reader(self):
        """Test sync reader()."""
        self.game.reader()
        self.assertEqual(
            self.game.reader(), synchronization.Sync().pickle_read()
        )

    def test_error_msg(self):
        """Test error_msg."""
        self.assertIsInstance(self.game.err_msg(), str)

    def test_get_scoreboard(self):
        """Test get_scoreboard."""
        self.assertEqual(
            self.game.get_scoreboard(),
            leaderboards.Leaderboards.scoreboard
        )

    def test_clear_screen(self):
        """Test clear_screen."""
        with patch('game.Game') as mock:
            exp = mock.return_value
            exp.method = None
            res = self.game.clear_screen()
            assert res is None
