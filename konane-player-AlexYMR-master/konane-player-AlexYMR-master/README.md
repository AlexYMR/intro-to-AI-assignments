# Assignment 4 — Game Search

## Introduction: Konane

Also known as Hawaiian checkers, [konane](https://en.wikipedia.org/wiki/Konane) is a strategy game played between two
players. Players alternate taking turns, capturing their opponent's pieces by jumping their own pieces over them (if 
you're familiar with checkers, there is a strong structural analogy to be made here). The first player to be unable to
capture any of their opponent's pieces loses.

The full rules can be read *[here](https://en.wikipedia.org/wiki/Konane#Rules_and_gameplay)* or
*[here](http://www.konanebrothers.com/How-to-Play.html)*. Here's my (rather terse) version, though:


![Konane Board](pictures/board.jpg "Board")

1. Black typically starts. They take one of their pieces off of the board.

![Konane Board](pictures/initial.jpg "Board")

2. White then takes one of their pieces off of the board from a space _orthogonally_ adjacent to the piece that black
removed.

![Konane Board](pictures/jump.jpg "Board")

3. Each player then alternately moves their pieces in capturing moves. A capturing move has a stone move in an
orthogonal direction, hopping over an opponent's piece. Multiple captures may be made in a turn, as long as the stone
moves in the same direction and captures at least one piece.

![Konane Board](pictures/nomoves.jpg "Board")

4. The first player to be unable to capture a piece loses. :(

## Play the game


In this assignment, you'll be implementing minimax and alpha-beta pruning for an agent playing one such game—that of
konane. But first, you should get familiar with how the game is played. To do this, play the game with the provided code. You've been distributed a codebase which includes an interface for playing the game in a variety of modes.
Notably, you don't need to actually _make_ the game of konane—just to make an agent that plays it.

_Playing the game interactively may only work on Linux and Mac.  However, this is not required for completing the assignment and is only provided to help you get familiar with the game (and for your entertainment)._

Run the following from your terminal:
```bash
python main.py $P1 $P2
```

By default, `main.py` will setup a human player versus a random player on a board that is 10x10. During **Human** mode, move the cursor with the ARROW keys and select the tile with SPACE. When it is a computer's turn, advance the game with the SPACE key. To see the game board in your terminal, you need a minimum terminal size of (rows + 2) x (columns + 2) to see the whole board. To exit the game, kill the process in your terminal (e.g., with CTRL-c).

You can change the game settings by passing in values to `python main.py`. You need to pass in _exactly_ two arguments. Valid arguments are as follows:

* H (Human)—manually select the tile to move and to where you will move it. Legal moves will be executed.
* D (Deterministic)—the agent will select the first move that it finds (the leftmost option in the tree) during its 
traversal.
* R (Random)—the agent will pick a random move.
* M (Minimax)—the agent will pick a move using the minimax algorithm. You will be prompted for a max. search depth.
* A (Alpha-beta pruning)—the agent will pick a move using AB pruning. You will be prompted for a max. search depth.

Passing in an invalid number or type of arguments will result in the system defaulting to a human vs a random player.

### Running on Windows

The `curses` module is not available on Windows.  You can try to install the package `windows-curses`:

```bash
pip install windows-curses
```

Alternatively, if you are running on Windows 10, you can install Ubuntu as a Linux subsystem.  Running your code there 
will give you access to many libraries and modules available on Linux.


## Your task

Now that you know how the game is played, it is time to make your own intelligent players of the game.  You will do this my implementing one player that use Minimax and another player that uses Alpha-Beta Pruning.

__For this assignment, make sure that you are running Python 3.6 or 3.7.  Python 3.8 may give different results on some tests.__ 
We don't know _why_ it matters, but the test results vary based on the version.
Programming is hard. :(

### Part 1: Minimax

Minimax is an algorithm for determining the best move in an adverserial game. Its objective is to find the move that 
_maximizes_ the gain for the player while _minimizing_ their loss. Since "maximin" sounds kind of dumb, we get 
"minimax." Minimax is typically employed in competitive, discrete- and finite-space games with abstracted time and 
perfect information.

You will complete the implementation of `MinimaxPlayer` in `player.py`. In your implementation, you need to be aware of 2 things: the max depth and the evaluation function.  The max depth is provided to the constructor of the `MinimaxPlayer` and defines the maximum number of plies that the player will simulate when choosing a move.  The evaluation function defines a score for a terminal node in the search.  Use the function `h1` defined in the parent class `Player` as your evaluation function.

Please leave the `selectInitialX` and `selectInitialO` methods alone; all of the editing that you need to do takes place in `getMove`. As always, feel free to add any methods/classes you feel that you need, provided that you change only `player.py`.


### Part 2: Alpha-Beta Pruning

You may notice that minimax starts to get terribly slow when you set your maximum search depth to values above, say, 4.
This makes perfect sense when you think about the fact that the total number of nodes in your game tree is the branching
factor to the power of the search depth. For comparatively "bushy" games (e.g., _chess_, _go_, etc.) the branching
factor is prohibitively large, which is why agents that play these games use cleverer algorithms to choose what move to
take next.

One such cleverer algorithm (although still not clever enough to do well at games like _GO_) is a modification of
minimax known as _alpha-beta pruning_. They are, at their core, the _same algorithm_. The distinction is that AB pruning
_ignores_ subtrees that are provably no better than any that it has considered so far. This can drastically reduce the runtime
of the algorithm. Since AB pruning is a variant on minimax, you aren't really writing a new algorithm; rather, you're
taking your implementation of minimax and making it a little smarter.


As with Minimax, your task is to complete the implementation of `AlphaBetaPlayer`. You will need to again consider the max depth and the evaluation function.


### Testing Your Work

You can manually test your work by playing against your agent yourself, or by having the agents play against each other.
We've also included a few tests for kicking the tires on your implementations of minimax and alpha-beta pruning. You can
find those tests in `test.py` and you can run them with:
```bash
python test.py
```

Since Windows does not support the signals used in `test.py`, there is a `windows_test.py` with all the same tests but a 
slightly different test infrastructure.

The timeouts provided in `test.py` should be generous, so see if you can do much better. It is worth noting that the tests can take upwards of five minutes to complete, so don't freak out. :)

**Scripted Replay**

To help with debugging and generating new tests, each play of the game automatically records all moves to `game.log`.  
The log can be helpful for comparing the sequence of moves in your implementation and in the implementation of others.  
For example, we provide a `game1.log` that is the correct sequence of moves for `test1`.  

Additionally, the logs can be used to replay a particular game by passing the log to the GameManager constructor.
In `test.py`,  you will see the `script` argument in the `makeGame` function.  This is the script used to replay
the game.  The GameManager will take moves from this script up until there are no moves left in the scripts.  At 
that point, the GameManager will continue execution with the defined players.  For examples, 
`test1s` is identical to `test1` except it is completely a scripted replay using `game1.log`.  If the last two
moves in `game1.log` were removed, then the Minimax player and the Deterministic player would make one more move 
(which should then match the two moves that were just removed).

This means you can use truncated log files to create specific test scenarios by replaying a previous game up to a 
given point.  This can be helpful if you know the first *n* moves are correct and then you want to debug the *n+1* move.
You may also want to consider creating test cases in a similar fashion.  You can edit the log to create a new path of
play and verify the game outcome from there.

**Your Tests**

As usual, you need to create two tests to verify the functionality of your code.  Please include comments that help 
make it clear what you are testing and how the tests differ from the other tests.
In designing your own tests, consider different board sizes (always square), depths for searching, and time to execute.  

Since it can be difficult to know whether the find board layout is "correct", you might also want to consider creating 
a valid game board, passing it to your `Player.getMove()`, and verifying the output of a single move.  For this one
move, you may need to manually walk through the scenario to determine what is the correct result.


## Notes

On the codebase:

* `player.py`—this is the file you'll be editing. Note that `MinimaxPlayer` and `AlphaBetaPlayer` are both diked out and
replaced with a determinstic player instead.
* `main.py`—to play the game (in Human mode) or to watch your agents duke it out, run `python main.py`. Use the arrow 
keys and the spacebar to select your actions.
* `test.py`—run tests with `python test.py`.
* `game_manager.py`—holds the board representation and handles turn-taking.
* `game_rules.py`—code determining available moves/their legality, etc.
* You can change the type of player, the board size, etc. in `main.py`



On Alpha-Beta Pruning:

* It's worth noting that alpha-beta produces answers which look more or less the same as vanilla minimax (they should be
identical, given that your search pattern hasn't changed), but alpha-beta will run substantially faster. The grading rig
will use timeouts in its tests, so ordinary minimax won't be fast enough to get you full credit for this part of the
assignment.
* To see the difference between minimax and alpha-beta, just run the game at progressively deeper search depths. You
won't see much of a difference at a depth of 2, but the difference between the two at depth 5 is extreme.
* The function `game_rules.getLegalMoves()` is an expensive function.  You should consider not calling it more than is necessary.


On additional fun:

* Try out a better evaluation function.  Define an `h2` and see how it does.  Can it do better than the `h1` evaluation function?  Note that we will use `h1` for grading, so be sure to have your Minimax and AlphaBeta players setup to use `h1` in your final submission.
* Can you beat AlphaBeta?  Use `main.py` to play against the computer and see if you can win.


## Questions

Please answer the following questions in `answers.txt`:

1.  Why do test3 and test5 have the same result?  Why is the time limit for test5 less?  

2.  For test6, it should take less than 300 seconds to run while using a depth of 6.  How long would it take to run if 
you were to use a depth of 7.  You may assume the following: 
    1.  Each game state has 3 available moves on average. 
    2. Alpha-Beta Pruning removes 1/3 of the branches.
    3. There are 30 plies in the game.

3. (Extra credit)  If you were to alter test6 to use a depth of 7, how long does your code actually take to run?  
How long does your test6 take to run?  What does this tell you about the three assumptions made in question 2?
