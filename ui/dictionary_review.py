import tkinter
import datetime
import init_path
from tkinter import ttk
from peewee import fn
from dictionary.model import Word

def get_data_of_day(fr, to):
    return Word.select().\
        where(~Word.last_modify.is_null()).\
        where(Word.last_modify.year>=fr.year).\
        where(Word.last_modify.month>=fr.month).\
        where(Word.last_modify.day>=to.day).\
        where(Word.last_modify.year<=to.year).\
        where(Word.last_modify.month<=to.month).\
        where(Word.last_modify.day<=to.day)

def task_for_today():
    ws = get_data_of_day(datetime.date.today(), datetime.date.today())

    if ws.count() > 30:
        print('==== review today ({}) ===='.format(ws.count()))
        ws = ws.order_by(fn.random())
        return ws
    else:
        print('==== new today ====')
        ws = Word.select().where(Word.last_modify.is_null()).\
            order_by(((Word.count-0.8) * Word.id).desc(), Word.id.desc()).\
            limit(65)
        return ws

def task_for_review():
    cr = (1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 15)
    cr = [datetime.datetime.now().date()-datetime.timedelta(days=i) for i in cr]
    cr = [i.year*10000+i.month*100+i.day for i in cr]

    # how does peewee support |(col1, col2) << ((a,b), (c,d))| ?
    ws = Word.select().\
            where(~Word.last_modify.is_null()). \
            where((Word.last_modify.year*10000+Word.last_modify.month*100+Word.last_modify.day) << cr).\
            order_by(Word.last_modify.desc(), fn.random())

    return ws


root = tkinter.Tk()

ttk.Style().configure('Treeview', rowheight=36)
tv = ttk.Treeview(root, columns=('brief'))
tv.heading('#0', text='title')
tv.heading('#1', text='brief')

w_to_show = task_for_review()
it = iter(w_to_show)


def __add(w):
    br = ' | '.join(w.brief.splitlines())
    item = tv.insert('', 'end', text=w.title, values=(br,))
    if item:
        tv.selection_set(item)
    return item

def add():
    try:
        w = it.next()
        n = __add(w)
        return n
    except:
        print('exception when add.')
        pass

c = 5
while c > 0:
    n = add()
    if not n:
        break
    c -= 1

def on_press(e):
    key = e.keysym
    if key == 'Return':
        n = add()
        if not n:
            print('nothing')
        tv.yview_moveto(1)

root.bind('<KeyPress>', on_press)

tv.pack()
root.mainloop()
