from colorama import Fore, Style, init

from book_v3000 import book
from dictionary.iciba import suggests

init(autoreset=True)


def partial_match_print(c):
    m = (i for i in book.byTitle if c in i)
    ms = ((i + ' ' * 18,
           ' | '.join(book.byTitle[i].brief.splitlines()),
           book.byTitle[i].position) for i in m)
    pr = [Fore.GREEN+a[:18]+Fore.YELLOW +
          '({}) '.format(c)+Fore.RESET+b for a, b, c in ms]
    print('\n'.join(pr))


print("{}Search words which contain what you type.".format(Fore.BLUE))
print("{}<ENTER> search; <q> quit.\n".format(Fore.BLUE))
while True:
    inin = input('>>> ')
    if inin == 'q':
        break
    if inin.strip():
        print("{}Source book3000:".format(Fore.BLUE))
        partial_match_print(inin.strip())
        try:
            print("{}Source internet:".format(Fore.BLUE))
            m = suggests(inin.strip(), 5)
            ms = ((i + ' ' * 18, ' | '.join(m[i].splitlines())) for i in m)
            pr = [Fore.GREEN+a[:18]+Fore.RESET+b[:55] for a, b in ms]
            print('\n'.join(pr))
        except:
            print('net fail!')
            pass
