import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import sqlite3

# y = DoubleVar()
# f = DoubleVar()
# g = DoubleVar()
# actual = IntVar()
# weight = IntVar()
# # macierz smak,kuchani,typXsmak,kuchnia,typ
# matrix = np.zeros((3, 3), float)
# np.fill_diagonal(matrix, 1)
#
# users_list = []
#
#
# def new_matrix():
#     try:
#         x = int(n_entry.get())
#     except ValueError:
#         x = 0
#     if x > 0:
#         for i in range(x):
#             matrix = np.zeros((3, 3), float)
#             np.fill_diagonal(matrix, 1)
#             users_list.append(matrix)
#         #user_input()
#         wagi(x)
#
#
# def zmien(x):
#     if x == 0:
#         x = 1
#     elif x < 0:
#         x = 1 / abs(x)
#     return x
#
#
# def pokaz():
#     print(matrix)
#
#
# def fun():
#     matrix[0][1] = zmien(y.get())
#     matrix[1][0] = 1 / zmien(y.get())
#
#     matrix[0][2] = zmien(f.get())
#     matrix[2][0] = 1 / zmien(f.get())
#
#     matrix[1][2] = zmien(g.get())
#     matrix[2][1] = 1 / zmien(g.get())
#     return matrix
#
# def next_user():
#         if actual.get() < len(users_list)-1:
#             actual.set(actual.get()+1)
#             user_input()
#         else:
#             pass    # stuff after weigh given by each user
#
#
# def prev_user():
#     if actual.get() > 0:
#         actual.set(actual.get() - 1)
#         user_input()
#
# def wagi(x):
#
#     n_entry.destroy()
#     n.destroy()
#     gen.destroy()
#     weights_l = Label(root, text="waga dla użytkowników: ").grid(row=0, column=0)
#
#     for i in range(x):
#         weight_l = Label(root, text='użytkownik' + str(i) + ':').grid(row=i + 1, column=0)
#         default_entry = IntVar()
#         default_entry.set(1)
#         weight_e = Entry(root, textvariable=default_entry).grid(row=i + 1, column=1)
#     weight_b = Button(root, text="dalej", command=user_input).grid(row=x + 1, column=1)
#
#
# def user_input():
#     print(actual.get())
#     #n_entry.destroy()
#     #n.destroy()
#     #gen.destroy()
#     krty1 = Label(root, text=f'użytkownik: {actual.get()+1}').grid(row=0, column=2)
#     krty1 = Label(root, text="smak").grid(row=1, column=0)
#     slider = Scale(root, from_=-9, to=9, resolution=3, variable=y, orient=HORIZONTAL)
#     slider.grid(row=1, column=2)
#     slider.set(0)
#     kryt2 = Label(root, text="kuchnia").grid(row=1, column=3)
#
#     krty3 = Label(root, text="kuchnia").grid(row=3, column=0)
#     slider1 = Scale(root, from_=-9, to=9, resolution=3, variable=f, orient=HORIZONTAL)
#     slider1.grid(row=3, column=2)
#     slider1.set(0)
#     kryt4 = Label(root, text="typ").grid(row=3, column=3)
#
#     krty5 = Label(root, text="smak").grid(row=5, column=0)
#     slider2 = Scale(root, from_=-9, to=9, resolution=3, variable=g, orient=HORIZONTAL)
#     slider2.grid(row=5, column=2)
#     slider2.set(0)
#     kryt6 = Label(root, text="typ").grid(row=5, column=3)
#
#     save = Button(root, text="zapisz", command=fun)
#     save.grid(row=6, column=2)
#     next_window = Button(root, text="następny", command=next_user)
#     next_window.grid(row=6, column=3)
#     prev_window = Button(root, text="poprzedni", command=prev_user)
#     prev_window.grid(row=6, column=0)
#     check_results = Button(root, text="zobacz_wyniki", command=pokaz)
#
#     check_results.grid(row=7, column=2)
#
# n = Label(root, text="ile typa")
# n.grid(row=0, column=0)
# default_entry = IntVar()
# default_entry.set(1)
# n_entry = Entry(root, textvariable=default_entry)
# n_entry.grid(row=0, column=2)
# gen = Button(root, text="generuj", command=new_matrix)
# gen.grid(row=0, column=3)
#
# close = Button(root, text="Quit", command=root.destroy).grid(row=8, column=2)


