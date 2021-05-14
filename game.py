"""Main game logic."""

from error_handling.already_exists import AlreadyExists
from error_handling.user_not_found import UserNotFound
import random
import player
import computer
import leaderboards
import subprocess
import synchronization
import platform


class Game():
    """Game class."""

    position = "menu"  # where you're currently navigating within the game
    list_players = []
    player_1 = player.Player
    player_2 = player.Player
    curr_player = player.Player
    curr_points = 0
    can_login = can_create = True
    error_msg_flavor = (
        "I do not get it",
        "I do not get it",
        "Oh my God",
        "OMG",
        "I don't understand it",
        "I don't understand it",
        "I do not understand",
        "I do not understand",
        "Oh my God",
        "My God",
        "I do not understand",
        "I don't understand"
    )
    error_msg = ">> {}! That cannot be done right now."

    def __init__(self):
        """Constructor."""
        try:
            synchronization.Sync().pickle_read()
        except FileNotFoundError:
            synchronization.Sync().pickle_write()

    def help(self):
        """Help Menu."""
        msg = """
            \t_______________________________________________________________

            \t        Welcome to our help menu! Here are your options
            \t_______________________________________________________________

            \t-------------
            \t  GAMEPLAY
            \t-------------
            \tr / roll         Roll the dice
            \th / hold         Hold your score (ends your turn)
            \tre / restart     Restart the game and discard your score
            \tcheat            Enter cheat mode. *Using this will disqualify
            \t                 you from earning any highscores this round

            \t-------------
            \t    USER
            \t-------------
            \tcreate           Create a new player
            \tlogin            Log in as an existing player
            \tstats            Show current player statistics
            \tstats <name>     Show the statistics of player 1 or player 2
            \tlb/highscore   Show global highscore
            \tnamechange       change your username (does not change previous
            \t                 Scoreboard scores)

            \t-------------
            \t  GENERAL
            \t-------------
            \tclear            clears the screen
            \trules            print out the rules for the game
            \thelp             Brings up (this) help menu
            \tq / quit         Quits the game
            \te / exit         Quits the game
            """
        return msg

    def show_menu(self):
        """Show game menu."""
        self.position = "menu"
        oink = """
        ________________________________________________________________

             >>>>>>   What game mode would you like to play?   <<<<<<
        ________________________________________________________________

            choose 1                Player vs. Player
            choose 2                Player vs. Computer
            quit                    Quit the game\n\n\n"""
        return oink

    def create_player(self, info):
        """Create instance of player class."""
        if isinstance(info, str):
            info = info.split(" ")
        username = info[0]
        password = info[1]
        """ creates a new player """

        names_not_allowed = (
            "computer",
            "pig",
            "test",
            "user",
            "tester",
            "random",
            "example"
            )

        if username.lower() not in names_not_allowed:
            new_player = player.Player(username, password)
            if len(self.list_players) > 0:
                for p in self.list_players:
                    if new_player.username == p.username:
                        raise AlreadyExists
            self.list_players.append(new_player)
            return True
        else:
            return False

    def show_rules(self):
        """Show menu of rules."""
        self.position = "rules"
        msg = """

            RULES |
                1   |   You may roll until you hold your score or roll 1
                2   |   Holding saves your accumulated points to your total
                3   |   Rolling 1 loses you all your unheld points
                4   |   The first player to hold a score of 100 points wins.

        """
        return msg
    
    
    def login(self, info):
        """Log in the user and sets the match as player."""
        username = info[0]
        username = username[0].upper() + username[1:]
        password = info[1]

        for p in self.list_players:
            if username == p.username and password == p.password:
                if self.player_1.username != "":
                    self.player_2 = p
                else:
                    self.player_1 = p
                self.can_login = False
                return True
        raise UserNotFound

    def namechange(self, name):
        """Change player name."""
        name = name.split(" ")
        name = name[0]
        name[0].upper()
        """Check for namechange availability."""
        for p in self.list_players:
            if p.username == name:
                raise AlreadyExists
        """if no error is raised, continue with the change."""
        self.curr_player.username = name
        return name

    def quit(self):
        """Exit the game."""
        raise SystemExit()

    def start_reset_restart(self):
        """Reset players and restarting game."""
        self.player_1.reset()
        if isinstance(self.player_2, player.Player):
            self.player_2.reset()
        else:
            self.player_2.points_held = 0

    def has_won(self):
        """Determine if player has won or not."""
        if self.curr_player.points_held >= 100:
            return True
        else:
            return False

    def hold(self):
        """Add the input points to the current points of player."""
        self.curr_player.points_held += self.curr_points

    def roll(self):
        """Call roll function."""
        rolled = 0
        if isinstance(self.curr_player, player.Player):
            rolled = self.curr_player.roll()
        else:
            rolled = self.curr_player.roll(computer.Computer)
        self.curr_points += rolled
        return rolled

    def next_player(self):
        """Switch current player."""
        if self.curr_player != self.player_1:
            self.player_2 = self.curr_player  # save to player_2
            self.curr_player = self.player_1
        elif self.curr_player != self.player_2:
            self.player_1 = self.curr_player  # save to player_1
            self.curr_player = self.player_2
            if isinstance(self.player_2, computer.Computer):
                computer.Computer.reset_action_pool(computer.Computer)
        return self.curr_player

    def reset_curr_points(self):
        """Reset the current points tally."""
        self.curr_points = 0

    def create_screen(self):
        """Instructions for creating a new account."""
        return "Enter <create> followed by a username and password"

    def clear_screen(self):
        """Clear the game-screen."""
        subprocess.run(
            "cls" if platform.system() == "Windows" else "clear", shell=True
            )
        return

    def update(self):
        """Test that user scores are updated correctly."""
        if self.curr_player.username != "Computer":
            self.curr_player.set_highscore()
            leaderboards.Leaderboards.update(
                leaderboards.Leaderboards, self.curr_player
                )
            return True
        else:
            return False

    def get_scoreboard(self):
        """Return scoreboard."""
        return leaderboards.Leaderboards.scoreboard

    def err_msg(self):
        """Print error message."""
        flav = random.choice(self.error_msg_flavor)
        return self.error_msg.format(flav) + "\n"

    def scores(self):
        """Present current scores."""
        msg = "\t\t\t[ {} : {} points || {} : {} points ]\n"
        msg = msg.format(
            self.player_1.username,
            self.player_1.points_held,
            self.player_2.username,
            self.player_2.points_held
            )
        return msg

    def writer(self):
        """Write to file."""
        return synchronization.Sync().pickle_write()

    def reader(self):
        """Read from file."""
        return synchronization.Sync().pickle_read()

    def set_filepath(self, file, path):
        """Set path to files."""
        if file == 'file1':
            synchronization.Sync.file1 = path
        elif file == 'file2':
            synchronization.Sync.file2 = path

    def set_computer(self):
        """Access static computer and assign as player_2."""
        self.player_2 = computer.Computer

    def set_computer_difficulty(self, difficulty):
        """Set computer difficulty to that which is specified by the user."""
        msg = f"You successfully have selected {difficulty} difficulty!"
        computer.Computer.difficulty = difficulty
        return msg

    def comp_choice(self):
        """Retrieve an action from the computer's action_pool attribute."""
        action = random.choice(computer.Computer.action_pool)

        """ replace a roll with hold in action_pool(+5% chance to hold) """
        for option in computer.Computer.action_pool:
            if option == "roll":
                option == "hold"
                break
        return action

