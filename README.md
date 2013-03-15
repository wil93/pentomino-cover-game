Pentomino covering game
=======================

In this game you have to cover the grid with pentominoes. It is inspired by http://oeis.org/A214294.

It is written in Python 2.x using Tkinter as GUI toolkit.
The game structure is very flexible: you can "easily" code different polyominos (but for the moment you must specify the coordinates of every cell, for every rotation).

Usage
------

```bash
python game.py
```

Keyboard controls
-----------------

* Restart the game: "R" key
* Rotate pentomino: left/right arrow keys (or Mousewheel scroll)
* Remove the last pentomino inserted: Backspace key
* Select a pentomino to be removed: Spacebar key