def database():
    database_name = 'data.db'
    connect = sqlite3.connect(database_name)
    c = connect.cursor()
    try:
        c.execute("SELECT * FROM USER")
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE user(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")


class App(tk.Tk):
    users = []

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        database()
        self.switch_frame(StartPage)
        tk.Button(self, text="Quit", command=self.destroy).pack(side="bottom")

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).grid(row=0, column=0)
        tk.Button(self, text="Znajdź obiad",
                  command=lambda: master.switch_frame(AmountPeople)).grid(row=1, column=0)
        tk.Button(self, text="Dodaj użytkownika",
                  command=lambda: master.switch_frame(AddNewUser)).grid(row=2, column=0)


class AmountPeople(tk.Frame):
    user_count = 0

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        tk.Label(self, text="Dodaj osoby", font=('Helvetica', 10)).grid(row=0, column=1)
        tk.Label(self, text="Dodaj wagę", font=('Helvetica', 10)).grid(row=0, column=2)
        self.another_user()
        tk.Button(self, text="kolejny",
                  command=self.another_user).grid(row=100, column=1)
        tk.Button(self, text="dalej",
                  command=lambda: master.switch_frame(StartPage)).grid(row=100, column=2)
        tk.Button(self, text="powrót",
                  command=lambda: master.switch_frame(StartPage)).grid(row=100, column=0)

    def another_user(self):
        tk.Label(self, text=f"User:{self.user_count+1}", font=('Helvetica', 10)).grid(row=self.user_count+1, column=0)
        self.n_entry = tk.Entry(self)
        self.n_entry.grid(row=self.user_count+1, column=2, padx=(10, 10))
        self.n_entry = ttk.Combobox(self)
        self.n_entry.grid(row=self.user_count+1, column=1, pady=(10, 10))
        self.user_count += 1


class AddNewUser(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        y = tk.DoubleVar()
        f = tk.DoubleVar()
        g = tk.DoubleVar()
        tk.Label(self, text="Nazwa", font=('Helvetica', 10)).grid(row=0, column=1)
        self.n_entry = tk.Entry(self)
        self.n_entry.grid(row=1, column=1, pady=(10, 10))
        kryt1 = tk.Label(self, text="smak").grid(row=2, column=0)
        slider = tk.Scale(self, from_=-9, to=9, resolution=3, variable=y, orient=tk.HORIZONTAL)
        slider.grid(row=2, column=1)
        slider.set(0)
        kryt2 = tk.Label(self, text="kuchnia").grid(row=2, column=2)

        krty3 = tk.Label(self, text="kuchnia").grid(row=3, column=0)
        slider1 = tk.Scale(self, from_=-9, to=9, resolution=3, variable=f, orient=tk.HORIZONTAL)
        slider1.grid(row=3, column=1)
        slider1.set(0)
        kryt4 = tk.Label(self, text="typ").grid(row=3, column=2)

        krty5 = tk.Label(self, text="smak").grid(row=4, column=0)
        slider2 = tk.Scale(self, from_=-9, to=9, resolution=3, variable=g, orient=tk.HORIZONTAL)
        slider2.grid(row=4, column=1)
        slider2.set(0)
        kryt6 = tk.Label(self, text="typ").grid(row=4, column=2)
        tk.Button(self, text="zapisz",
                  command=lambda: master.switch_frame(StartPage)).grid(row=5, column=2)
        tk.Button(self, text="powrót",
                  command=lambda: master.switch_frame(StartPage)).grid(row=5, column=0)


if __name__ == '__main__':
    app = App()
    app.geometry("400x300")
    app.mainloop()
