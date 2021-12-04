#!/usr/bin/python3

import re
import utils


def all_cells_marked(rowcol):
    for cell in rowcol:
        if not cell.marked:
            return False
    return True


class Cell:

    def __init__(self, value):
        self.value = value
        self.marked = False

    def mark(self):
        self.marked = True

    def __str__(self):
        if self.marked:
            return '*{:2}*'.format(self.value)
        else:
            return ' {:2} '.format(self.value)


class Board:
    
    def __init__(self, lines):
        self.cells_by_value = {}
        
        self.rows = []
        for line in lines:
            line = re.sub('^ +', '', re.sub(' +$', '', line))
            row = []
            for value_s in re.split(' +', line):
                value = int(value_s)
                cell = Cell(value)
                row.append(cell)
                self.cells_by_value[value] = cell
            self.rows.append(row)

        self.columns = []
        for column_idx in range(len(self.rows[0])):
            column = []
            for row in self.rows:
                column.append(row[column_idx])
            self.columns.append(column)

    def __str__(self):
        return '\n'.join(map(lambda row: ' '.join(map(str, row)), self.rows))

    def is_winner(self):
        for row in self.rows:
            if all_cells_marked(row):
                return True
            
        for column in self.columns:
            if all_cells_marked(column):
                return True

        return False

    def score(self, winning_number):
        unmarked_sum = 0
        for row in self.rows:
            for cell in row:
                if not cell.marked:
                    unmarked_sum += cell.value
        return unmarked_sum * winning_number


def get_bingo(lines, state):
    if len(lines) == 1:
        state['numbers'] = map(int, lines[0].split(','))
    else:
        state['boards'].append(Board(lines))


state = {
    'numbers': [],
    'boards': [],
}
utils.call_for_records(get_bingo, state)
print('State: {}'.format(state))

unwon_boards = set(state['boards'])
for number in state['numbers']:
    print('About to mark {} on {} boards'.format(number, len(state['boards'])))
    for board in state['boards']:
        cell = board.cells_by_value.get(number)
        if not cell:
            continue
        cell.mark()
        if board.is_winner():
            if board in unwon_boards:
                print('Board has won with {}'.format(number))
                print(board)
                unwon_boards.remove(board)
                print('Board score: {}'.format(board.score(number)))
    if not unwon_boards:
        break
