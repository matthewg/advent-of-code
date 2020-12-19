#!/usr/bin/python3
# Augmented Rudolph-Dasher Form

import sys


def depth_str(depth):
    return ' ' * (depth*2)


class TextRule:
    def __init__(self, rule_id, text):
        self.rule_id = rule_id
        self.text = text

    def matches(self, message, rules, depth=0):
        if message.startswith(self.text):
            #print('%s%r v. rule %d: %r: Yes' % (depth_str(depth), message, self.rule_id, self.text))
            return [self.text]
        else:
            #print('%s%r v. rule %d: %r: No' % (depth_str(depth), message, self.rule_id, self.text))
            return []


class RefRule:
    def __init__(self, rule_id, options):
        # Disjunction of conjunctions
        # ((1, 2), (2, 1)) means we match one of:
        # - Rule 1 followed by rule 2
        # - Rule 2 followed by rule 1
        self.rule_id = rule_id
        self.options = options
        
    def matches(self, message, rules, depth=0):
        #print('%s%r v. rule %d: %r' % (depth_str(depth), message, self.rule_id, self.options))
        matches = self.matches_option(message, rules, self.options[0], depth+1)
        if len(self.options) > 1:
            matches += self.matches_option(message, rules, self.options[1], depth+1)
        return matches

    def matches_option(self, message, rules, option, depth=0):
        #print('%s%r v. option %r' % (depth_str(depth), message, option))
        total_matches = []
        if not message:
            return total_matches

        rule = rules[option[0]]
        rule_matches = rule.matches(message, rules, depth+1)
        if not rule_matches:
            #print('%sNo' % depth_str(depth))
            return total_matches
        for rule_match in rule_matches:
            remaining_message = message[len(rule_match):]
            consumed_message = message[0:len(rule_match)]
            if len(option) == 1:
                total_matches.append(consumed_message)
                #print('%sYes, consumed %r' % (depth_str(depth), consumed_message))
            else:
                next_matches = [consumed_message + match for match in self.matches_option(remaining_message, rules, option[1:], depth+1)]
                total_matches.extend(next_matches)
                #print('%sYes, consumed: %r' % (depth_str(depth), next_matches))
        return total_matches


def parse_rule(rule_str):
    (rule_id, rule_txt) = rule_str.split(': ')
    rule_id = int(rule_id)
    if rule_txt.startswith('"'):
        return (rule_id, TextRule(rule_id, rule_txt[1]))
    options = tuple(tuple(int(ref_rule_id) for ref_rule_id in option_txt.split(' '))
               for option_txt in rule_txt.split(' | '))
    return (rule_id, RefRule(rule_id, options))


def matches_rule(message, rule_id, rules):
    return message in rules[rule_id].matches(message, rules)


input = sys.stdin.read()
(rules_str, messages_str) = input.split('\n\n')

rules = dict(parse_rule(rule_str) for rule_str in rules_str.split('\n') if rule_str)
messages = [message for message in messages_str.split('\n') if message]

match0_count = 0
for message in messages:
    #print('')
    #print('=======')
    #print('Trying to match %r' % message)
    if matches_rule(message, 0, rules):
        #print('Success!')
        match0_count += 1
print('Matches rule 0: %d' % match0_count)
