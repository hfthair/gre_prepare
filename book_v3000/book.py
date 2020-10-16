import os
import pickle
import attr

@attr.s
class Mean(object):
    cn = attr.ib(default='')
    en = attr.ib(default='')
    synonym = attr.ib(default='')
    antonym = attr.ib(default='')
    derive = attr.ib(default='')
    eg = attr.ib(default='')

@attr.s
class Word(object):
    title = attr.ib()
    brief = attr.ib()
    full = attr.ib()
    means = attr.ib(default=None)
    position = attr.ib(default=0)


def create_word(src):
    lines = src.splitlines()
    title, _ = lines[0].split('  ')

    means = []
    mean = None
    for line in lines[1:]:
        if line.startswith(' ♠'):
            mean = Mean()
            cn = line.split('：')[0].strip()
            mean.cn = cn[cn.index(' '):].strip()
            mean.en = line.replace(cn, '').strip()
            # mean.synonym = ''
            # mean.antonym = ''
            # mean.eg = ''
            # mean.derive = ''
            means.append(mean)
        elif line.startswith(' ♣近'):
            if mean.synonym != '':
                # some error of source
                mean.antonym = line.replace(' ♣近', '').strip()
                continue
            mean.synonym = line.replace(' ♣近', '').strip()
        elif line.startswith(' ♣反'):
            mean.antonym = line.replace(' ♣反', '').strip()
        elif line.startswith(' ♣例'):
            mean.eg = line.replace(' ♣例', '').strip()
        elif line.startswith(' ♣派'):
            mean.derive = line.replace(' ♣派', '').strip()

    brief = '\n'.join(i.cn for i in means)

    return Word(title, brief, src, means)

byTitle = {}
byList = {}
arrayAll = []

__dir, _ = os.path.split(__file__)

pickle_path = os.path.join(__dir, 'data/yaoniming3000.pickle')
if os.path.exists(pickle_path):
    with open(pickle_path, 'rb') as f:
        byTitle, arrayAll, byList = pickle.load(f)
else:
    import pandas as pd

    with open(os.path.join(__dir, 'static/source_from_github.txt'), encoding='utf8') as f:
        c = f.read()
        sp = (i.strip().replace('A: ', ' ') for i in c.split('Q:') if i.strip())
        tps = (create_word(i) for i in sp)
        for i in tps:
            if i.title in byTitle:
                print('!!!!! dupulicated in source --> ' + i.title)
                continue
            arrayAll.append(i)
            byTitle[i.title] = i

    for i in range(1, 32):
        byList[i] = []
        sheet = pd.read_excel(os.path.join(__dir, 'static/GRE3000.xlsx'), 'L' + str(i), header=None)
        l = sheet[0].values.tolist()
        for w in l:
            if w not in byTitle:
                print('missing ---> |{}| in list{}({})'.format(w, i, l.index(w)+1))
                continue
            byTitle[w].position = i
            byList[i].append(byTitle[w])

    for i in arrayAll:
        if i.position == 0:
            byList[31].append(i)

    with open(pickle_path, 'wb') as f:
        pickle.dump((byTitle, arrayAll, byList), f)

def search(w):
    if w in byTitle:
        return byTitle[w]



def synonym(w):
    res = []
    for m in w.means:
        s = m.synonym
        s = ''.join(i for i in s if ord(i) < 128)
        s = s.replace(',', ' ')
        l = [i.strip() for i in s.split(' ') if i.strip()]
        res.extend(l)
    res = set(res)
    res = [i for i in res if i in byTitle]
    return res


