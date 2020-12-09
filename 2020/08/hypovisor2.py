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
        return True
    elif ip > len(state['instructions']) or ip < 0:
        print('Program terminating abnormally, inslen=%d, ip=%d, acc=%d' % (len(state['instructions']), ip, acc))
        return True
    ins = state['instructions'][ip]

    ins[0](ins[1], state)
    new_ip = state['ip']
    new_acc = state['acc']
    #print('Executing %s: ip=%d, acc=%d --> ip=%d, acc=%d' % (ins[2], ip, acc, new_ip, new_acc))
    return False


state = {'instructions': [], 'ip': 0, 'acc': 0}
utils.call_for_lines(parse_code, state)

vms = []
changed_ins = []
for i in range(len(state['instructions'])):
    instruction = state['instructions'][i]
    if instruction[2] == 'jmp':
        new_instruction = (Nop, instruction[1], 'nop')
    elif instruction[2] == 'nop':
        new_instruction = (Jump, instruction[1], 'jmp')
    else:
        continue

    new_state = {
        'instructions': state['instructions'][:],
        'ip': 0,
        'acc': 0,
    }
    new_state['instructions'][i] = new_instruction
    changed_ins.append(i)
    vms.append(new_state)

print('Executing %d VMs' % len(vms))
i = 0
while True:
    if i % 100 == 0:
        print('Executed all VMs %d times' % i)
    for i in range(len(vms)):
        vm = vms[i]
        if step(vm):
            print('VM with change in instruction %d terminated' % changed_ins[i])
            sys.exit(0)
    i += 1
