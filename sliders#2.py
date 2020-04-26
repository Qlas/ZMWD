from tkinter import *
from numpy import *
import numpy as np

root = Tk()
y = DoubleVar()
f = DoubleVar()
g = DoubleVar()
actual = IntVar()
# macierz smak,kuchani,typXsmak,kuchnia,typ
matrix = np.zeros((3, 3), float)
np.fill_diagonal(matrix, 1)

users_list = []


def new_matrix():
    try:
        x = int(n_entry.get())
    except ValueError:
        x = 0
    if x > 0:
        for i in range(x):
            matrix = np.zeros((3, 3), float)
            np.fill_diagonal(matrix, 1)
            users_list.append(matrix)
        user_input()


def zmien(x):
    if x == 0:
        x = 1
    elif x < 0:
        x = 1 / abs(x)
    return x


def pokaz():
    print(matrix)


def fun():
    matrix[0][1] = zmien(y.get())
    matrix[1][0] = 1 / zmien(y.get())

    matrix[0][2] = zmien(f.get())
    matrix[2][0] = 1 / zmien(f.get())

    matrix[1][2] = zmien(g.get())
    matrix[2][1] = 1 / zmien(g.get())
    return matrix

def next_user():
        if actual.get() < len(users_list)-1:
            actual.set(actual.get()+1)
            user_input()
        else:
            pass    # stuff after weigh given by each user


def prev_user():
    if actual.get() > 0:
        actual.set(actual.get() - 1)
        user_input()


def user_input():
    print(actual.get())
    n_entry.destroy()
    n.destroy()
    gen.destroy()
    krty1 = Label(root, text=f'użytkownik: {actual.get()+1}').grid(row=0, column=2)
    krty1 = Label(root, text="smak").grid(row=1, column=0)
    slider = Scale(root, from_=-9, to=9, resolution=3, variable=y, orient=HORIZONTAL)
    slider.grid(row=1, column=2)
    slider.set(0)
    kryt2 = Label(root, text="kuchnia").grid(row=1, column=3)

    krty3 = Label(root, text="kuchnia").grid(row=3, column=0)
    slider1 = Scale(root, from_=-9, to=9, resolution=3, variable=f, orient=HORIZONTAL)
    slider1.grid(row=3, column=2)
    slider1.set(0)
    kryt4 = Label(root, text="typ").grid(row=3, column=3)

    krty5 = Label(root, text="smak").grid(row=5, column=0)
    slider2 = Scale(root, from_=-9, to=9, resolution=3, variable=g, orient=HORIZONTAL)
    slider2.grid(row=5, column=2)
    slider2.set(0)
    kryt6 = Label(root, text="typ").grid(row=5, column=3)

    save = Button(root, text="zapisz", command=fun)
    save.grid(row=6, column=2)
    next_window = Button(root, text="następny", command=next_user)
    next_window.grid(row=6, column=3)
    prev_window = Button(root, text="poprzedni", command=prev_user)
    prev_window.grid(row=6, column=0)
    check_results = Button(root, text="zobacz_wyniki", command=pokaz)

    check_results.grid(row=7, column=2)

n = Label(root, text="ile typa")
n.grid(row=0, column=0)
default_entry = IntVar()
default_entry.set(1)
n_entry = Entry(root, textvariable=default_entry)
n_entry.grid(row=0, column=2)
gen = Button(root, text="generuj", command=new_matrix)
gen.grid(row=0, column=3)
close = Button(root, text="Quit", command=root.destroy).grid(row=8, column=2)

"""
button1.grid(row=4, column=1)
button2.grid(row=6, column=1)

"""

mainloop()
