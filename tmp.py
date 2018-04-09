from yaoniming3000 import tempDic
from colorama import init, Fore, Style

init(autoreset=True)

def partial_match_print(c):
    m = (i for i in tempDic if c in i)
    ms = ((i + ' ' * 18, ' | '.join(tempDic[i].brief.splitlines())) for i in m)
    pr = [Fore.GREEN+a[:18]+Fore.RESET+b for a, b in ms]
    print('\n'.join(pr))


while True:
    inin = input('>>> ')
    if inin == 'q':
        break
    if inin.strip():
        partial_match_print(inin.strip())