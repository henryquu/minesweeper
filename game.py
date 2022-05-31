from time import gmtime, strftime
import tkinter as tk
from tkinter.messagebox import askokcancel
from setup import DIFFICULTY, FLAG, CLOCK, function_running
from board import Board


class Game(tk.Tk):
    def __init__(self) -> None:
        tk.Tk.__init__(self)
        self.title('Minesweeper')
        self.resizable(False, False)

        self.chosen_diff = tk.StringVar(value='Easy')
        self.diff = DIFFICULTY[self.chosen_diff.get()]

        self.geometry(
            (f"{self.diff['game_width']}x{self.diff['game_height']}"
             f"+{self.winfo_screenwidth() // 3}+0")
            )

        self.frame = tk.Frame(self, height=60, bg='#3B5E23')
        self.frame.pack(fill='x')
        self.frame.option_add('*Background', '#3B5E23')
        self.frame.option_add('*Font', 'Arial, 14')
        self.frame.grid_propagate(False)

        self.diff_menu = tk.OptionMenu(
            self.frame,
            self.chosen_diff,
            *DIFFICULTY,
            command=self.change_diff
            )
        self.diff_menu.config(
            bg='#181a1b',
            fg='#c6c1ba',
            activebackground='#181a1b',
            activeforeground='#c6c1ba',
            highlightthickness=0
            )
        self.diff_menu['menu'].config(bg='#181a1b', fg='#c6c1ba', bd=0)
        self.diff_menu.grid(row=0, column=0, pady=15, padx=10)

        self.marks = self.diff['mines']
        self.marks_label = tk.Label(self.frame, text=FLAG + f"{self.marks:02d}")
        self.marks_label.grid(row=0, column=1, padx=8, pady=15)

        self.time = 0
        self.timer = tk.Label(
            self.frame,
            text=CLOCK + strftime("%M:%S", gmtime(self.time)),
            )
        self.timer.grid(row=0, column=2, pady=15)
        self.timer_id = None
        self.frame.columnconfigure(2, weight=5)

        self.restart_button = tk.Button(
            self.frame,
            text='Restart',
            command=function_running(self.new_game)
            )

        self.restart_button.grid(row=0, column=4, sticky='e', padx=8, pady=10)
        self.frame.columnconfigure(4, weight=2)

        self.board = Board(self, self.diff)

    def lost(self) -> None:
        if askokcancel(
                title='You lost',
                message='Maybe next time! Do you wish to play again?'):
            self.new_game()

    def won(self) -> None:
        if askokcancel(
                title='You Won',
                message='Congratulations! Do you wish to play again?'):
            self.new_game()

    @function_running
    def change_diff(self, *_) -> None:
        self.diff = DIFFICULTY[self.chosen_diff.get()]
        self.geometry(f"{self.diff['game_width']}x{self.diff['game_height']}")
        self.frame.update()
        self.new_game()

    def new_game(self) -> None:
        if self.timer_id:
            self.after_cancel(self.timer_id)

        self.marks = self.diff['mines']
        self.marks_update()

        self.time = 0
        self.timer['text'] = CLOCK + strftime("%M:%S", gmtime(self.time))

        self.board.destroy()
        self.board = Board(self, self.diff)

    def update_time(self) -> None:
        self.time += 1
        if self.time / 60 < 60:
            self.timer['text'] = CLOCK + strftime("%M:%S", gmtime(self.time))
        else:
            self.timer['text'] = CLOCK + strftime("%H:%M:%S", gmtime(self.time))
        self.timer_id = self.after(1000, self.update_time)

    def marks_update(self) -> None:
        self.marks_label['text'] = FLAG + f"{self.marks:02d}"


def main():
    game = Game()
    game.mainloop()


if __name__ == '__main__':
    main()
