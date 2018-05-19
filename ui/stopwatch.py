import tkinter
import time

class Timer:
    def __init__(self):
        self.__t = None
        self.__p = None

    def start(self):
        self.__t = time.time()

    def pause(self):
        if not self.__p:
            self.__p = time.time()

    def resume(self):
        if self.__p:
            self.__t += (time.time() - self.__p)
            self.__p = None

    def display(self):
        if not self.__t:
            return
        delta = time.time() - self.__t
        if self.__p:
            delta = self.__p - self.__t
        m = int(delta/60)
        s = int(delta - m*60)
        return '{:0>2d} : {:0>2d}'.format(m, s)

timer = Timer()

root = tkinter.Tk()

label = tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
label.pack()

btn = tkinter.Button(root, text='pause')
btn.pack(side=tkinter.BOTTOM)

def action():
    text = btn['text']
    if text == 'pause':
        timer.pause()
        btn['text'] = 'resume'
    else:
        timer.resume()
        btn['text'] = 'pause'
btn.configure(command=action)

root.call('wm', 'attributes', '.', '-topmost', '1')

def go():
    timer.start()
    update()

def update():
    label['text'] = timer.display()
    root.after(50, update)

go()
root.mainloop()

print(timer.display())
