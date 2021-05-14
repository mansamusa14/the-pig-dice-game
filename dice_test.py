"""Importing the required modules for class to work."""
import unittest
import dice


class TestDice(unittest.TestCase):
    """Testing class for Dice class."""

    def setUp(self):
        """Creating instance of dice before every test."""
        self.die = dice.Dice()
        self.assertIsInstance(self.die, dice.Dice)

    def test_roll(self):
        """Testing roll()."""
        """ Testing roll properties """
        normal = self.die.dice_pool_normal
        easy = self.die.dice_pool_easy
        hard = self.die.dice_pool_hard
        cheat = self.die.dice_pool_cheat

        """ Ensuring roll properties are called correctly """
        self.assertEqual(normal, (1, 2, 3, 4, 5, 6))
        self.assertEqual(easy, (1, 1, 2, 2, 2, 3, 3, 4, 5, 6))
        self.assertEqual(hard, (1, 2, 3, 4, 4, 5, 5, 5, 6, 6))
        self.assertEqual(cheat, self.die.dice_pool_normal[1:])

        """ Ensuring roll behaviours are called correctly """
        self.assertTrue(self.die.roll("normal") in normal)
        self.assertTrue(self.die.roll("easy") in easy)
        self.assertTrue(self.die.roll("hard") in hard)
        self.assertTrue(self.die.roll(True) in cheat)
