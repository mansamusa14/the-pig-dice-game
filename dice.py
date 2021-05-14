"""Player or computer reaction to a roll."""

import random


class Dice():
    """Define dice variations."""

    dice_pool_normal = (1, 2, 3, 4, 5, 6)
    dice_pool_easy = (1, 1, 2, 2, 2, 3, 3, 4, 5, 6)
    dice_pool_hard = (1, 2, 3, 4, 4, 5, 5, 5, 6, 6)
    dice_pool_cheat = dice_pool_normal[1:]

    def roll(self, condition):
        """Roll method combines the different possibilities
        for rolling the die for computer and player."""

        if condition is False or condition == "normal":
            return random.choice(self.dice_pool_normal)
        elif condition == "easy":
            return random.choice(self.dice_pool_easy)
        elif condition == "hard":
            return random.choice(self.dice_pool_hard)
        elif condition is True:
            return random.choice(self.dice_pool_cheat)
