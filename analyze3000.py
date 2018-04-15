import pickle
import os
from yaoniming3000 import wordByTitle
from difflib import SequenceMatcher as SM
from itertools import combinations


def common_substr(a, b):
    sm = SM(None, a, b)
    i, _, k = sm.find_longest_match(0, len(a), 0, len(b))
    if k > 3:
        return a[i:i+k]
    return None

substrs = {}
keys = []

if os.path.exists('gre3000/analyze3000.pickle'):
    with open('gre3000/analyze3000.pickle', 'rb') as f:
        substrs, keys = pickle.load(f)
else:
    all_words = wordByTitle.keys()

    for i, j in combinations(all_words, 2):
        c = common_substr(i, j)
        if c:
            if c not in substrs:
                substrs[c] = set()
            substrs[c].add(i)
            substrs[c].add(j)

    keys = sorted(substrs.keys(), key=lambda x: len(x), reverse=True)
    with open('gre3000/analyze3000.pickle', 'wb') as f:
            pickle.dump((substrs, keys), f)


if __name__ == '__main__':
    # print('\n'.join(substrs[keys[0]]))
    print('\n'.join(keys))
