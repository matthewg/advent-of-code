#!/usr/bin/python3

import sys


def value_matches_fields(value, rules):
    matching_fields = set()
    for (field, field_values) in rules.items():
        valid = False
        for (bottom, top) in field_values:
            if value >= bottom and value <= top:
                valid = True
                break
        if valid:
            matching_fields.add(field)
    return matching_fields


input = sys.stdin.read()
(rule_str, yours_str, nearby_str) = input.split('\n\n')

rules = {}
for rule_line in rule_str.split('\n'):
    if not rule_line:
        continue
    (name, values_str) = rule_line.split(': ')
    values = []
    for value_str in values_str.split(' or '):
        (bottom, top) = value_str.split('-')
        values.append((int(bottom), int(top)))
    rules[name] = values

yours = (int(x) for x in yours_str.split('\n')[1].split(','))

nearby = []
for nearby_line in nearby_str.split('\n'):
    if ':' in nearby_line or not nearby_line:
        continue
    nearby.append((int(x) for x in nearby_line.split(',')))

"""
print('Rules:')
print(rules)
print()
print('Yours:')
print(yours)
print()
print('Nearby:')
print(nearby)
"""

field_possibilities = None
invalid_values = 0
for ticket in nearby:
    ticket_is_valid = True
    value_fields = []
    for value in ticket:
        matching_fields = value_matches_fields(value, rules)
        if matching_fields:
            value_fields.append(matching_fields)
        else:
            invalid_values += value
            ticket_is_valid = False
            break
    if ticket_is_valid:
        if field_possibilities is None:
            field_possibilities = value_fields
        else:
            for (existing_possibilities, new_possibilities) in zip(field_possibilities, value_fields):
                existing_possibilities.intersection_update(new_possibilities)
print(invalid_values)

while True:
    field_possibilities_counts = [len(f) for f in field_possibilities]
    if len(set(field_possibilities_counts)) == 1:
        break
    for i in range(len(field_possibilities)):
        f = field_possibilities[i]
        if len(f) == 1:
            field = list(f)[0]
            for j in range(len(field_possibilities)):
                if i == j:
                    continue
                try:
                    field_possibilities[j].remove(field)
                except KeyError:
                    pass

print('The fields are:')
for i in range(len(field_possibilities)):
    print('%d: %r' % (i, field_possibilities[i]))

departure_product = 1
for (fields, value) in zip(field_possibilities, yours):
    field = list(fields)[0]
    if not field.startswith('departure'):
        continue
    departure_product *= value
print('Departure product: %d' % departure_product)
