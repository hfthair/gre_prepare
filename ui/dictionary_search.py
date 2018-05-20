import tkinter
import datetime
import init_path
from tkinter import ttk
from peewee import fn
from dictionary.iciba import search as search_iciba
from book_v3000.book import search as bookv3000
from dictionary.model import Word

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

        self.btn = tkinter.Button(self.root, text='GO', width=8, command=None)
        self.btn.grid(row=0, column=4, pady=8)

        self.detail = tkinter.Text(self.root, height=21, width=66, relief='sunken')
        self.detail.config(state=tkinter.DISABLED)
        self.detail.tag_configure('title', font=('bold',))
        self.detail.tag_configure('pron', foreground='lightgreen')
        self.detail.tag_configure('brief', foreground='green')
        self.detail.tag_configure('error', foreground='red')
        self.detail.grid(row=1, column=0, columnspan=5, pady=1, padx=15)

        self.entry.focus_set()
        self.entry.bind('<Return>', self.on_enter)

    def on_enter(self, e):
        w = self.entry.get()
        self.detail.config(state=tkinter.NORMAL)
        self.detail.delete(1.0, tkinter.END)

        try:
            pron, brief, detail = search(w)

            self.detail.insert(tkinter.END, w + '\n', 'title')
            self.detail.insert(tkinter.END, pron + '\n', 'pron')
            self.detail.insert(tkinter.END, brief + '\n\n', 'brief')
            self.detail.insert(tkinter.END, detail + '\n')
        except Exception as e:
            self.detail.insert(tkinter.END, str(e), 'error')

        self.detail.config(state=tkinter.DISABLED)


    def mainloop(self):
        self.root.mainloop()

if __name__ == '__main__':
    window = Window()
    window.mainloop()
