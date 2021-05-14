"""Return a message when a user is not found in the player_list."""


class UserNotFound(Exception):
    """Raise when user is not found during login."""

    msg = "User not found! Please try again."
