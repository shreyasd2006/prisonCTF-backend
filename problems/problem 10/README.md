There is a bug in the board initialization code:
his creates rows that reference the same list, so modifying one row affects all rows.

You need to fix this bug and also support a command-style interface:

Commands:

make_board w h → create a new board of size h × w (height × width).

set i j val → set the cell at row i, column j to the string val.

At the end, print the board as a Python list of lists.