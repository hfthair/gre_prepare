from yaoniming3000 import wordByTitle
from difflib import SequenceMatcher as SM
from itertools import combinations

def common_substr(a, b):
    sm = SM(None, a, b)
    i, _, k = sm.find_longest_match(0, len(a), 0, len(b))
    if k > 6:
        return a[i:i+k]
    return None

all_words = wordByTitle.keys()
col = {}
for i, j in combinations(all_words, 2):
    c = common_substr(i, j)
    if c:
        if c not in col:
            col[c] = set()
        col[c].add(i)
        col[c].add(j)

keys = sorted(col.keys(), key=lambda x: len(x), reverse=True)




if __name__ == '__main__':
    pass
    # print(common_substr('xxabxcdyy', 'asabcdykdls'))
