import random
import sys
import time

import fire
from colorama import Fore, Style, init

from book_v3000 import book
from book_v3000.model import Word
from util.tools import iinput

init(autoreset=True)


def getList(i):
    temp = book.byList[i]
    return temp


def main(start, to=None, rand=False, select=0, iwilltype=False, iwantsurprise=False, simple=False):
    s = None

    start = int(start)
    if not to:
        to = start

    print(Fore.BLUE +
          "Start learn list ({}) to ({}),{} try finish in 15 minutes.".format(start, to, Fore.RED))
    print(Fore.BLUE + "Press <q> to quit...\n")

    s = []
    for i in range(start, to+1):
        s += getList(i)

    if rand:
        random.shuffle(s)
        if select and select > 0:
            s = s[:select]
        if iwantsurprise:
            tt = (book.byTitle[w.title] for w in Word.ran(
                len(s)//20+5) if w.title in book.byTitle)
            s.extend(tt)
            random.shuffle(s)

    print(Fore.BLUE + '========= {} words ========='.format(len(s)))

    count = len(s)
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
                if rand:
                    random.shuffle(s)
                words_unrecognize = []
                print(Fore.BLUE +
                      '========= Review {}/{} ========='.format(len(s), count))
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
        if simple:
            def gen_line(a, b):
                t = (a + ' ' * 13)[:13]
                return Fore.GREEN + t + Fore.RESET + ' | '.join(b.splitlines())
            print(gen_line(w.title, w.brief), end='')
            inin = iinput("  {}<ENTER>{}".format(
                Fore.BLUE, Fore.RESET))
            if inin == 'q':
                break
        else:
            print(str(i) + '. ' + Fore.GREEN + w.title +
                  Fore.RESET + '    ({})'.format(w.position), end='')

            inin = iinput("  {}<ENTER>{}".format(
                Fore.BLUE, Fore.RESET))
            if inin == 'q':
                break

            for m in w.means:
                print('  ' + m.cn)
                if m.synonym:
                    print('   ' + m.synonym)

            inin = iinput("  {}<ENTER> I know; <d> detail; <b> go back; <q> quit{}".format(
                Fore.BLUE, Fore.RESET))
            if inin == 'q':
                break
            if inin == 'b' and i > 1:
                i -= 2
                continue
            if inin != '\r':
                if w not in words_unrecognize:
                    words_unrecognize.append(w)
                print(Fore.YELLOW + ' ' + w.full + Fore.BLUE +
                      "\n  * We will review it later.\n")
                Word.increase(w.title)
                while iwilltype and inin != w.title and inin != "q":
                    inin = input('<i will type>:' if iwilltype else '')
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

    print(Fore.BLUE + " ({}) ".format(len(word_all)),
          ' | '.join(i.title for i in word_all))


if __name__ == '__main__':
    fire.Fire(main)
