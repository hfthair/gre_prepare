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

def task_from_prehistory():
    print('==== from prehistory ====')
    ws = Word.select().where(Word.last_modify.is_null()).\
        order_by(((Word.count-0.8) * Word.id).desc(), Word.id.desc()).\
        limit(65)
    return ws

def task_for_review(day):
    ws = get_data_of_day(day, day)
    if not ws or ws.count() <= 0:
        return task_for_review(day-datetime.timedelta(days=1))

    return day, ws


class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('860x580')

        tips = '''keyboard control: { (-> <- ^ v): direction, (space): mark }'''
        tkinter.Label(self.root, text=tips).grid(row=1, column=0, columnspan=3, padx=5, sticky=tkinter.W)

        self.btn_l = tkinter.Button(self.root, text='<-', width=8, command=self.show_prev_day)
        self.btn_r = tkinter.Button(self.root, text='->', width=8, command=self.show_next_day)
        self.btn_z = tkinter.Button(self.root, text='-z-', width=8, command=self.show_prehistory)
        self.btn_l.grid(row=1, column=4, pady=8)
        self.btn_r.grid(row=1, column=5, pady=8)
        self.btn_z.grid(row=1, column=6, pady=8)

        self.detail = tkinter.Text(self.root, height=38, width=46, relief='sunken')
        self.detail.config(state=tkinter.DISABLED)
        self.detail.grid(row=0, column=4, columnspan=3, pady=16, padx=3, sticky=tkinter.W)

        ttk.Style().configure('Treeview', rowheight=26)
        self.tv = ttk.Treeview(self.root, columns=('brief'), height=18)
        self.tv.heading('#0', text='title')
        self.tv.heading('#1', text='brief')
        self.tv.column('#0', width=100, minwidth=80)
        self.tv.column('#1', width=400, minwidth=200)
        self.tv.grid(row=0, column=0, columnspan=3, pady=16, padx=5)

        self.tv.tag_configure('mark', background='orange')

        self.root.bind('<Key>', self.on_press)
        self.tv.bind('<<TreeviewSelect>>', self.on_select)

        self.cur = None
        self.stack = []
        self.marks = set()

    def __next(self):
        d = None
        if not self.cur:
            d = datetime.datetime.now().date()
        else:
            d = self.cur-datetime.timedelta(days=1)
        r = task_for_review(d)
        if r:
            self.cur, _ = r
            self.stack.append(self.cur)
        return r

    def __prev(self):
        if len(self.stack) < 2:
            return
        last = self.stack[-2]
        r = task_for_review(last)
        if r and r[0] == last:
            self.cur, _ = r
            self.stack = self.stack[:-1]
            return r
        else:
            print('last retrive error {} || {}'.format(r[0], last))
            return

    def restore_marks(self):
        for i in self.tv.get_children():
            if self.tv.item(i, 'text') in self.marks:
                self.tv.item(i, tags=('mark', ))

    def update(self, d, ws, touch=False):
        self.tv.delete(*self.tv.get_children())
        self.root.title(str(d))
        first = None
        for w in ws:
            br = ' | '.join(w.brief.splitlines())
            i = self.tv.insert('', 'end', text=w.title, values=(br,))
            if touch:
                w.touch()
            if not first and i:
                first = i
        self.restore_marks()
        self.tv.focus_set()
        self.tv.selection_set((first, ))
        self.tv.focus(first)

    def show_next_day(self):
        r = self.__next()
        if r:
            d, ws = r
            self.update(d, ws)
        else:
            print('no next')

    def show_prev_day(self):
        r = self.__prev()
        if r:
            d, ws = r
            self.update(d, ws)
        else:
            print('no prev')

    def show_prehistory(self):
        r = task_from_prehistory()
        if r:
            d = datetime.datetime.now().date()
            self.cur = d
            self.update(d, r, True)
        else:
            print('no prehistory items')

    def update_detail(self):
        sels = self.tv.selection()
        if sels:
            text = self.tv.item(sels[0], 'text')
            ws = Word.select().where(Word.title==text)
            if ws:
                w = ws[0]
                detail = w.full
                if not detail:
                    detail = w.brief
                # self.detail['text'] = detail
                self.detail.config(state=tkinter.NORMAL)
                self.detail.delete(1.0, tkinter.END)
                self.detail.insert(tkinter.END, detail)
                self.detail.config(state=tkinter.DISABLED)

    def mark(self):
        sels = self.tv.selection()
        if sels:
            iid = sels[0]
            text = self.tv.item(iid, 'text')
            if self.tv.tag_has('mark', iid):
                self.marks.remove(text)
                self.tv.item(iid, tags=())
            else:
                self.tv.item(iid, tags=('mark', ))
                self.marks.add(text)

    def on_press(self, e):
        key = e.keysym
        m = {
            'Right': self.show_next_day,
            'Left': self.show_prev_day,
            'space': self.mark
        }

        if key in m:
            m[key]()

    def on_select(self, e):
        self.update_detail()

    def mainloop(self):
        self.show_next_day()
        self.root.mainloop()

if __name__ == '__main__':
    window = Window()
    window.mainloop()

    print('\n'.join(window.marks))