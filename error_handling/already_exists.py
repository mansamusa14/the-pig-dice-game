"""Return a message when a user already exists in the player_list."""


class AlreadyExists(Exception):
    """Raise when the username has already been taken."""

    msg = "This username is already taken"
