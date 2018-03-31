import attr

@attr.s
class Word(object):
    title = attr.ib()
    pronounce = attr.ib()
    brief = attr.ib()
    full = attr.ib()

# todo: save to db
temp = {}

def process(src):
    lines = src.splitlines()
    title, pron = lines[0].split('  ')
    def get_briefs(line):
        t = line.split('：')[0].strip()
        t = t[t.index(' '):].strip()
        return t

    brief = '\n'.join(get_briefs(i) for i in lines[1:] if i.startswith(' ♠'))
    return Word(title, pron, brief, src)

with open('gre3000/source_from_github.txt', encoding='utf8') as f:
    c = f.read()
    sp = (i.strip().replace('A: ', ' ') for i in c.split('Q:') if i.strip())
    tps = (process(i) for i in sp)
    for i in tps:
        temp[i.title] = i

def search(w):
    if w in temp:
        return temp[w]
