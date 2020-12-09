#!/usr/bin/python3

import collections
import sys
import utils


def Accumulate(arg, state):
    state['acc'] += arg
    state['ip'] += 1


def Jump(arg, state):
    state['ip'] += arg


def Nop(_, state):
    state['ip'] += 1


def parse_code(line, state):
    (command, arg) = line.split(' ')
    if command == 'acc':
        command_fn = Accumulate
    elif command == 'jmp':
        command_fn = Jump
    elif command == 'nop':
        command_fn = Nop
    else:
        raise Exception('Bad instruction: %r' % command)
    state['instructions'].append((command_fn, int(arg), command))


def step(state):
    ip = state['ip']
    acc = state['acc']

    if ip == len(state['instructions']):
        print('Program terminating normally with acc=%d.' % acc)
        sys.exit(0)
    elif ip > len(state['instructions']) or ip < 0:
        print('Program terminating abnormally, inslen=%d, ip=%d, acc=%d' % (len(state['instructions']), ip, acc))
        sys.exit(1)
    ins = state['instructions'][ip]

    visited = state['visited']
    if ip in visited and not state['solved_pt1']:
        print('**PART 1 SOLUTION** -- ip=%d, acc=%d' % (ip, acc))
        state['solved_pt1'] = True

    if acc in visited[ip]:
        print('Infinite loop: Already visited ip=%d with acc=%d' % (ip, acc))
        sys.exit(0)
    visited[ip].add(acc)
    
    ins[0](ins[1], state)
    new_ip = state['ip']
    new_acc = state['acc']
    print('Executing %s: ip=%d, acc=%d --> ip=%d, acc=%d' % (ins[2], ip, acc, new_ip, new_acc))
    

state = {'instructions': [], 'ip': 0, 'acc': 0, 'visited': collections.defaultdict(set), 'solved_pt1': False}
utils.call_for_lines(parse_code, state)
while True:
    step(state)
