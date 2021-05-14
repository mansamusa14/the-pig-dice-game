## Pig dice game: -

The project is in fulfillment of the DA115A Methods for sustainable programming  course, Part 2.


## Features of the game: -

The game comes with a help menu where all commands available to users are shown

A "rules" menu is available for where they can learn how the game works.

The game allows the creation of accounts with passwords where players statistics such as
- points
- wins
- losses
are shown.

player names can be changed once the account is logged in

The game holds a top 5 players list of players with highest top scores which is updated whenever a player beats any of the top 5 player top scores.

The game has a cheat mode, when activated player will not roll a 1 until end of game.

When player activates cheat mode their new top score will not be added to the list.

It can be played in singular mode or versus a computer with three difficulty levels
1. Easy
2. Normal
3. Hard


## Structure of the game: -

shell class:
    Takes command from users and executes corresponding method
    
game class:
    - Most of the intelligence and operations are done in game - class.
    - Player class instances are saved in a list in game class.
    - Computer and Player class data are only returned to game class.
    - Leaderboards class is updated through game class and data - is only return to game class.
    - Synchronization class is used from game class and only returns data to game class.
    - Has a test class.

Computer class:
    - Computer class only holds methods and variables for game class to access.
    - Roll method is accessed through Computer class.
    - Has a test class

Dice class:
    - Dice class holds a method of "roll" for computer and player class to access.
    - Has a test class

player class:
    - Instances of player class will be created for each payer created.
    - Roll method is called from the player instances.
    all the methods in player class only return data, no prints
    - Has a test class

Leaderboards class:
    - Holds a tuple "scoreboard" of top five highest scoring players.
    - The scoreboard is updated every time a game ends.
    - Has a test class

Synchronization class:
    - Updates leaderboards.pickle and users.pickle files with top players and the users.
    - Only returns data to game class
    - Has a test class

## Install guide: -

Getting the game:
    In Gitbash, copy and clone in your terminal
    -- git clone https://github.com/mansamusa14/the-pig-dice-game.git

To launch game enter:
    In Gitbash/CMD
    -- pig.py
    or
    -- main.py
    
Run guide:
    for cmd
    -- pig.py
    or 
    -- main.py
    
## Document guide: -

setup:
    -- make venv
    -- cd .venv/scripts
    -- . activate
    -- cd ../..
    -- make install

Automated uml and documentation:
    -- make doc

Quick read pydoc:
    -- py/python/python3 -m pydoc <filename>

Generate html page pydoc:
    -- py/python/python3 -m pydoc -w <filename>

Generate html documentation:
    -- make pdoc

Generate uml:
    -- pyreverse <filename>
    -- dot -Tpng classes.dot -o classes.png
    or
    -- make pyreverse


## Test guide: -

Execute all unittests:
    -- make unittest
    or
    -- py/python/python3 -m unittest discover . "*_test.py"
    or
    # for more details
    -- py/python/python3 -m unittest discover -v . "*_test.py"
    

## Coverage guide: -

Automated:
    -- make coverage

Run coverage report:
    -- coverage run -m unittest discover . "*_test.py"

Execute coverage report:
    -- coverage report -m

Execute coverage and generate html:
    -- coverage html

Thank You!!!