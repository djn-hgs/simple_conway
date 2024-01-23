import tkinter as tk
from enum import IntEnum

WIDTH = 30
HEIGHT = 20

NEIGHBOUR_OFFSETS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]

TICK = 10


class State(IntEnum):
    dead = 0
    alive = 1


class Cell(tk.Button):
    def __init__(self, master: 'ConwayGrid', pos, *args, **kwargs):

        super().__init__(master, command=self.clicked, *args, **kwargs)

        self.master: 'ConwayGrid' = master
        self.i, self.j = pos
        self.neighbours = []
        self.state = State.dead
        self.new_state = None
        self.off()

    def on(self):
        self.state = State.alive
        self.new_state = State.alive
        self.configure(relief=tk.SUNKEN, bg='blue')

    def off(self):
        self.state = State.dead
        self.new_state = State.dead
        self.configure(relief=tk.RAISED, bg='red')

    def set_new_state(self, state: State):
        self.new_state = state

    def apply_new_state(self):
        if self.new_state == State.alive:
            self.on()
        elif self.new_state == State.dead:
            self.off()
        else:
            self.off()

    def flip(self):
        if self.state == State.dead:
            self.on()
        elif self.state == State.alive:
            self.off()
        else:
            self.on()

        self.master.update_count()

    def clicked(self):
        self.flip()

    @property
    def neighbour_count(self):
        return sum(n.state for n in self.neighbours)


class ConwayGrid(tk.Frame):
    def __init__(self, master, size, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.running = False
        self.master = master
        self.entries = {}
        self.width, self.height = size
        self.show_neighbours = False

        self.populate()
        self.get_neighbours()

    def populate(self):
        for j in range(self.height):
            for i in range(self.width):
                new_cell = Cell(self, (i, j))

                self.entries[(i, j)] = new_cell

                new_cell.grid(row=j, column=i, sticky='news')

        for i in range(self.width):
            self.columnconfigure(i, weight=1)
        for j in range(self.height):
            self.rowconfigure(j, weight=1)

    def tick(self):
        self.update_conway()

        if self.running:
            self.after(TICK, self.tick)

    def start(self):
        self.running = True
        self.tick()

    def stop(self):
        self.running = False

    def show_count(self):
        if self.show_neighbours:
            self.show_neighbours = False
            for cell in self.entries.values():
                cell.configure(text='')
        else:
            self.show_neighbours = True
            self.update_count()

    def update_count(self):
        if self.show_neighbours:
            for cell in self.entries.values():
                cell.configure(text=f'{cell.neighbour_count}')

    def reset(self):
        for cell in self.entries.values():
            cell.off()
        self.update_count()

    def update_conway(self):
        for cell in self.entries.values():
            neighbour_count = cell.neighbour_count

            if self.show_neighbours:
                cell.configure(text=f'{neighbour_count}')

            if cell.state == State.alive and (neighbour_count < 2 or neighbour_count > 3):
                cell.set_new_state(State.dead)
            elif cell.state == State.dead and neighbour_count == 2:
                cell.set_new_state(State.alive)

        for cell in self.entries.values():
            cell.apply_new_state()

    def get_neighbours(self):
        for pos in self.entries:
            cell = self.entries[pos]

            i, j = cell.i, cell.j

            for x, y in NEIGHBOUR_OFFSETS:
                if x + i in range(self.width) and y + j in range(self.height):
                    cell.neighbours.append(self.entries[(x + i, y + j)])


class Controls(tk.Frame):
    def __init__(self, master, conway_grid: ConwayGrid, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.master = master
        self.conway_grid = conway_grid

        start_button = tk.Button(self, text='Start', command=self.conway_grid.start)
        tick_button = tk.Button(self, text='Tick', command=self.conway_grid.tick)
        stop_button = tk.Button(self, text='Stop', command=self.conway_grid.stop)
        count_button = tk.Button(self, text='Count', command=self.conway_grid.show_count)
        reset_button = tk.Button(self, text='Reset', command=self.conway_grid.reset)

        start_button.grid(row=0, column=0)
        tick_button.grid(row=0, column=1)
        stop_button.grid(row=0, column=2)
        count_button.grid(row=0, column=3)
        reset_button.grid(row=0, column=4)

        for i in range(5):
            self.columnconfigure(i, weight=1)


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x400')

    my_grid = ConwayGrid(root, size=(WIDTH, HEIGHT))
    my_controls = Controls(root, my_grid)

    my_grid.grid(sticky='news')
    my_controls.grid()

    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    root.mainloop()
