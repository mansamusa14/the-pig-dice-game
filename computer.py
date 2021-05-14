"""Functionality for the computer mode"""
import dice


class Computer():

    """Create an instance of Dice class and assigning it to a variable."""
    die = dice.Dice()

    """Create a variable to hold assigned difficulty for computer object."""

    difficulty = ""
    points_held = 0
    username = "Computer"
    final_action_pool = (
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "roll",
        "hold",
        "hold",
        "hold",
        "hold",
        "hold",
        "hold",
        "hold"
        )

    action_pool = list(final_action_pool)

    times_rolled = 0

    def roll(self):
        """Call Roll method from dice class and returning it."""
        return dice.Dice().roll(self.difficulty)

    def reset_action_pool(self):
        """Reset action_pool variable."""
        self.action_pool = list(self.final_action_pool)
