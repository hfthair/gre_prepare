#encoding=utf-8
import sys
from iciba import search as search_iciba
from model2 import Word, save
from colorama import init, Fore, Style
from peewee import fn
from yaoniming3000 import search as gre3000

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

def random_show(limit, withcn):
    if not random_show.res or not withcn:
        random_show.res = Word.ran(limit)
    if withcn:
        for i in random_show.res:
            t = i.title + ' ' * 18
            t = t[:18]
            print(Fore.GREEN + t + Fore.RESET +
                ' | '.join(i.brief.splitlines()))
    else:
        for i in random_show.res:
            print(Fore.GREEN + i.title)
random_show.res = None

def search(w):
    finds = Word.select().where(Word.title == w)
    if finds:
        find = finds[0]
        return find.pron, find.brief, find.full
    else:
        return search_iciba(w)

def main():
    init(autoreset=True)

    while True:
        w = input('>>> ')
        w = ''.join(x for x in w if x.lower()>='a' and x.lower()<='z' or x in ' -')
        if not w:
            continue

        if len(w) < 3:
            if w == 'q':
                break
            elif w == 'l':
                cache_show(False)
            elif w == 'll':
                cache_show(True)
            elif w == 'r':
                random_show(10, False)
            elif w == 'rr':
                random_show(10, True)
            continue

        try:
            print(Fore.GREEN + '\n ' + w, end='')
            pron, brief, detail = search(w)
            print(pron)

            print('===============' * 4)
            print(Fore.GREEN + brief)
            print('===============' * 4)
            print(Fore.YELLOW + detail)

            cache_add(w, brief)

            save(w, pron, brief, detail)

        except Exception as e:
            print('')
            print('===============' * 4)
            print(Fore.RED + str(e))
        print('===============' * 4)

        ret = gre3000(w)
        if ret:
            _, g3 = ret.brief, ret.full
            print(Fore.RED + g3)
            print('===============' * 4)

        print('')

if __name__ == '__main__':
    main()



