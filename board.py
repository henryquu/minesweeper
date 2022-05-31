from time import sleep
from tkinter import Canvas
from random import randrange
from setup import FLAG, BOMB, function_running


class Cell():
    def __init__(self, master, row, column, size) -> None:
        self.val = 0
        self.row = row
        self.column = column
        self.master = master
        self.root = master.master
        self.text = None

        self.cords = (
            size*column,
            size*row,
            size*(1 + column),
            size*(1 + row)
            )

        if (column + row) % 2 == 0:
            self.fill = '#a7d948'
            self.disabledfill = '#e5c29f'
        else:
            self.fill = '#8ecc39'
            self.disabledfill = '#d7b899'

        self.id = master.create_rectangle(
            self.cords,
            width=0,
            fill=self.fill,
            activefill='#bfe17d')

        master.tag_bind(
            self.id,
            '<ButtonRelease-1>',
            lambda _: master.click(self)
            )
        master.tag_bind(self.id, '<ButtonRelease-3>', self.mark_bomb)

    def reveal(self, *_) -> None:
        if self.master.itemcget(self.id, 'state') == 'disabled':
            return

        self.master.non_mine -= 1

        if self.val == -1:
            self.master['state'] = 'disabled'
            self.root.after_cancel(self.root.timer_id)
            self.master.itemconfigure(self.id, fill='red', activefill='red')
            self.add_text(BOMB)
            self.master.mine.remove((self.row, self.column))
            self.master.mine_reveal()
            self.root.lost()
            return

        elif self.val != 0:
            self.master.itemconfigure(self.id, state='disabled')
            self.master.itemconfigure(self.id, fill=self.disabledfill)
            self.add_text()

        else:
            if self.text:
                self.master.delete(self.text)
            self.master.empty_reveal(self.row, self.column, set())

        if self.master.non_mine < 1:
            self.root.after_cancel(self.root.timer_id)
            self.master['state'] = 'disabled'
            self.root.won()

    def mark_bomb(self, *_):
        if not self.text:
            self.add_text(FLAG)
            self.master.tag_bind(
                self.text, '<Button-1>',
                lambda _: self.master.click(self)
                )
            self.master.tag_bind(self.text, '<Button-3>', self.mark_bomb)
            self.master.tag_bind(self.text, '<Enter>', self.on_hover)
            self.master.tag_bind(self.text, '<Leave>', self.on_leave)

            if self.root.marks > 0:
                self.root.marks -= 1
        else:
            self.master.delete(self.text)
            self.text = None
            sleep(0.05)
            self.on_leave()
            if self.root.marks < self.master.diff['mines']:
                self.root.marks += 1

        self.root.marks_update()

    def add_text(self, text=None) -> None:
        if text is None:
            text = self.val
        if self.text:
            self.master.delete(self.text)

        self.text = self.master.create_text(
                    self.cords[0] + self.master.diff['cell'] // 2,
                    self.cords[1] + self.master.diff['cell'] // 2,
                    text=text,
                    font='Arial, 14',
                    )

    def on_hover(self, *_) -> None:
        self.master.itemconfigure(self.id, fill='#bfe17d')

    def on_leave(self, *_) -> None:
        self.master.itemconfigure(self.id, fill=self.fill)


class Board(Canvas):
    def __init__(self, master, diff) -> None:
        Canvas.__init__(self, master)
        self.pack(fill='both', expand=True)

        self.diff = diff
        self.non_mine = diff['height'] * diff['width'] - diff['mines']

        self.board = []

        for y in range(diff['height']):
            row = [Cell(self, y, x, diff['cell']) for x in range(diff['width'])]
            self.board.append(row)

    def click(self, cell) -> None:
        self.mine_gen(cell.row, cell.column)
        self.master.update_time()
        self.click = Cell.reveal
        self.click(cell)

    @function_running
    def mine_gen(self, y: int, x: int) -> None:
        spawning_grid = self.adjacents(y, x)

        mine = set()
        while len(mine) < self.diff['mines']:
            bomb = (randrange(self.diff['height']), randrange(self.diff['width']))
            if bomb not in mine and bomb not in spawning_grid:
                mine.add(bomb)
                self.board[bomb[0]][bomb[1]].val = -1

                for y, x in self.adjacents(bomb[0], bomb[1]):
                    if self.board[y][x].val >= 0:
                        self.board[y][x].val += 1
        self.mine = mine

    @function_running
    def mine_reveal(self) -> None:
        for y, x in self.mine:
            id = self.board[y][x].id
            self.itemconfigure(id, state='disabled', fill='red')
            self.board[y][x].add_text(BOMB)
            self.master.update()
            sleep(1 / self.diff['mines'])

    def adjacents(self, y: int, x: int) -> list:
        adjacent = set()
        for yad in [-1, 0, 1]:
            indy = y + yad
            if indy >= 0 and indy < self.diff['height']:
                for xad in [-1, 0, 1]:
                    indx = x + xad
                    if indx >= 0 and indx < self.diff['width']:
                        adjacent.add((indy, indx))
        return adjacent

    def empty_reveal(self, row: int, column: int, visited: set) -> None:
        if (row, column) in visited:
            return
        visited.add((row, column))

        id = self.board[row][column].id

        self.itemconfigure(id, state='disabled')
        self.itemconfigure(id, fill=self.board[row][column].disabledfill)

        adjacents = self.adjacents(row, column)
        for y, x in adjacents:
            if not self.board[y][x].text:
                if self.itemcget(self.board[y][x].id, 'state') != 'disabled':
                    if self.board[y][x].val > 0:
                        self.board[y][x].reveal()
                    if self.board[y][x].val == 0:
                        self.non_mine -= 1
                        self.empty_reveal(y, x, visited)


if __name__ == '__main__':
    import game
    game.main()
