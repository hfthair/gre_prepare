import datetime
import init_path
from peewee import fn
from colorama import init, Fore, Style
from book_v3000 import book
from book_v3000.model import Word

init()

def get_data_of_day(fr, to):
    # frr = datetime.datetime.combine(fr, datetime.time.min)
    # too = datetime.datetime.combine(fr, datetime.time.max)
    return Word.select().where(~Word.last_modify.is_null()).\
        where(Word.last_modify.year>=fr.year).\
        where(Word.last_modify.month>=fr.month).\
        where(Word.last_modify.day>=to.day).\
        where(Word.last_modify.year<=to.year).\
        where(Word.last_modify.month<=to.month).\
        where(Word.last_modify.day<=to.day)

def printw(w, cnt):
    t = w.title + ' ' * 15
    t = '({}) '.format(cnt) + t[:15]
    print(Fore.GREEN + t + Fore.RESET + ' | '.join(w.brief.splitlines()), end='')

def print_ws(ws, touch):
    cnt = 0
    for w in ws:
        cnt += 1

        printw(book.byTitle[w.title], cnt)
        q = input()
        if touch:
            w.touch()
        if q == 'q':
            break

def task_for_today():
    ws = get_data_of_day(datetime.date.today(), datetime.date.today())

    if ws.count() > 30:
        print('==== review today ({}) ===='.format(ws.count()))
        ws = ws.order_by(fn.random())
        print_ws(ws, False)
    else:
        print('==== new today ====')
        ws = Word.select().where(Word.last_modify.is_null()).\
            order_by(Word.lid, Word.count.desc()).\
            limit(80)
        print_ws(ws, True)

def task_for_review():
    cr = (1, 2, 3, 5)
    cr = [datetime.datetime.now().date()-datetime.timedelta(days=i) for i in cr]
    cr = [i.year*10000+i.month*100+i.day for i in cr]

    # how does peewee support |(col1, col2) << ((a,b), (c,d))| ?
    ws = Word.select().\
            where(~Word.last_modify.is_null()). \
            where((Word.last_modify.year*10000+Word.last_modify.month*100+Word.last_modify.day) << cr).\
            order_by(Word.last_modify.desc(), fn.random())

    print_ws(ws, False)

import fire
fire.Fire({'today': task_for_today, 'review': task_for_review})
