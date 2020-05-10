import tkinter as tk
import tkinter.ttk as ttk
from database import Database


class App(tk.Tk):
    users = []
    new_user = {'name': '', 'const': {}, 'allergy': {}, 'ahp': {}}

    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.database = Database()
        self.switch_frame(StartPage)
        tk.Button(self, text="Quit", command=self.exit_program).pack(side="bottom")

    def exit_program(self):
        self.database.close_connection()
        self.destroy()

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.new_user = {'name': '', 'const': {}, 'allergy': {}, 'ahp': {}}
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).grid(row=0, column=0)
        tk.Button(self, text="Znajdź obiad",
                  command=lambda: master.switch_frame(AmountPeople)).grid(row=1, column=0)
        tk.Button(self, text="Dodaj użytkownika",
                  command=lambda: master.switch_frame(AddNewUserPageOne)).grid(row=2, column=0)


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
        tk.Label(self, text=f"User:{self.user_count + 1}", font=('Helvetica', 10)).grid(row=self.user_count + 1,
                                                                                        column=0)
        self.n_entry = tk.Entry(self)
        self.n_entry.grid(row=self.user_count + 1, column=2, padx=(10, 10))
        self.n_entry = ttk.Combobox(self)
        self.n_entry.grid(row=self.user_count + 1, column=1, pady=(10, 10))
        self.user_count += 1


