"""
___________________________________________________

    ******  Welcome Pig Dice Game!  ******  
___________________________________________________

To start the game, please select an option:

login <username> <password>  -   Login  (existing)
create <username> <password> -   Create (new)
quit                         -   Exit the game

"""

import shell
import subprocess
import platform

if __name__ == '__main__':
    subprocess.run(
        "cls" if platform.system() == "Windows" else "clear",
        shell=True)
    print(__doc__)
    shell.Shell().cmdloop()
