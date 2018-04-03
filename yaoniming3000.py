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
        if i.title in tempDic:
            print('!!!!! dupulicated in source --> ' + i.title)
        tempDic[i.title] = i


def search(w):
    if w in tempDic:
        return tempDic[w]

# todo: move to sep file
if __name__ == '__main__':

    import sys
    import random
    from colorama import init, Fore, Style
    init(autoreset=True)

    s = None
    ran = False
    sv = False

    if len(sys.argv) >= 2:
        if ':' in sys.argv[1]:
            left = None
            right = None
            l, r = sys.argv[1].split(':')
            try:
                l = int(l)
            except:
                left = tempArray.index(tempDic[l])

            try:
                r = int(r)
            except:
                right = tempArray.index(tempDic[r])

            if not right and not left:
                left, right = l, r
            elif not right:
                right = left + r
            elif not left:
                left = right - r

            s = tempArray[left:right]
        else:
            l = sys.argv[1].lower().replace('list', '')
            int(l)
            temp = []
            import pandas as pd
            sheet = pd.read_excel('gre3000/GRE3000.xlsx', 'L' + l, header=None)
            l = sheet[0].values.tolist()
            print('L ---> {}'.format(len(l)))
            # temp = [tempDic[i] for i in l if i in tempDic]
            for i in l:
                if i in tempDic:
                    temp.append(tempDic[i])
                else:
                    print(i)
            s = temp
    else:
        sys.exit(0)
    if len(sys.argv) >= 3:
        if 'r' in sys.argv[2]:
            ran = True
        if 's' in sys.argv[2]:
            sv = True

    if ran:
        random.shuffle(s)
    count = len(s)
    print('========= {} ========='.format(count))

    i = 0
    k = i
    checked = []
    while True:
        if i >= len(s):
            if len(checked) > 0:
                s = checked
                if ran:
                    random.shuffle(s)
                checked = []
                print('========= re0: {}/{} ========='.format(len(s), count))
                i = 0
            else:
                break

        if i - k >= 26:
            k = i
            t = checked[:]
            random.shuffle(t)
            s[i:i] = t[:len(t)//2+2]

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
            if sv:
                from model import Word, save
                save(Word, s[i].title, s[i].brief, s[i].full)
            inin = input()

        i += 1

    print('\n'.join(i.title for i in checked))

