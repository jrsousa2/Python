#Also note that `from <module> import *` is generally frowned upon
#since it can lead to namespace collisions. It's much better to only
#explicitly import the things you need.
from tkinter import Tk, Label
root = Tk()
w = Label(root, text="Hello, world!")
w.pack()
root.mainloop()