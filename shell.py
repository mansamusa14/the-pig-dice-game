"""Functionality from the command line."""

import cmd
from error_handling.user_not_found import UserNotFound
import game
from error_handling.already_exists import AlreadyExists
from time import sleep


class Shell(cmd.Cmd):
    """Response to do_something in terminal window."""

    intro = 'Type help to see a list of commands\n'
    prompt = '(game) '
    bool = False

    def __init__(self):
        """Construct and initialise on instancing this class."""
        game.Game.set_filepath(game.Game, 'file1', 'data/users.pickle')
        game.Game.set_filepath(game.Game, 'file2', 'data/leaderboards.pickle')
        super().__init__()
        try:
            self.game = game.Game()
        except FileNotFoundError:
            game.Game.writer(game.Game)
            self.game = game.Game()

    def do_help(self, _):
        """Print help menu."""
        print(self.game.help()+"\n")

    def do_create(self, arg):
        """Create new instance of user."""
        name = self.game.curr_player.username
        if self.game.can_create and (
            self.game.position != "rules" or name == ""
                ):
            if len(arg.split(" ")) >= 2:
                try:
                    arg = arg[0].upper() + arg[1:]
                    if self.game.create_player(arg):
                        msg = "Player creation successful! Logging you in now!"
                        print(msg)
                        self.game.writer()
                        self.do_login(arg)
                    else:
                        msg1 = "That username is not allowed! "
                        msg2 = "Please pick another..."
                        print(msg1 + msg2 + "\n")
                except AlreadyExists as error:
                    print(error.msg + "\n")
            else:
                print("Arguments are missing. Please try again")
        else:
            print("Can't do that right now...")
            print()

    def do_login(self, arg):
        """Log into existing account."""
        arg = arg.split(" ")  # split additional parameters apart
        name = self.game.curr_player.username
        if len(arg) >= 2:
            pass
        else:
            print("Missing arguments!")
            return

        if self.game.can_create and (
            self.game.position != "rules" or name == ""
                ):
            try:
                if self.game.login(arg):
                    arg = arg[0]  # discard of extra parameters
                    arg = arg[0].upper() + arg[1:]  # uppercase 1st letter
                    self.game.clear_screen()
                    msg = "\nLogin successful! Welcome {}"
                    n = self.game.curr_player.username
                    print(msg.format(arg), end=". " if n != "" else "\n")
                    if n != "":
                        print(f"{arg} has been set as Player 2.\n\n")
                        print("\n" + self.game.show_rules())
                        self.game.start_reset_restart()
                        print(self.game.scores())
                    else:
                        self.game.curr_player = self.game.player_1
                        p1n = self.game.curr_player.username
                        self.prompt = f"(game)({p1n}) "
                        self.game.can_create = False
                        print(self.game.show_menu())
            except UserNotFound as error:
                print(error.msg)
        else:
            msg1 = "Cannot logging "
            msg2 = "in to another account right now...\n"
            print(msg1+msg2)
    
    
    def do_namechange(self, arg):
        """Change username of player."""
        if len(arg) > 0:
            pass
        else:
            print("Missing arguments!")
        arg = arg[0].upper() + arg[1:]
        if self.game.curr_player == self.game.player_1:
            self.bool = self.game.curr_player.username != ""
        elif self.game.curr_player == self.game.player_2:
            self.bool = (self.game.curr_player.username != "")
        if self.bool:
            try:
                new_name = self.game.namechange(arg)
                if self.game.curr_player == self.game.player_1:
                    self.game.player_1.username = new_name
                else:
                    self.game.player_2.username = new_name
                self.game.clear_screen()
                print("\n>> Name updated.")
                if self.game.position == "menu":
                    print(self.game.show_menu())
                elif self.game.position == "rules":
                    print(self.game.show_rules())
                    print(self.game.scores())
                p1n = self.game.curr_player.username
                self.prompt = f"(game)({p1n}) "
                if self.game.curr_player == self.game.player_1:
                    self.game.player_1 == self.game.curr_player
                else:
                    self.game.player_2 == self.game.curr_player
                self.game.writer()
            except AlreadyExists as error:
                print(error.msg)
        else:
            print("You can't change your name mid-game.", end=" ")
            print("Consider resetting the game (/re or /reset)")

    def do_roll(self, _):
        """Roll dice."""
        if self.game.position == 'menu':
            return print(self.game.err_msg())

        if self.game.curr_player == self.game.player_1:
            self.bool = self.game.curr_player.username != ""
        elif self.game.curr_player == self.game.player_2:
            self.bool = (self.game.curr_player.username != "")
        if self.bool:
            rolled = self.game.roll()
            name = self.game.curr_player.username
            points = self.game.curr_points
            print(f">> {name} rolled ", flush=True, end="")
            sleep(0.2)
            for _ in range(0, 3):
                print(". ", flush=True, end="")
                sleep(0.2)
            if rolled != 1:
                print(f"{rolled}! {name}'s current score is {points}\n")
            else:
                msg1 = f"{rolled}! Oh no, {name}'s non-held points and "
                msg2 = "turn have been forfeited.\n"
                print(msg1+msg2)
                self.game.reset_curr_points()
                self.game.next_player()
                name = self.game.curr_player.username
                self.prompt = f"(game)({name}) "
                if name == "Computer":
                    self.computer_logic()
        else:
            print(self.game.err_msg())

    def do_r(self, _):
        """Run do_roll()."""
        return self.do_roll(_)

    def do_hold(self, arg):
        """Hold current points in round."""
        if self.game.position == 'menu':
            return print(self.game.err_msg())

        if self.game.curr_player == self.game.player_1:
            self.bool = self.game.curr_player.username != ""
        elif self.game.curr_player == self.game.player_2:
            self.bool = (self.game.curr_player.username != "")
        if self.bool:
            sleep(0.2)
            self.game.clear_screen()
            print("\n\n\n" + self.game.show_rules())
            arg = arg.split(" ")
            arg = arg[0]
            name = self.game.curr_player.username
            points = self.game.curr_points  # curr points
            hpoints = self.game.curr_player.points_held  # curr held points
            self.game.curr_player.points_held = hpoints + points  # updating
            total = self.game.curr_player.points_held
            if self.update_won(name, total):
                return
            else:
                print(self.game.scores())
                msg1 = f">> {name} saved {points} points this round! "
                msg2 = f"{name} now has a total of {total} points held!\n"
                self.game.reset_curr_points()
                self.game.next_player()
                name = self.game.curr_player.username
                self.prompt = f"(game)({name}) "
                print(msg1 + msg2)
            if name == "Computer":
                self.computer_logic()
        else:
            print(self.game.err_msg())

    
    def do_h(self, _):
        """Run do_hold()."""
        return self.do_hold(_)

    def update_won(self, name, total):
        """Check if won."""
        if self.game.has_won():
            self.game.clear_screen()

            """write data if curr player is player obj."""
            if isinstance(self.game.curr_player, game.Game.curr_player):
                self.game.curr_player.add_win()
                if name == self.game.player_2.username:
                    """ player 1 is always player obj"""
                    self.game.player_2 = self.game.curr_player
                    self.game.player_1.add_losses()
                else:
                    self.game.player_1 = self.game.curr_player
                    if self.game.player_2.username != "Computer":
                        self.game.player_2.add_losses()
                for player in self.game.list_players:
                    if player.username == name:
                        player = self.game.curr_player
                self.game.update()
                # self.game.curr_player.reset()
                self.game.writer()
                self.game.reader()
                if self.game.curr_player == self.game.player_1:
                    self.game.player_1 = self.game.curr_player
                elif self.game.curr_player == self.game.player_2:
                    self.game.player_2 == self.game.curr_player
            else:
                self.game.player_1.add_losses()

            """reset player 2."""
            p2_msg = f"{self.game.player_2.username} has been logged out!"
            self.game.player_2 = game.Game.player_2

            """Print victory message and reset main menu."""
            victory_msg = ">>  Congratulations, {}! You won with {} points!"
            print(f"\n\n{victory_msg.format(name, total)}")
            print(f">>  {p2_msg}\n\n")
            print(self.game.show_menu())
            return True
        else:
            return False

    def computer_logic(self):
        """Logic powering computer/AI decisions(can't be called by cmdloop)."""
        action = ""
        while self.game.curr_player == self.game.player_2:

            if self.game.curr_points == 0:
                action = "roll"
            else:
                action = self.game.comp_choice()

            print(f"{self.prompt} ", flush=True, end="")
            sleep(0.6)
            print(action)

            if action == "roll":
                self.do_roll(action)
            elif action == "hold":
                self.do_hold(action)

    def do_quit(self, _):
        """Terminate game."""
        print("Bye!")
        self.game.quit()

    def do_q(self, _):
        """Run do_quit()."""
        self.do_quit(_)

    def scores(self):
        """Return player scores."""
        return [self.game.player_1.points_held, self.game.player_2.points_held]
