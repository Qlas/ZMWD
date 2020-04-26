from tkinter import *
from tkinter import Button
from numpy import *
import numpy as np

root = Tk()
y = DoubleVar()
f = DoubleVar()
g = DoubleVar()


# macierz smak,kuchani,typXsmak,kuchnia,typ
matrix = np.zeros((3, 3), float)
np.fill_diagonal(matrix, 1)

users_list = []


def new_matrix():
    x = int(n_entry.get())
    for i in range(x):
        matrix = np.zeros((3, 3), float)
        np.fill_diagonal(matrix, 1)
        users_list.append(matrix)
    return print(users_list)


def zmien(x):
    if x == 0:
        x = 1
    elif x < 0:
        x = 1 / abs(x)
    return x


def pokaz():
    return print(matrix)


def fun(value, l):
    value = zmien(value)
    for i in range(len(matrix)):
        find = False
        for j in range(len(matrix[i])):
            if l == y:
                matrix[0][1] = value
                matrix[1][0] = 1 / value
            elif l == f:
                matrix[0][2] = value
                matrix[2][0] = 1 / value
            elif l == g:
                matrix[1][2] = value
                matrix[2][1] = 1 / value
        if find:
            break
    return matrix


n = Label(root, text="ile typa").grid(row=0, column=0)
n_entry = Entry(root)
n_entry.grid(row=0, column=1)
gen = Button(root, text="generuj", command=new_matrix).grid(row=0, column=3)

krty1 = Label(root, text="smak").grid(row=1, column=0)
kryt2 = Label(root, text="kuchnia").grid(row=1, column=3)
krty3 = Label(root, text="kuchnia").grid(row=3, column=0)
kryt4 = Label(root, text="typ").grid(row=3, column=3)
krty5 = Label(root, text="smak").grid(row=5, column=0)
kryt6 = Label(root, text="typ").grid(row=5, column=3)

slider = Scale(root, from_=-9, to=9, resolution=3, variable=y, orient=HORIZONTAL).grid(row=1, column=1)
slider1 = Scale(root, from_=-9, to=9, resolution=3, variable=f, orient=HORIZONTAL).grid(row=3, column=1)
slider2 = Scale(root, from_=-9, to=9, resolution=3, variable=g, orient=HORIZONTAL).grid(row=5, column=1)
"""
button = Button(root, text="add", command=lambda: [klik(y.get()), switch("button"), fun(y)])
button1 = Button(root, text="add", command=lambda: [klik(f.get()), switch("button1"), fun(f)])
button2 = Button(root, text="add", command=lambda: [klik(g.get()), switch("button2"), fun(g)])
"""
button = Button(root, text="zapisz", command=lambda: [fun(y.get(), y), fun(f.get(), f), fun(g.get(), g)])
button4 = Button(root, text="zobacz_wyniki", command=lambda: pokaz())
exit = Button(root, text="Quit", command=root.quit()).grid(row=8, column=1)

button.grid(row=6, column=1)
button4.grid(row=7, column=1)
"""
button1.grid(row=4, column=1)
button2.grid(row=6, column=1)

"""
mainloop()
