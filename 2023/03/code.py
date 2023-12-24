#!/usr/bin/python3
import utils


class Cell:
    def __init__(self, value):
        self.value = value
        self.number = None
        self.number_val = 0

    def __str__(self):
        return self.value


state = {'grid': utils.Grid(Cell)}
state['grid'].Parse(state)

for cell in state['grid']:
    if cell.value.value.isdigit():
        if cell.value.number:
            continue
        cell2 = cell
        while cell2 and cell2.value.value.isdigit():
            cell2.value.number = cell.value
            cell.value.number_val *= 10
            cell.value.number_val += int(cell2.value.value)
            cell2 = state['grid'].Cell(cell2.row, cell2.col + 1)

seen_numbers = set()
num_sum = 0
gear_sum = 0
for cell in state['grid']:
    if cell.value.value.isdigit() or cell.value.value == '.':
        continue
    adj_seen_numbers = set()
    for adj_cell in state['grid'].AdjacentCells(cell, include_diagonal=True):
        if not adj_cell.value.number:
            continue
        adj_seen_numbers.add(adj_cell.value.number)
        if adj_cell.value.number in seen_numbers:
            continue
        num_sum += adj_cell.value.number.number_val
        seen_numbers.add(adj_cell.value.number)
    if cell.value.value == '*' and len(adj_seen_numbers) == 2:
        gears = list(adj_seen_numbers)
        gear_sum += gears[0].number_val * gears[1].number_val
print(num_sum)
print(gear_sum)
