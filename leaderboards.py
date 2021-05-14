"""Showing the top 5 global scores."""
import player


class Leaderboards():
    """Tracking and updating scoreboard."""

    scoreboard = (
        player.Player,
        player.Player,
        player.Player,
        player.Player,
        player.Player
        )

    def update(self, p):
        """Updating scoreboard."""
        updating = list(self.scoreboard)
        r5 = self.scoreboard[-1]
        if p.points_held > r5.points_held and isinstance(p, player.Player):
            if p.is_cheating is False:
                """ Assign new temporary player object for mem. ref """
                player_to_write = player.Player("pig", "pig")
                player_to_write = p
                p = player_to_write
                updating.append(p)
                updating.sort(key=lambda p: p.points_held, reverse=True)
                updating.pop(len(updating) - 1)
                self.scoreboard = tuple(updating)
