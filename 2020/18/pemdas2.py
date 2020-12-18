#!/usr/bin/python3

import utils


def finish_token(curr_token, curr_tokens):
    if curr_token:
        curr_tokens.append(int(''.join(curr_token)))
        curr_token.clear()


def calculate(line, state):
    #print('Calculating %r' % line)
    stack = []
    curr_tokens = []
    curr_token = []

    i = 0
    for c in line:
        i += 1
        if c == '(':
            if curr_token:
                raise Exception('Unexpected curr_token %r at pos %d of %r' % (curr_token, i, line))
            stack.append(curr_tokens)
            curr_tokens = []
        elif c == ')':
            finish_token(curr_token, curr_tokens)
            subexpr_val = eval_expr(curr_tokens)
            curr_tokens = stack.pop()
            curr_tokens.append(subexpr_val)
        elif c == ' ':
            finish_token(curr_token, curr_tokens)
        elif c in ('+', '*'):
            finish_token(curr_token, curr_tokens)
            curr_tokens.append(c)
        elif c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            curr_token.append(c)
        else:
            raise Exception('Unknown character %r at pos %d of %r' % (c, i, line))
    if stack:
        raise Exception('Missing close paren in %r' % line)
    finish_token(curr_token, curr_tokens)
    val = eval_expr(curr_tokens)
    print('{0}: {1}'.format(line, val))
    state['sum'] += val


def eval_expr(tokens):
    #print('Evaluating %r' % tokens)

    # Addition pass
    mult_tokens = []
    lhs = tokens.pop(0)
    while tokens:
        op = tokens.pop(0)
        if op == '+':
            lhs = lhs + tokens.pop(0)
        elif op == '*':
            mult_tokens.append(lhs)
            mult_tokens.append('*')
            lhs = tokens.pop(0)
            #print('Got *, mult_tokens is now %r, %r on deck' % (mult_tokens, lhs))
        else:
            raise Exception('Unexpected token %r' % op)
    mult_tokens.append(lhs)

    #print('After adding: %r' % mult_tokens)
    val = mult_tokens.pop(0)
    while mult_tokens:
        op = mult_tokens.pop(0)
        if op == '*':
            val *= mult_tokens.pop(0)
        else:
            raise Exception('Unexpected token %r' % op)
    return val


state = {'sum': 0}
utils.call_for_lines(calculate, state)
print('Grand total: %d' % state['sum'])
