#!/usr/bin/python3

import collections
import re
import utils


def ParseFood(food_str, state):
    g = re.fullmatch(r'(.*?)(?: [(]contains (.*)[)])?', food_str)
    ingredients = set(g.group(1).split(' '))
    allergens = g.group(2).split(', ')
    for ingredient in ingredients:
        state['ingredient_count'][ingredient] += 1

    print('Got food %r' % food_str)
    for allergen in allergens:
        if allergen in state['allergen_candidates']:
            candidate_set = state['allergen_candidates'][allergen]
            print('Previous potential sources of allergen %r: %r' % (allergen, candidate_set))
            candidate_set.intersection_update(ingredients)
            print('After incorporating %r: %r' % (ingredients, candidate_set))
        else:
            print('Potential sources of allergen %r: %r' % (allergen, ingredients))
            state['allergen_candidates'][allergen] = set(ingredients)


state = {'ingredient_count': collections.defaultdict(lambda: 0),
         'allergen_candidates': {}}
utils.call_for_lines(ParseFood, state)
print('')

print('Allergen candidates:')
allergens_by_ingredient = collections.defaultdict(set)
for allergen in sorted(state['allergen_candidates'].keys()):
    allergen_candidates = state['allergen_candidates'][allergen]
    print('%s: %r' % (allergen, allergen_candidates))
    for ingredient in allergen_candidates:
        allergens_by_ingredient[ingredient].add(allergen)
print('')

while True:
    unique_candidates = set(list(candidates)[0] for (allergen, candidates) in state['allergen_candidates'].items()
                            if len(candidates) == 1)
    print('Unique candidates: %r' % unique_candidates)
    if len(unique_candidates) == len(state['allergen_candidates']):
        break
    improved_uniqueness = False
    for (allergen, candidates) in state['allergen_candidates'].items():
        if len(candidates) == 1:
            continue
        unique_to_remove = candidates.intersection(unique_candidates)
        if unique_to_remove:
            candidates.difference_update(unique_candidates)
            improved_uniqueness = True
            print('Removing %r from %r leaves %r' % (unique_to_remove, allergen, candidates))
    if not improved_uniqueness:
        raise Exception('Could not make candidates more unique')
print('')

print('Allergen candidates after uniqifying:')
ingredients_and_allergens = []
for allergen in sorted(state['allergen_candidates'].keys()):
    allergen_ingredient = state['allergen_candidates'][allergen].pop()
    print('%s: %s' % (allergen, allergen_ingredient))
    ingredients_and_allergens.append((allergen_ingredient, allergen))
ingredients_and_allergens.sort(key=lambda a: a[1])
print('')

print('No-allergen ingredients:')
no_allergen_count = 0
for (ingredient, count) in sorted(state['ingredient_count'].items(), key=lambda x:x[0]):
    if allergens_by_ingredient[ingredient]:
        continue
    print(ingredient)
    no_allergen_count += count
print('')

print('No-allergen count: %d' % no_allergen_count)
print('Part 2 answer: %s' % ','.join([a[0] for a in ingredients_and_allergens]))
