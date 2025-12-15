import collections
import sys


def call_for_lines(fn, state):
    line_idx = 0
    for line in sys.stdin.readlines():
        fn(line.replace('\n', ''), state, line_idx)
        line_idx += 1


def call_for_records(fn, state):
    lines = []
    while True:
        line = sys.stdin.readline()
        if line == '\n' or not line:
            if lines:
                fn(lines, state)
                lines = []
            if not line:
                break
        else:
            lines.append(line.replace('\n', ''))


class Cell:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value


class GridIter:
    def __init__(self, grid):
        self._grid = grid
        self._row = 0
        self._col = 0

    def __next__(self):
        if self._grid.rows and self._col >= len(self._grid.rows[0]):
            self._col = 0
            self._row += 1
        if self._row >= len(self._grid.rows):
            raise StopIteration
        item = self._grid.Cell(self._row, self._col)
        self._col += 1
        return item


class Grid:
    def __init__(self, parse_cell_fn):
        self.rows = []
        self.parse_cell_fn = parse_cell_fn

    def __str__(self):
        return '\n'.join([''.join([c.value for c in r]) for r in self.rows])

    def __iter__(self):
        return GridIter(self)

    def Parse(self, state):
        call_for_lines(self._AddRow, state)

    def _AddRow(self, row_str, state, row_idx):
        row = []
        for col_idx, cell_s in enumerate(row_str):
            row.append(Cell(row=row_idx, col=col_idx, value=self.parse_cell_fn(cell_s)))
        self.rows.append(row)

    def Cell(self, row_idx, col_idx):
        if row_idx >= len(self.rows):
            return None
        row = self.rows[row_idx]
        if col_idx >= len(row):
            return None
        return row[col_idx]

    def Height(self):
        return len(self.rows)

    def Width(self):
        if self.rows:
            return len(self.rows[0])
        else:
            return 0
    
    def AdjacentCells(self, cell, include_diagonal):
        row = cell.row
        col = cell.col
        ret = []
        for d_x, d_y in ((-1, 0), (1, 0), (0, -1), (0, 1),
                         (-1, -1), (1, 1), (-1, 1), (1, -1)):
            if d_x != 0 and d_y != 0 and not include_diagonal:
                continue
            row2 = row + d_x
            col2 = col + d_y
            if row2 < 0 or col2 < 0 or row2 >= len(self.rows) or col2 >= len(self.rows[0]):
                continue
            ret.append(self.Cell(row2, col2))
        return ret
