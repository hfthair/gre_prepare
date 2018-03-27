#encoding=utf-8
from iciba import search
from model import Read, Word

if __name__ == '__main__':
    from colorama import init, Fore, Style
    init(autoreset=True)

    val = False
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'word':
        val = True

    cache = {}
    while True:
        w = input('>>> ' if not val else '$$$ ')
        w = ''.join(x for x in w if x.lower()>='a' and x.lower()<='z' or x in ' -')
        if not w:
            print('q to quit')
            continue

        if w == 'q':
            break
        elif w == 'p':
            for x in cache:
                print(Fore.GREEN + x)
            continue
        elif w == 'r':
            for x in cache:
                print(Fore.GREEN + x + Fore.RESET + '\t' + cache[x])
            continue

        print(Fore.YELLOW + ' ' + w)
        print('===============' * 4)
        try:
            brief, detail = search(w)
            meaning = detail if detail else brief
            print(Fore.YELLOW + meaning)
            cache[w] = '|'.join(brief.splitlines())
            T = Read
            if val:
                T = Word
            d = T.select().where(T.title == w)
            if d:
                d[0].count = d[0].count + 1
                d[0].save()
            else:
                ww = T(title=w, brief=brief, iciba=detail, merriam='')
                ww.save()

        except Exception as e:
            print(Fore.RED + str(e))
        print('===============' * 4)
        print('')



