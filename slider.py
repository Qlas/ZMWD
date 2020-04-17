from tkinter import *
import pandas as pd
from numpy import *
import numpy as np

root = Tk()

r = IntVar()
u = IntVar()
x = IntVar()
p = IntVar()
l = IntVar()
y = IntVar()


kryteria = ['komunikacja', 'udogodnienia', 'dostępność mediów', 'lokalizacja', 'zagrożenia']

value= IntVar

def klik(y, list=[], list1=[], list2=[], list3=[]):
    if y < 0:
        y = abs(y)
    if len(list) <= 3:
        list.append(y)
    elif len(list1) <= 2:
        list1.append(y)
    elif len(list2) <= 1:
        list2.append(y)
    elif len(list3) <= 0:
        list3.append(y)
    return print(list, list1, list2, list3)

krty1 = Label(root, text="smak").grid(row=1, column=0)
kryt2 = Label(root, text="kuchnia").grid(row=1, column=3)
slider = Scale(root, from_=-9, to=9 , resolution=3, variable=y, orient=HORIZONTAL).grid(row=1, column=1)
button = Button(root, text="add", command=lambda: klik(y.get())).grid(row=2, column=1)

exit = Button(root, text="Quit", command=root.quit).grid(row=3, column=1)



mainloop()
