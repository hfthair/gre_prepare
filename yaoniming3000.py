import attr

@attr.s
class Word(object):
    title = attr.ib()
    pronounce = attr.ib()
    brief = attr.ib()
    full = attr.ib()

# todo: save to db
tempDic = {}
tempArray = []

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
        tempArray.append(i)
        tempDic[i.title] = i

def search(w):
    if w in tempDic:
        return tempDic[w]

if __name__ == '__main__':
    import sys
    from colorama import init, Fore, Style
    init(autoreset=True)

    left = ''
    right = ''
    ran = True
    if len(sys.argv) >= 3:
        left = sys.argv[1]
        right = sys.argv[2]
    else:
        sys.exit(0)
    if len(sys.argv) >= 4 and sys.argv[3] == 'r':
        ran = False

    s = tempArray[tempArray.index(tempDic[left]) : tempArray.index(tempDic[right]) + 1]
    if ran:
        import random
        random.shuffle(s)
    print('========={}========='.format(len(s)))

    i = 0
    while True:
        if i >= len(s):
            break

        print(str(i) + '. ' + Fore.GREEN + s[i].title, end='')
        inin = input()
        if inin == 'q':
            break

        print('  ' + '\n  '.join(s[i].brief.splitlines()))

        inin = input()
        if inin == 'q':
            break
        if inin:
            print(Fore.YELLOW + ' ' + s[i].full)
            print()

        i += 1

