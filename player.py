"""Importing Dice modules."""
import dice


class Player:
    """Player class"""

    wins = 0
    points_held = 0
    top_scores = (0, 0, 0, 0, 0)
    username = ""
    password = ""
    is_cheating = False
    losses = 0

    def __init__(self, username, password):
        """Contructor to create instances with set username and passwords."""
        self.username = username
        self.password = password

    def add_win(self):
        """Add one value to wins."""
        self.wins = self.wins + 1

    def cheat(self):
        """Turn on cheating."""
        self.is_cheating = True

    def set_highscore(self):
        """Add points_held to top_scores."""
        if self.is_cheating:
            pass
        else:
            temp = list(self.top_scores)
            temp.append(self.points_held)
            temp.sort(reverse=True)
            temp.pop(-1)
            self.top_scores = tuple(temp)


    def roll(self):
        """Return number rolled."""
        return dice.Dice().roll(self.is_cheating)

    def add_losses(self):
        """Call this method adds 1 value to player losses."""
        self.losses += 1

    def show_statistics(self):
        """Return a list of necessary variables."""
        return [self.username, self.top_scores, self.wins, self.losses]

    def reset(self):
        """Reset player points, turns cheats off."""
        self.points_held = 0
        self.is_cheating = False
