#encoding=utf-8
import sys
from iciba import search
from model import Read, Word
from colorama import init, Fore, Style
from peewee import fn
from fill_gre3000.fill_to_db import gre3000

def save(T, title, brief, detail):
    finds = T.select().where(T.title == title)
    if finds:
        find = finds[0]
        find.count = find.count + 1

        # todo: rm this
        # fix i
        ret = gre3000(title)
        if ret and ret[2] != find.brief:
            find.brief = ret[2]
            find.iciba = ret[3]
            find.save()

        find.save()
    else:
        find = T(title=title, brief=brief, iciba=detail, merriam='')
        find.save()

cache = {}
def cache_add(w, d):
    cache[w] = ' | '.join(d.splitlines())

def cache_show(withcn):
    if withcn:
        for x in cache:
            t = x + ' ' * 18
            t = t[:18]
            print(Fore.GREEN + t + Fore.RESET + cache[x])
    else:
        for x in cache:
            print(Fore.GREEN + x)

def random_show(T, limit, withcn):
    if not random_show.res or not  withcn:
        random_show.res = T.select().order_by((fn.random()*T.count).desc()).limit(limit)
    if withcn:
        for i in random_show.res:
            t = i.title + ' ' * 18
            t = t[:18]
            # todo: rm this
            # fix i
            ret = gre3000(i.title)
            if ret and ret[2] != i.brief:
                i.brief = ret[2]
                i.iciba = ret[3]
                i.save()

            print(Fore.GREEN + t + Fore.RESET +
                ' | '.join(i.brief.splitlines()))


    else:
        for i in random_show.res:
            print(Fore.GREEN + i.title)
random_show.res = None

def main():
    T = Read
    header = '>>> '
    if len(sys.argv) > 1 and sys.argv[1] == 'word':
        T = Word
        header = '$$$ '

    init(autoreset=True)

    while True:
        w = input(header)
        w = ''.join(x for x in w if x.lower()>='a' and x.lower()<='z' or x in ' -')
        if not w:
            print('q to quit')
            continue

        if len(w) < 3:
            if w == 'q':
                break
            elif w == 'l':
                cache_show(False)
            elif w == 'll':
                cache_show(True)
            elif w == 'r':
                random_show(T, 10, False)
            elif w == 'rr':
                random_show(T, 10, True)
            continue
        elif w.startswith('-'):
            # if w.startswith('-r'):
            #     try:
            #         random_show(T, int(w[2:]), False)
            #     except:
            #         pass
            continue

        print(Fore.GREEN + ' ' + w)
        print('===============' * 4)
        try:
            brief = None
            detail = None
            ret = gre3000(w)
            if ret:
                _, p, brief, detail = ret
            else:
                brief, detail = search(w)

            print(Fore.GREEN + brief)
            print('===============' * 4)
            print(Fore.YELLOW + detail)

            cache_add(w, brief)

            save(T, w, brief, detail)

        except Exception as e:
            print(Fore.RED + str(e))
        print('===============' * 4)
        print('')

if __name__ == '__main__':
    main()



