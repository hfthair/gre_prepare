
temp = {}

def process(src):
    lines = src.splitlines()
    title, pron = lines[0].split('  ')
    def get_briefs(line):
        t = line.split('： ')[0].strip()
        t = t[t.index(' '):].strip()
        return t

    brief = '\n'.join(get_briefs(i) for i in lines[1:] if i.startswith(' ♠'))
    return title, pron, brief, src




with open('fill_gre3000/source_from_github.txt', encoding='utf8') as f:
    c = f.read()
    sp = (i.strip().replace('A: ', ' ') for i in c.split('Q:') if i.strip())
    tps = (process(i) for i in sp)
    for i in tps:
        temp[i[0]] = i

def gre3000(w):
    if w in temp:
        return temp[w]
