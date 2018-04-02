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

# todo: move to sep file
if __name__ == '__main__':
    import sys
    from colorama import init, Fore, Style
    init(autoreset=True)

    left = None
    right = None
    ran = True
    if len(sys.argv) >= 2:
        l, r = sys.argv[1].split(':')
        try:
            l = int(l)
        except:
            left = tempArray.index(tempDic[l])

        try:
            r = int(r)
        except:
            right = tempArray.index(tempDic[r])

        if not right:
            right = left + r
        if not left:
            left = right - r
    else:
        sys.exit(0)
    if len(sys.argv) >= 3 and sys.argv[2] == 'r':
        ran = False

    s = tempArray[left : right]
    if ran:
        import random
        random.shuffle(s)
    count = len(s)
    print('========= {} ========='.format(count))

    i = 0
    checked = []
    while True:
        if i >= len(s):
            if len(checked) > 0:
                s = checked
                if ran:
                    import random
                    random.shuffle(s)
                checked = []
                print('========= re0: {}/{} ========='.format(len(s), count))
                i = 0
            else:
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
            if s[i] not in checked:
                checked.append(s[i])
            print(Fore.YELLOW + ' ' + s[i].full)
            print()
            inin = input()

        i += 1

    print('\n'.join(checked))

