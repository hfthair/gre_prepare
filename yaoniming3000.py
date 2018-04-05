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

# todo: file structure
if __name__ == '__main__':

    import sys
    import random
    from colorama import init, Fore, Style

    init(autoreset=True)

    def getList(i):
        temp = []
        import pandas as pd
        sheet = pd.read_excel('gre3000/GRE3000.xlsx', 'L' + str(i), header=None)
        l = sheet[0].values.tolist()
        print('L ---> {}'.format(len(l)))
        # temp = [tempDic[w] for w in l]
        for w in l:
            if w in tempDic:
                temp.append(tempDic[w])
            else:
                print(w)
        return temp

    def main(rang, args='', sel=0):
        rang = str(rang)
        s = None
        rand = False
        sav = False
        verify = False

        if 'r' in args:
            rand = True
        if 's' in args:
            sav = True
        if 'v' in args:
            verify = True

        if ':' in rang:
            l, r = rang.split(':')
            if l.startswith('list') and l[-1]>='0' and l[-1]<='9':
                # base on list id
                left = int(l.lower().replace('list', ''))
                right = int(r.lower().replace('list', ''))

                s = []
                for i in range(left, right):
                    s += getList(i)
            else:
                # word1:word2 or word1:number or number:word2
                left = None
                right = None
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
            left = int(rang.lower().replace('list', ''))
            s = getList(left)

        if rand:
            random.shuffle(s)
            if sel and sel > 0:
                s = s[:sel+1]
        count = len(s)
        print('========= {} ========='.format(count))

        i = 0
        k = i
        checked = []
        while True:
            if i >= len(s):
                if len(checked) > 0:
                    s = checked
                    if rand:
                        random.shuffle(s)
                    checked = []
                    print('========= re0: {}/{} ========='.format(len(s), count))
                    i = 0
                else:
                    break

            if i - k >= 26:
                t = checked[:]
                pick = len(t)//5+12
                k = i + pick
                random.shuffle(t)
                s[i:i] = t[:pick]

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
                if sav:
                    from model import Word, save
                    save(Word, s[i].title, s[i].brief, s[i].full)
                inin = input(':' if verify else '')
                while verify and inin != s[i].title:
                    inin = input(':')

            i += 1

        print('\n'.join(i.title for i in checked))

    import fire
    fire.Fire(main)

