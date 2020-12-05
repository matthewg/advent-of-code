#!/usr/bin/python3

import re
import sys

REQUIRED_FIELDS = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
VALIDATORS = {
    'byr': lambda v: intInRange(v, 1920, 2002),
    'iyr': lambda v: intInRange(v, 2010, 2020),
    'eyr': lambda v: intInRange(v, 2020, 2030),
    'hgt': lambda v: numSuffixRange(v, 'cm', 150, 193) or numSuffixRange(v, 'in', 59, 76),
    'hcl': lambda v: re.match(r'#[0-9a-f]{6}$', v),
    'ecl': lambda v: v in ('amb', 'blu', 'brn', 'grn', 'gry', 'hzl', 'oth'),
    'pid': lambda v: re.match(r'\d{9}$', v),
    'cid': lambda _: True,
}


def intInRange(v, bottom, top):
    if not re.match(r'\d+$', v):
        return False
    v = int(v)
    return v >= bottom and v <= top


def numSuffixRange(v, suffix, bottom, top):
    g = re.match(r'(\d+)' + suffix + '$', v)
    if not g:
        return False
    v = int(g.group(1))
    return v >= bottom and v <= top


def main():
    validCount1 = 0
    validCount2 = 0
    passportLines = []
    while True:
        line = sys.stdin.readline()
        if line and line != '\n':
            passportLines.append(line.replace('\n', ''))
            continue

        passport = ' '.join(passportLines)
        (isValid1, isValid2) = validate(passport)
        if isValid1:
            validCount1 += 1
        if isValid2:
            validCount2 += 1

        passportLines = []
        if not line:
            break

    print(validCount1)
    print(validCount2)


def validate(passport):
    passportFields = [fieldPair.split(':') for fieldPair in passport.split(' ')]
    fieldsPresent = set([field[0] for field in passportFields])
    valid1 = fieldsPresent.issuperset(REQUIRED_FIELDS)

    valid2 = valid1
    invalidFields = []
    for field in passportFields:
        if not VALIDATORS[field[0]](field[1]):
            invalidFields.append(field[0])
            valid2 = False
    
    #missing = REQUIRED_FIELDS.difference(fieldsPresent)
    #print(passport)
    #print('Valid=(%r, %r) for %r (missing: %r; invalid:%r)' % (valid1, valid2, fieldsPresent, missing, invalidFields))
    #print()

    return (valid1, valid2)


if __name__ == '__main__':
    main()
