import tkinter
import datetime
import init_path
from tkinter import ttk
from tkinter.font import Font
from peewee import fn
from dictionary.iciba import search as search_iciba
from book_v3000.book import search as bookv3000
from dictionary.model import Word, save

def search(w):
    finds = Word.select().where(Word.title == w)
    if finds:
        find = finds[0]
        return find.pron, find.brief, find.full
    else:
        return search_iciba(w)

class Window:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('500x345')

        self.entry = tkinter.Entry(self.root, width=48)
        self.entry.grid(row=0, column=1, columnspan=3, pady=8, padx=8)

        self.btn = tkinter.Button(self.root, text='GO', width=8, command=self.on_enter)
        self.btn.grid(row=0, column=4, pady=8)

        self.detail = tkinter.Text(self.root, height=21, width=66, relief='sunken')
        self.detail.config(state=tkinter.DISABLED)
        self.detail.tag_configure('title', font=('Arial', 12, 'bold'), spacing1=9)
        self.detail.tag_configure('pron', foreground='green', spacing1=5)
        # ft = Font(size=11)
        self.detail.tag_configure('brief', foreground='darkgreen', spacing1=9)
        self.detail.tag_configure('error', foreground='red', spacing1=3)
        self.detail.tag_configure('detail', foreground='black', spacing1=3)
        self.detail.grid(row=1, column=0, columnspan=5, pady=1, padx=15)

        self.entry.focus_set()
        self.entry.bind('<Return>', self.on_enter)
        self.entry.bind('<Up>', self.on_key_up_down)
        self.entry.bind('<Down>', self.on_key_up_down)

        self.cache = []
        self.cache_iter = None

    def on_key_up_down(self, e):
        if self.cache_iter is None:
            self.cache_iter = len(self.cache)
            if len(self.cache) > 0 and self.entry.get() == self.cache[-1]:
                self.cache_iter -= 1

        w = None
        if e.keysym == 'Up':
            self.cache_iter -= 1
            if self.cache_iter >= 0:
                w = self.cache[self.cache_iter]
            else:
                self.cache_iter = 0
        elif e.keysym == 'Down':
            self.cache_iter += 1
            if self.cache_iter > len(self.cache):
                self.cache_iter = len(self.cache)
            if self.cache_iter < len(self.cache):
                w = self.cache[self.cache_iter]
        if w:
            self.entry.delete(0, tkinter.END)
            self.entry.insert(tkinter.END, w)

    def on_enter(self, e=None):
        w = self.entry.get()
        w = w.strip()
        self.detail.config(state=tkinter.NORMAL)
        self.detail.delete(1.0, tkinter.END)

        try:
            pron, brief, detail = search(w)

            self.detail.insert(tkinter.END, w + '\n', 'title')
            self.detail.insert(tkinter.END, pron + '\n\n', 'pron')
            self.detail.insert(tkinter.END, brief + '\n\n', 'brief')
            self.detail.insert(tkinter.END, '---------------\n', 'detail')
            self.detail.insert(tkinter.END, detail + '\n', 'detail')

            self.entry.delete(0, tkinter.END)

            save(w, pron, brief, detail)
        except Exception as e:
            self.detail.insert(tkinter.END, str(e), 'error')

        self.detail.config(state=tkinter.DISABLED)

        self.cache.append(w)
        self.cache_iter = None


    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    window = Window()
    window.mainloop()
