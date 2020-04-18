from tkinter import *
from tkinter import Button
from numpy import *
import numpy as np

root = Tk()
y = DoubleVar()
f = DoubleVar()
g = DoubleVar()


matrix = np.zeros((3, 3), float)
np.fill_diagonal(matrix, 1)

def switch(v):
    if v == "button":
        button.config(state=DISABLED)
    elif v == "button1":
        button1.config(state=DISABLED)
    elif v == "button2":
        button2.config(state=DISABLED)


def zmien(x):
    if x == 0:
        x =1
    elif x < 0:
         x = 1/abs(x)
    return x


def klik(y):
    y = zmien(y)
    for i in range(len(matrix)):
        find = False
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                matrix[i][j] = y
                matrix[j][i] = 1 / y
                find = True
                break
        if find:
            break
    return print(matrix)


krty1 = Label(root, text="smak").grid(row=1, column=0)
kryt2 = Label(root, text="kuchnia").grid(row=1, column=3)
krty3 = Label(root, text="kuchnia").grid(row=3, column=0)
kryt4 = Label(root, text="typ").grid(row=3, column=3)
krty5 = Label(root, text="smak").grid(row=5, column=0)
kryt6 = Label(root, text="typ").grid(row=5, column=3)


slider = Scale(root, from_=-9, to=9, resolution=3, variable=y, orient=HORIZONTAL).grid(row=1, column=1)
slider1 = Scale(root, from_=-9, to=9, resolution=3, variable=f, orient=HORIZONTAL).grid(row=3, column=1)
slider2 = Scale(root, from_=-9, to=9, resolution=3, variable=g, orient=HORIZONTAL).grid(row=5, column=1)

button = Button(root, text="add", command=lambda: [klik(y.get()), switch("button")])
button1 = Button(root, text="add", command=lambda: [klik(f.get()), switch("button1")])
button2 = Button(root, text="add", command=lambda: [klik(g.get()), switch("button2")])

exit = Button(root, text="Quit", command=switch).grid(row=7, column=1)

button.grid(row=2, column=1)
button1.grid(row=4, column=1)
button2.grid(row=6, column=1)
mainloop()
