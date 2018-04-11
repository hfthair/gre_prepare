import attr
import os
import pickle

@attr.s
class Word(object):
    title = attr.ib()
    brief = attr.ib()
    full = attr.ib()
    position = attr.ib(default=0)

enable_pickle = False

# todo: save to db
wordByTitle = {}
wordByList = {}
wordArrayAll = []

if os.path.exists('gre3000/yaoniming3000.pickle') and enable_pickle:
    with open('gre3000/yaoniming3000.pickle', 'rb') as f:
        wordByTitle, wordArrayAll, wordByList = pickle.load(f)
else:
    def process(src):
        lines = src.splitlines()
        title, pron = lines[0].split('  ')
        def get_briefs(line):
            t = line.split('：')[0].strip()
            t = t[t.index(' '):].strip()
            return t

        brief = '\n'.join(get_briefs(i) for i in lines[1:] if i.startswith(' ♠'))
        return Word(title, brief, src)

    with open('gre3000/source_from_github.txt', encoding='utf8') as f:
        c = f.read()
        sp = (i.strip().replace('A: ', ' ') for i in c.split('Q:') if i.strip())
        tps = (process(i) for i in sp)
        for i in tps:
            wordArrayAll.append(i)
            if i.title in wordByTitle:
                print('!!!!! dupulicated in source --> ' + i.title)
            wordByTitle[i.title] = i

    if enable_pickle:
        import pandas as pd
        for i in range(1, 32):
            wordByList[i] = []
            sheet = pd.read_excel('gre3000/GRE3000.xlsx', 'L' + str(i), header=None)
            l = sheet[0].values.tolist()
            for w in l:
                if w not in wordByTitle:
                    print('missing ---> |{}| in list{}({})'.format(w, i, l.index(w)+1))
                    continue
                wordByTitle[w].position = i
                wordByList[i].append(wordByTitle[w])

        with open('gre3000/yaoniming3000.pickle', 'wb') as f:
            pickle.dump((wordByTitle, wordArrayAll, wordByList), f)

def search(w):
    if w in wordByTitle:
        return wordByTitle[w]

# todo: file structure
if __name__ == '__main__':

    import sys
    import random
    import time
    from colorama import init, Fore, Style
    from model import Word, save

    init(autoreset=True)

    def partial_match_print(c):
        m = (i for i in wordByTitle if c in i)
        ms = ((i + ' ' * 18, ' | '.join(wordByTitle[i].brief.splitlines())) for i in m)
        pr = [Fore.GREEN+a[:18]+Fore.RESET+b for a, b in ms]
        print('\n'.join(pr))

    def getList(i):
        temp = []
        import pandas as pd
        sheet = pd.read_excel('gre3000/GRE3000.xlsx', 'L' + str(i), header=None)
        l = sheet[0].values.tolist()
        print('L{} ---> {}'.format(i, len(l)))
        # temp = [wordByTitle[w] for w in l]
        for w in l:
            if w in wordByTitle:
                temp.append(wordByTitle[w])
            else:
                print('  ', l.index(w)+1, w)
        return temp

    def main(rang, args='', sel=0):
        rang = str(rang)
        s = None
        rand = False
        sav = False
        verify = False
        addition = False

        if 'r' in args:
            rand = True
        if 's' in args:
            sav = True
        if 'v' in args:
            verify = True
        if 'a' in args:
            addition = True

        if ':' in rang:
            l, r = rang.split(':')
            if l.startswith('list') and l[-1]>='0' and l[-1]<='9':
                # base on list id
                left = int(l.lower().replace('list', ''))
                right = int(r.lower().replace('list', ''))

                s = []
                for i in range(left, right+1):
                    s += getList(i)
            else:
                # word1:word2 or word1:number or number:word2
                left = None
                right = None
                try:
                    l = int(l)
                except:
                    left = wordArrayAll.index(wordByTitle[l])

                try:
                    r = int(r)
                except:
                    right = wordArrayAll.index(wordByTitle[r])

                if not right and not left:
                    left, right = l, r
                elif not right:
                    right = left + r
                elif not left:
                    left = right - r

                s = wordArrayAll[left:right]
        else:
            left = int(rang.lower().replace('list', ''))
            s = getList(left)

        if rand:
            random.shuffle(s)
            if sel and sel > 0:
                s = s[:sel+1]
            if addition:
                tt = (wordByTitle[w.title] for w in Word.ran(len(s)//20+5) if w.title in wordByTitle)
                s.extend(tt)
                random.shuffle(s)

        count = len(s)
        print('========= {} ========='.format(count))

        time_left = 15
        time_deadline = 60 * time_left + time.time()
        i = 0
        k = i
        words_unrecognize = []
        review_in_process = []
        while True:
            if i >= len(s):
                if len(words_unrecognize) > 0:
                    s = words_unrecognize
                    if rand:
                        random.shuffle(s)
                    words_unrecognize = []
                    print('========= re0: {}/{} ========='.format(len(s), count))
                    i = 0
                else:
                    break

            if i - k >= 26:
                t = words_unrecognize[:]
                pick = len(t)//5+5
                k = i
                random.shuffle(t)
                review_in_process = t[:pick]

            w = s[i]
            if len(review_in_process) > 0:
                w = review_in_process[-1]
                review_in_process = review_in_process[:-1]
            else:
                i += 1
            print(str(i) + '. ' + Fore.GREEN + w.title, end='')
            inin = input()
            if inin == 'q':
                break
            if inin == 'b' and i > 0:
                i -= 2
                continue

            print('  ' + '\n  '.join(w.brief.splitlines()))

            inin = input()
            if inin == 'q':
                break
            if inin.startswith('*'):
                partial_match_print(inin.replace('*', ''))
                continue
            if inin:
                if w not in words_unrecognize:
                    words_unrecognize.append(w)
                print(Fore.YELLOW + ' ' + w.full)
                print()
                if sav:
                    save(Word, w.title, w.brief, w.full)
                inin = input(':' if verify else '')
                while verify and inin != w.title and inin != "'":
                    inin = input(':')
            time_tmp = int(time_deadline - time.time())//60
            if time_left != time_tmp:
                time_left = time_tmp
                time_warning = '    ||| {} minutes left.'.format(time_left)
                if time_left > 0:
                    print(Fore.YELLOW + time_warning)
                else:
                    print(Fore.RED + time_warning)

        print('\n'.join(i.title for i in words_unrecognize))

    def test(idx):
        s = getList(idx)
        random.shuffle(s)
        i = 0
        while True:
            x = s[i:i+10]
            if not x:
                break
            x = [(j.title + ' ' * 18, ' | '.join(j.brief.splitlines())) for j in x]
            x = [Fore.GREEN+a[:18]+Fore.RESET+b for a, b in x]
            print('\n'.join(x))
            inin = input()
            if inin == 'q':
                break
            i += 10

    import fire
    fire.Fire(main)

