#!/usr/bin/python3

import collections
import functools
import sys


MAX_CACHE = collections.defaultdict(lambda: 0)
TRANSFORM_CACHE = collections.defaultdict(dict)
def Transform(subject, loop_size):
    value = 1
    cache = TRANSFORM_CACHE[subject]
    start = MAX_CACHE[subject]
    if start in cache and start > 0:
        value = cache[start - 1]
    
    for i in range(start, loop_size):
        if i in cache:
            value = cache[i]
        else:
            value *= subject
            value %= 20201227
            cache[i] = value
            MAX_CACHE[subject] = i
    return value


# Find loop size for a or b, whichever is smaller
def FindLoopSize(subject, transform_result_a, transform_result_b):
    for i in range(100_000_000):
        if i % 1000 == 0:
            print('Checking loop size %d...' % i)
        transform = Transform(subject, i)
        if transform == transform_result_a:
            return (i, None)
        elif transform == transform_result_b:
            return (None, i)
       

def PublicKey(secret_loop_size):
    return Transform(7, secret_loop_size)


def EncryptionKey(public_key_a, loop_size_b):
    return Transform(public_key_a, loop_size_b)


public_key_a = int(sys.stdin.readline().replace('\n', ''))
public_key_b = int(sys.stdin.readline().replace('\n', ''))

(loop_size_a, loop_size_b) = FindLoopSize(7, public_key_a, public_key_b)
print('Loop size: (%r, %r)' % (loop_size_a, loop_size_b))

if loop_size_a:
    encryption_key = EncryptionKey(public_key_b, loop_size_a)
else:
    encryption_key = EncryptionKey(public_key_a, loop_size_b)
print('Encryption key: %d' % encryption_key)
