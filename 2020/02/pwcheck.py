#!/usr/bin/python3

import functools
import operator
import re
import sys
pw_re = re.compile(r'(\d+)-(\d+) ([a-z]): ([a-z]+)\n')

valid1_count = 0
valid2_count = 0

for line in sys.stdin.readlines():
    match = pw_re.match(line)
    if not match:
        sys.stderr.write('Bad line: %r\n' % line)
        sys.exit(1)
    a = int(match.group(1))
    b = int(match.group(2))
    letter = match.group(3)
    pw = match.group(4)

    count = len([c for c in pw if c == letter])
    if count >= a and count <= b:
        valid1_count += 1

    if (pw[a-1] == letter) ^ (pw[b-1] == letter):
        valid2_count += 1

print(valid1_count)
print(valid2_count)