class AddNewUserPageOne(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.fish = tk.IntVar()
        self.w = tk.IntVar()
        tk.Frame.__init__(self, master)
        self.error = tk.Label(self, text='', font=('Helvetica', 10, 'bold'))
        self.error.config(fg='red')
        self.error.grid(row=8, column=1)
        tk.Label(self, text="Imię", font=('Helvetica', 10)).grid(row=0, column=1)
        self.n_entry = tk.Entry(self)
        self.n_entry.grid(row=1, column=1, pady=(10, 10))
        tk.Label(self, text="Zaznacz czy..", font=('Helvetica', 18, "bold")).grid(row=2, column=1)
        tk.Radiobutton(self, text="Jesz mięso", variable=self.w, value=1).grid(row=3, column=1)
        tk.Radiobutton(self, text="Jesteś wegetarianinem", variable=self.w, value=2).grid(row=4, column=1)
        tk.Radiobutton(self, text="Jesteś weganinem", variable=self.w, value=3).grid(row=5, column=1)
        tk.Checkbutton(self, text="Jesz ryby", variable=self.fish).grid(row=6, column=1)
        tk.Button(self, text="Dalej",
                  command=self.next_page).grid(row=7, column=2)
        tk.Button(self, text="Powrót",
                  command=lambda: master.switch_frame(StartPage)).grid(row=7, column=0)
        if self.master.new_user['name'] != '':
            self.set_values()

    def set_values(self):
        self.n_entry.insert(0, self.master.new_user['name'])
        if self.master.new_user['const']['mięso'] == 1:
            self.w.set(1)
        elif self.master.new_user['const']['wegetarianin'] == 1:
            self.w.set(2)
        else:
            self.w.set(3)
        self.fish.set(self.master.new_user['const']['ryby'])

    def next_page(self):
        if self.n_entry.get() == '' or self.n_entry.get().startswith(' '):
            self.error['text'] = 'Podaj imię'
        else:
            self.master.database.c.execute("SELECT * FROM users WHERE name=?", (self.n_entry.get(),))
            print()
            if len(self.master.database.c.fetchall()) != 0:
                self.error['text'] = 'To imię jest już zajęte'
            elif self.w.get() == 0:
                self.error['text'] = 'Musisz zaznaczyć radio'
            else:
                self.master.new_user['name'] = self.n_entry.get()
                self.master.new_user['const'] = {'ryby': self.fish.get(),
                                                 'mięso': 1 if self.w.get() == 1 else 0,
                                                 'wegetarianin': 1 if self.w.get() == 2 else 0,
                                                 'weganin': 1 if self.w.get() == 3 else 0}
                self.master.switch_frame(AddNewUserPageTwo)


class AddNewUserPageTwo(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.allergy = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.allergies = ('nabiał', 'orzechy', 'gluten', 'jajka')
        tk.Frame.__init__(self, master)

        print(self.master.new_user)
        tk.Label(self, text="Jestem uczulony na ...", font=('Helvetica', 18, "bold")).grid(row=0, column=1)
        for i in range(len(self.allergies)):
            tk.Checkbutton(self, text=self.allergies[i], variable=self.allergy[i]).grid(row=i + 1, column=1)
        tk.Button(self, text="Dalej",
                  command=self.next_page).grid(row=5, column=2)
        tk.Button(self, text="Powrót",
                  command=lambda: master.switch_frame(AddNewUserPageOne)).grid(row=5, column=0)
        tk.Button(self, text="Wyczyść",
                  command=self.reset).grid(row=5, column=1)

        if len(self.master.new_user['allergy'].values()) > 0:
            self.set_values()

    def set_values(self):
        values = list(self.master.new_user['allergy'].values())
        for i in range(len(values)):
            self.allergy[i].set(values[i])

    def reset(self):
        for i in self.allergy:
            i.set(0)

    def next_page(self):
        for i in range(len(self.allergies)):
            self.master.new_user['allergy'][self.allergies[i]] = self.allergy[i].get()
        print(self.master.new_user)
        self.master.switch_frame(AddNewUserPageThree)


class AddNewUserPageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.values = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
        for i in self.values:
            i.set(4)
        self.ahp_value = [1 / 9, 1 / 7, 1 / 5, 1 / 3, 1, 3, 5, 7, 9]
        self.value_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.labels = []
        tk.Label(self, text="Co wolisz bardziej", font=('Helvetica', 18, "bold")).grid(column=1)
        self.sliders = []
        self.text_val = ['ekstremalna przewaga', 'bardzo silna przewaga', 'silna przewaga', 'umiarkowana przewaga',
                         'równość', 'umiarkowana przewaga', 'silna przewaga', 'bardzo silna przewaga',
                         'ekstremalna przewaga']

        self.labels.append(tk.Label(self, text=self.text_val[4]))
        self.labels[0].grid(row=1, column=1)
        tk.Label(self, text="smak").grid(row=2, column=0)
        self.sliders.append(tk.Scale(self, from_=0, to=8,
                                     command=lambda value: self.value_check(value, self.labels[0]),
                                     orient=tk.HORIZONTAL, showvalue=0, variable=self.values[0]))
        self.sliders[0].grid(row=2, column=1)
        tk.Label(self, text="kuchnia").grid(row=2, column=2)

        tk.Label(self).grid(row=3, column=1)

        self.labels.append(tk.Label(self, text=self.text_val[4]))
        self.labels[1].grid(row=4, column=1)
        tk.Label(self, text="kuchnia").grid(row=5, column=0)
        self.sliders.append(tk.Scale(self, from_=0, to=8,
                                     command=lambda value: self.value_check(value, self.labels[1]),
                                     orient=tk.HORIZONTAL, showvalue=0, variable=self.values[1]))
        self.sliders[1].grid(row=5, column=1)
        tk.Label(self, text="typ").grid(row=5, column=2)

        tk.Label(self).grid(row=6, column=1)

        self.labels.append(tk.Label(self, text=self.text_val[4]))
        self.labels[2].grid(row=7, column=1)
        tk.Label(self, text="smak").grid(row=8, column=0)
        self.sliders.append(tk.Scale(self, from_=0, to=8,
                                     command=lambda value: self.value_check(value, self.labels[2]),
                                     orient=tk.HORIZONTAL, showvalue=0, variable=self.values[2]))
        self.sliders[2].grid(row=8, column=1)
        tk.Label(self, text="typ").grid(row=8, column=2)

        tk.Button(self, text="dalej",
                  command=self.next_page).grid(row=9, column=2)
        tk.Button(self, text="powrót",
                  command=lambda: master.switch_frame(AddNewUserPageTwo)).grid(row=9, column=0)

        if len(self.master.new_user['ahp'].values()) > 0:
            self.set_values()

    def set_values(self):
        values = list(self.master.new_user['ahp'].values())
        for i in range(len(self.values)):
            value = self.ahp_value.index(values[i])
            self.values[i].set(value)
            self.value_check(value, self.labels[i])

    def value_check(self, value, label):
        label['text'] = self.text_val[int(value)]

    def next_page(self):
        self.master.new_user['ahp'] = {}
        names = ('kuchnia-smak', 'typ-kuchnia', 'typ-smak')
        for i in range(len(names)):
            self.master.new_user['ahp'][names[i]] = self.ahp_value[self.values[i].get()]
        print(self.master.new_user)
        self.master.switch_frame(AddNewUserPageFour)


class AddNewUserPageFour(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.allergy = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.allergies = ('nabiał', 'orzechy', 'gluten', 'jajka')
        tk.Frame.__init__(self, master)

        print(self.master.new_user)
        tk.Label(self, text="NOT IMPLEMENTED YET", font=('Helvetica', 18, "bold")).grid(row=0, column=1)
        for i in range(len(self.allergies)):
            tk.Checkbutton(self, text=self.allergies[i], variable=self.allergy[i]).grid(row=i + 1, column=1)
        tk.Button(self, text="Dalej",
                  command=self.next_page).grid(row=5, column=2)
        tk.Button(self, text="Powrót",
                  command=lambda: master.switch_frame(AddNewUserPageThree)).grid(row=5, column=0)
        tk.Button(self, text="Wyczyść",
                  command=self.reset).grid(row=5, column=1)



    def set_values(self):
        values = list(self.master.new_user[next(iter(self.master.new_user))]['allergy'].values())
        for i in range(len(values)):
            self.allergy[i].set(values[i])

    def reset(self):
        for i in self.allergy:
            i.set(0)

    def next_page(self):
        self.master.new_user[next(iter(self.master.new_user))]['allergy'] = {}
        for i in range(len(self.allergies)):
            self.master.new_user[next(iter(self.master.new_user))]['allergy'][self.allergies[i]] = self.allergy[i].get()
        print(self.master.new_user)
        self.master.switch_frame(AddNewUserPageThree)


if __name__ == '__main__':
    app = App()
    app.geometry("400x300")
    app.mainloop()
