"""Testing the computer class to ensure functionality."""
import unittest
import computer
import dice


class TestComputerClass(unittest.TestCase):
    """Test class for computer class in pig."""

    def test_points_held(self):
        """Testing points_held gets updated correctly."""
        computer.Computer.points_held = 100
        self.assertEqual(computer.Computer.points_held, 100)

    def test_username(self):
        """Testing that the username is final and as expected."""
        self.assertTrue(computer.Computer.username == "Computer")

    def test_difficuly_string(self):
        """Testing whether difficulty of type String changes."""
        self.assertEqual(computer.Computer.difficulty, "")
        computer.Computer.difficulty = "easy"
        self.assertEqual(computer.Computer.difficulty, "easy")

    def test_roll(self):
        """Testing make_roll method."""
        easy = dice.Dice.dice_pool_easy
        normal = dice.Dice.dice_pool_normal
        hard = dice.Dice.dice_pool_hard

        rolling = computer.Computer().roll()

        computer.Computer.difficulty = "easy"
        self.assertTrue(rolling in easy)
        computer.Computer.difficulty = "normal"
        self.assertTrue(rolling in normal)
        computer.Computer.difficulty = "hard"
        self.assertTrue(rolling in hard)
