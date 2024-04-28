import time
import random

from cell import Cell
from graphics import Window


class Maze:
    def __init__(
        self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        if self._seed is not None:
            random.seed(seed)
        self._directions = {
            (1, 0): "right",
            (0, 1): "bottom",
            (-1, 0): "left",
            (0, -1): "top",
        }
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0]._has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1]._has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            to_visit = []
            for dx, dy in self._directions.keys():
                new_x, new_y = i + dx, j + dy
                if self._is_valid_cell(new_x, new_y):
                    if not self._cells[new_x][new_y]._visited:
                        to_visit.append((dx, dy))
            if len(to_visit) == 0:
                return
            else:
                dx, dy = random.choice(to_visit)
                if self._directions[(dx, dy)] == "right":
                    self._cells[i][j].has_right_wall = False
                    self._cells[i + dx][j + dy].has_left_wall = False
                elif self._directions[(dx, dy)] == "left":
                    self._cells[i][j].has_left_wall = False
                    self._cells[i + dx][j + dy].has_right_wall = False
                elif self._directions[(dx, dy)] == "top":
                    self._cells[i][j].has_top_wall = False
                    self._cells[i + dx][j + dy].has_bottom_wall = False
                else:
                    self._cells[i][j].has_bottom_wall = False
                    self._cells[i + dx][j + dy].has_top_wall = False
                self._break_walls_r(i + dx, j + dy)

    def _is_valid_cell(self, i, j):
        return 0 <= i < self._num_cols and 0 <= j < self._num_rows

    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j]._visited = True
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True
        for dx, dy in self._directions.keys():
            if self._is_valid_cell(i + dx, j + dy):
                if (
                    self._directions[(dx, dy)] == "top"
                    and not self._cells[i][j].has_top_wall
                    and not self._cells[i][j]._visited
                ):
                    self._cells[i][j].draw_move(self._cells[i + dx][j + dy])
                    if self._solve_r(i + dx, j + dy):
                        return True
                    else:
                        self._cells[i][j].draw_move(
                            self._cells[i + dx][j + dy], undo=True
                        )
        return False
