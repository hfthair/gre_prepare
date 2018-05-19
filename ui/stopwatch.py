import tkinter
import time

root = tkinter.Tk()
label = tkinter.Label(root, text="Welcome!", fg="black", font="Verdana 30 bold")
label.pack()
root.call('wm', 'attributes', '.', '-topmost', '1')

start = None

def go():
    global start
    start = time.time()
    update()

def update():
    delta = time.time() - start
    m = int(delta/60)
    s = int(delta - m*60)
    label['text'] = '{:0>2d} : {:0>2d}'.format(m, s)
    root.after(50, update)

go()
root.mainloop()