import random
from collections import defaultdict


def all_indices_of(word, letter):
    return [idx for idx, l in enumerate(list(word)) if l == letter]


def letter_indices(word):
    results = defaultdict(list)
    for idx, letter in enumerate(list(word)):
        results[letter].append(idx)
    return results


def letter_counts(word):
    results = defaultdict(int)
    for letter in word:
        results[letter] += 1
    return results


def letter_frequencies(words):
    letter_frequencies = defaultdict(int)
    for word in words:
        for letter in set(list(word)):
            letter_frequencies[letter] += 1
    return letter_frequencies


def choose_random(words, n=1):
    if n == 1:
        return random.choice(words)
    else:
        return random.sample(words, n)
