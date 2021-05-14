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

    
    def do_choose(self, arg):
        """Choose difficulty level."""
        if not arg:
            print(">> Missing argument!")
        else:
            if self.game.position == "menu":
                if arg == '1':
                    self.game.can_login = self.game.can_create = True
                    msg1 = ">> Enter <login> or <create> followed "
                    msg2 = "by your username and password"
                    print(msg1 + msg2)
                elif arg == '2':
                    self.game.set_computer()
                    msg1 = "\nBeep, beep, boops! "
                    msg2 = "Computer gonna pwn some noobs!\n"
                    print(msg1 + msg2)
                    self.game.position = "computer_menu"
                    print("Please select a difficulty")
                    print("__________________________")
                    print("choose 1              Easy")
                    print("choose 2            Normal")
                    print("choose 3              Hard\n")
                else:
                    print(self.game.err_msg())
            elif self.game.position == "computer_menu":
                if arg >= '1' and arg <= '3':
                    self.game.clear_screen()
                    self.game.curr_player == self.game.player_1
                    if arg == '1':
                        print(self.game.set_computer_difficulty("easy"))
                    elif arg == '2':
                        print(self.game.set_computer_difficulty("normal"))
                    elif arg == '3':
                        print(self.game.set_computer_difficulty("hard"))
                    print("\n" + self.game.show_rules())
                    self.game.start_reset_restart()
                    print(self.game.scores())
                    msg1 = "You may type help to view a list of "
                    msg2 = "all available commands"
                    print(msg1 + msg2 + "\n")
                else:
                    print(self.game.err_msg())
            else:
                print("No choices are currently being presented\n")

    def do_cheat(self, _):
        """Activate cheat."""
        if self.game.position == "rules" and self.game.player_2.username != "":
            pass
        else:
            print(self.game.err_msg())
            return

        if self.game.curr_player == self.game.player_1:
            self.bool = self.game.curr_player != game.Game.player_1
        elif self.game.curr_player == self.game.player_2:
            self.bool = self.game.curr_player != game.Game.player_2
        if self.bool:
            self.game.curr_player.is_cheating = True
            print("Cheater!!!.")
            print(">> setting Highscores has been disabled for this round <<")
            print(">>>>>>>>>>>>>>> You can no longer roll 1 <<<<<<<<<<<<<<<<")
            print("\n")
        else:
            print(self.game.err_msg())

    def do_restart(self, _):
        """Restart running game."""
        self.bool = (self.game.player_2.username != "")
        if self.bool:
            self.game.start_reset_restart()
            self.game.clear_screen()
            print(">> Game restarted.".format())
            print("\n" + self.game.show_rules())
            print(self.game.scores())
        else:
            print(self.game.err_msg())

    def do_re(self, _):
        """Call do_restart to restart the game."""
        return self.do_restart(_)

    def do_stats(self, arg):
        """Show player statistics."""
        if self.game.player_1.username == "":
            print(">>  No user is currently logged in.\n")
            return
        self.bool = False
        player = None
        p1n = self.game.player_1.username
        p2n = self.game.player_2.username
        arg = arg.split(" ")
        arg = arg[0]

        if len(arg) == 0 or arg.lower() == "p1" or arg.lower() == p1n.lower():
            player = self.game.player_1
        elif arg.lower() == "p2" or arg.lower() == p2n.lower():
            if p2n.lower() != "computer":
                if p2n != "":
                    player = self.game.player_2
                elif p2n == " ":
                    player = self.game.player_1
                else:
                    print(f">>  {p2n} is not currently logged in!\n")
                    return
            else:
                print(">>  Computer has no statistics!\n")
                return
        else:
            m = 'Stats retrieval failed. '
            m2 = 'Please check if the user is logged in and try again.\n'
            print(m + m2)
            return

        if player is not None:
            self.bool = True

        if self.bool:
            stats = player.show_statistics()
            name = stats[0]
            scores = stats[1]
            wins = stats[2]
            losses = stats[3]
            q = "___________________________________________"
            txt = f"Player statistics for {name}"
            print(f"{q}\n\n{txt.center(len(q))}\n{q}\n")

            print("> Player Top Scores:")
            for i in range(0, len(scores)):
                print(f"\t{i + 1}.  {scores[i]} points")
            print(f"> Player Wins: {wins}")
            print(f"> Player Losses: {losses}")
            print("\n\n")
        else:
            print(self.game.err_msg())

    def do_leaderboards(self, _):
        """Print leaderboard."""
        q = "___________________________________________"
        txt = "Pig Game Leaderboards"
        print(f"{q}\n\n{txt.center(len(q))}\n{q}\n")
        for i in range(0, len(self.game.get_scoreboard())):
            print("  {}{} ".format(i + 1, '.'), end=" ")
            obj = self.game.get_scoreboard()[i]
            name = obj.username
            score = obj.points_held
            if name == "" or obj.points_held == 0:
                name = "Empty slot"
            print("{:15s}".format(name), end="")
            print(end="|\t\t" if name != "Empty slot" else "\n")
            if name != "Empty slot":
                print(f"{score} points")
        print()

    def do_leaderboard(self, _):
        """Run do_leaderboards()."""
        return self.do_leaderboards(_)

    def do_lb(self, _):
        """Run do_leaderboards()."""
        return self.do_leaderboards(_)

    
    def do_rules(self, _):
        """Print rules."""
        position = self.game.position
        print(self.game.show_rules())
        self.game.position = position
        return

    def do_exit(self, _):
        """Terimnate game."""
        return self.do_quit(_)

    def do_e(self, _):
        """Run do_exit()."""
        return self.do_exit(_)

    def do_clear(self, _):
        """Clear screen."""
        if self.game.player_1.username != "":
            self.game.clear_screen()
            print(">>  Screen cleared!")
            if self.game.position == "menu":
                print(self.game.show_menu())
            elif self.game.position == "rules":
                print(self.game.show_rules())
                print(self.game.scores())
        else:
            return print(self.game.err_msg())

