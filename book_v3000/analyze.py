import pickle
import os
from difflib import SequenceMatcher as SM
from itertools import combinations
from . import book

def common_substr(a, b):
    sm = SM(None, a, b)
    i, _, k = sm.find_longest_match(0, len(a), 0, len(b))
    if k > 3:
        return a[i:i+k]
    return None

substrs = {}
keys = []

__dir, _ = os.path.split(__file__)

pickle_path = os.path.join(__dir, 'data/analyze3000.pickle')

if os.path.exists(pickle_path):
    with open(pickle_path, 'rb') as f:
        substrs, keys = pickle.load(f)
else:
    all_words = book.byTitle.keys()

    for i, j in combinations(all_words, 2):
        c = common_substr(i, j)
        if c:
            if c not in substrs:
                substrs[c] = set()
            substrs[c].add(i)
            substrs[c].add(j)

    keys = sorted(substrs.keys(), key=lambda x: len(x), reverse=True)
    with open(pickle_path, 'wb') as f:
            pickle.dump((substrs, keys), f)


if __name__ == '__main__':
    from colorama import init, Fore, Style
    init(autoreset=True)
    for k in keys:
        print('============= {} ============'.format(k))
        input('_')
        for w in substrs[k]:
            wx = w + ' ' * 18
            ms = ' | '.join(m.cn for m in book.byTitle[w].means)
            print(Fore.GREEN + wx[:18] + Fore.RESET + ms)
        input('_')
