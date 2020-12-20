import sys


def call_for_lines(fn, state):
    for line in sys.stdin.readlines():
        fn(line.replace('\n', ''), state)


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
