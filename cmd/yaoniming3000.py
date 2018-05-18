import os
import pickle
from yaoniming3000_word import Word, create_word

# todo: save to db
wordByTitle = {}
wordByList = {}
wordArrayAll = []

if os.path.exists('gre3000/yaoniming3000.pickle'):
    with open('gre3000/yaoniming3000.pickle', 'rb') as f:
        wordByTitle, wordArrayAll, wordByList = pickle.load(f)
else:
    with open('gre3000/source_from_github.txt', encoding='utf8') as f:
        c = f.read()
        sp = (i.strip().replace('A: ', ' ') for i in c.split('Q:') if i.strip())
        tps = (create_word(i) for i in sp)
        for i in tps:
            wordArrayAll.append(i)
            if i.title in wordByTitle:
                print('!!!!! dupulicated in source --> ' + i.title)
            wordByTitle[i.title] = i

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

    for i in wordArrayAll:
        if i.position == 0:
            wordByList[31].append(i)

    with open('gre3000/yaoniming3000.pickle', 'wb') as f:
        pickle.dump((wordByTitle, wordArrayAll, wordByList), f)

def search(w):
    if w in wordByTitle:
        return wordByTitle[w]


def synonym_in_3000(w):
    res = []
    for m in w.means:
        s = m.synonym
        s = ''.join(i for i in s if ord(i) < 128)
        s = s.replace(',', ' ')
        l = [i.strip() for i in s.split(' ') if i.strip()]
        res.extend(l)
    res = set(res)
    res = [i for i in res if i in wordByTitle]
    return res


if __name__ == '__main__':
    import sys
    import random
    import time
    from colorama import init, Fore, Style
    from model1 import Word

    init(autoreset=True)

    def partial_match_print(c):
        m = (i for i in wordByTitle if c in i)
        ms = ((i + ' ' * 18, ' | '.join(wordByTitle[i].brief.splitlines())) for i in m)
        pr = [Fore.GREEN+a[:18]+Fore.RESET+b for a, b in ms]
        print('\n'.join(pr))

    def getList(i):
        temp = wordByList[i]
        return temp

    def main(rang, args='', sel=0):
        rang = str(rang)
        s = None
        arg_rand_order = False
        arg_save_res = False
        arg_verify_input = False
        arg_addition_words = False
        arg_show_eg = False
        arg_inline = False

        if 'r' in args:
            arg_rand_order = True
        if 's' in args:
            arg_save_res = True
        if 'v' in args:
            arg_verify_input = True
        if 'a' in args:
            arg_addition_words = True
        if 'e' in args:
            arg_show_eg = True
        if 'l' in args:
            arg_inline = True

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

        if arg_rand_order:
            random.shuffle(s)
            if sel and sel > 0:
                s = s[:sel]
            if arg_addition_words:
                tt = (wordByTitle[w.title] for w in Word.ran(len(s)//20+5) if w.title in wordByTitle)
                s.extend(tt)
                random.shuffle(s)

        count = len(s)
        print('========= {} ========='.format(count))

        time_left = 15
        time_deadline = 60 * time_left + time.time()
        i = 0
        k = i
        word_all = []
        words_unrecognize = []
        review_in_process = []
        while True:
            if i >= len(s):
                if len(words_unrecognize) > 0:
                    s = words_unrecognize
                    if arg_rand_order:
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

            word_all.append(w)
            if arg_inline:
                def gen_line(a, b):
                    t = a + ' ' * 13
                    t = t[:13]
                    return Fore.GREEN + t + Fore.RESET + ' | '.join(b.splitlines())
                print(gen_line(w.title, w.brief), end='')
                inin = input()
                if inin == 'q':
                    break
            else:
                question = w.title
                if arg_show_eg:
                    pass
                    # egs = '\n'.join(mean.eg for mean in w.means)
                    # question = ''.join(c if ord(c)<128 else '\n' for c in egs)
                    # question = '\n'.join(q for q in question.splitlines() if q and len(q)>6)
                    # question = question.replace(w.title, Fore.RED + w.title + Fore.GREEN)
                    # question = '\n' + question + '\n'

                print(str(i) + '. ' + Fore.GREEN + question +
                        Fore.RESET + '    ({})'.format(w.position), end='')

                inin = input()
                if inin == 'q':
                    break
                if inin == 'b' and i > 0:
                    i -= 2
                    continue

                # print('  ' + '\n  '.join(w.brief.splitlines()))
                for m in w.means:
                    print('  ' + m.cn)
                    if m.synonym:
                        print('   ' + m.synonym)

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
                    if arg_save_res:
                        Word.increase(w.title)
                    inin = input(':' if arg_verify_input else '')
                    while arg_verify_input and inin != w.title and inin != "'":
                        inin = input(':')
                else:
                    Word.descrease(w.title)

                time_tmp = int(time_deadline - time.time())//60
                if time_left != time_tmp:
                    time_left = time_tmp
                    time_warning = '    ||| {} minutes left.'.format(time_left)
                    if time_left > 0:
                        print(Fore.YELLOW + time_warning)
                    else:
                        print(Fore.RED + time_warning)

        print('\n'.join(i.title for i in word_all))

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

