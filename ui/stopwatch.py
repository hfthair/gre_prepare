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

    def reset(self):
        self.__t = None
        self.__p = None
        self.start()

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
root.title('stopwatch')

label = tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
label.grid(row=0, column=0, columnspan=4, pady=3)

btn = tkinter.Button(root, text='pause', width=8)
btn.grid(row=1, column=1, pady=3)

def pause_or_resume(e=None):
    text = btn['text']
    if text == 'pause':
        timer.pause()
        btn['text'] = 'resume'
    else:
        timer.resume()
        btn['text'] = 'pause'
btn.configure(command=pause_or_resume)

def reset():
    timer.reset()
    btn['text'] = 'pause'
tkinter.Button(root, text='reset', width=8, command=reset).grid(row=1, column=2, pady=3)

root.bind('<space>', pause_or_resume)
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
