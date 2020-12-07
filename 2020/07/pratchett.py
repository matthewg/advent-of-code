#!/usr/bin/python3

import utils


class Node:
    def __init__(self):
        self.srcs = set()


    def __repr__(self):
        return 'Node(%r)' % self.srcs


def parse_rules(rule, state):
    rules = state['rules']
    rule = rule.replace('.', '').replace(' bags', '').replace(' bag', '')
    rule_components = rule.split(' contain ')
    if len(rule_components) != 2:
        raise Exception('Unexpected rule: %r' % rule)
    
    bagtype = rule_components[0]
    if bagtype in rules:
        raise Exception('Bagtype %r already in rules at %r' % (bagtype, rule))
    contains = {}
    rules[bagtype] = contains
    
    for contains_rule in rule_components[1].split(', '):
        contains_data = contains_rule.split(' ', 1)
        if contains_data[0] == 'no':
            qty = 0
        else:
            qty = int(contains_data[0])
        contains[contains_data[1]] = qty


def get_qty(outer_color, inner_color, rules):
    color_rules = rules.get(outer_color, {})
    target_qty = color_rules.get(inner_color, color_rules.get('other', 0))
    return target_qty


def find_path(nodes, c, target, visited):
    if target in c.srcs:
        return True
    for node in c.srcs:
        if node in visited:
            continue
        visited.add(node)
        if find_path(nodes, node, target, visited):
            return True
    return False


def bags_inside(color, rules, depth = 0):
    qty = 1
    depth_prefix = '....' * depth
    print('%sLooking for bags inside %s' % (depth_prefix, color))
    for inner_color in rules[color]:
        inner_qty = rules[color][inner_color]
        print('%s....inner_qty for %s: %d' % (depth_prefix, inner_color, inner_qty))
        if inner_qty == 0:
            continue
        qty += inner_qty * bags_inside(inner_color, rules, depth + 1)
    print('%sBags inside %s: %d' % (depth_prefix, color, qty))
    return qty


state = {'rules': {}}
utils.call_for_lines(parse_rules, state)
#for k in sorted(state['rules']):
#    print('%s: %r' % (k, state['rules'][k]))

colors = set(state['rules'].keys())
colors.add('shiny gold')
print('Colors: %r' % colors)

nodes = dict((color, Node()) for color in colors)
for outer_color in state['rules']:
    for inner_color in colors:
        if get_qty(outer_color, inner_color, state['rules']) > 0:
            nodes[inner_color].srcs.add(nodes[outer_color])
#print('Nodes: %r' % nodes)


valid_shiny_gold_starts = set()
for c in colors:
    if find_path(nodes, nodes['shiny gold'], nodes[c], set()):
        #print('Found path for %s' % c)
        valid_shiny_gold_starts.add(c)
print('Valid starting colors for shiny gold: %d' % len(valid_shiny_gold_starts))

shiny_gold_contains = bags_inside('shiny gold', state['rules'])
# Subtract 1 to avoid counting the shiny gold bag itself
print('Shiny gold must contain %d bags' % (shiny_gold_contains-1))
