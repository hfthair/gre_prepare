from yaoniming3000 import wordByTitle
from iciba import suggests
from colorama import init, Fore, Style

init(autoreset=True)

def partial_match_print(c):
    m = (i for i in wordByTitle if c in i)
    ms = ((i + ' ' * 18, \
            ' | '.join(wordByTitle[i].brief.splitlines()), \
            wordByTitle[i].position) for i in m)
    pr = [Fore.GREEN+a[:18]+Fore.YELLOW+'({}) '.format(c)+Fore.RESET+b for a, b, c in ms]
    print('\n'.join(pr))


while True:
    inin = input('>>> ')
    if inin == 'q':
        break
    if inin.strip():
        partial_match_print(inin.strip())
        print('==========')
        try:
            m = suggests(inin.strip(), 5)
            ms = ((i + ' ' * 18, ' | '.join(m[i].splitlines())) for i in m)
            pr = [Fore.GREEN+a[:18]+Fore.RESET+b[:55] for a, b in ms]
            print('\n'.join(pr))
        except:
            import traceback
            traceback.print_exc()
            print('net fail!')
            pass