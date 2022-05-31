# minesweeper
Minesweeper in python using tkinter

Board Generation:
- start generating bombs only after user clicks first cell
- no bombs around user's click
- add bomb count to cells around every bomb
 
Gameplay:
- click on empty cell reveals all connected horizontally and verticaly empty cells
- click on number reveals it
- click on revealed cell -> do nothing
- right click not revealed cell - mark as bomb
- all non-bomb cells revealed -> win
- click on bomb -> lost game, show all bombs 

GUI based on Google Minesweeper game.

GUI contains:
- upper frame:
    - difficulty menu
    - counter of unmarked bombs
    - timer
    - restart button
- grid
- highlight hovered cells

Difficulty - Nr of bombs - Height - Width:
Easy            10           8        10
Medium          40          14        18
Hard            99          20        24
