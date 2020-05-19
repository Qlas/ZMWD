import tkinter as tk
import tkinter.ttk as ttk
from database import Database
from meal_selection import MealSelection
from copy import deepcopy

class App(tk.Tk):
    users = []
    new_user = {'name': '', 'const': {}, 'allergy': {}, 'ahp': {}, 'pref': {'smak': {}, 'typ': {}, 'kuchnia': {}}}

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
        master.new_user = {'name': '', 'const': {}, 'allergy': {}, 'ahp': {},
                           'pref': {'smak': {}, 'typ': {}, 'kuchnia': {}}}
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
        master.database.c.execute("SELECT name FROM users")
        self.users = [i[0] for i in master.database.c.fetchall()]
        self.left_users = deepcopy(self.users)
        self.chosen_users = []

        self.error = tk.Label(self, text="", font=('Helvetica', 10))
        self.error.pack(side=tk.TOP)
        self.error.config(fg='red')

        canvas = tk.Canvas(self, borderwidth=0, height=20)
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw", tags="frame", width=400)
        canvas.pack(side="bottom", fill="both", expand=True)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)

        tk.Button(frame, text="kolejny",
                  command=self.another_user).pack()
        tk.Button(canvas, text="dalej",
                  command=self.next_page).pack(side=tk.RIGHT)
        tk.Button(canvas, text="powrót",
                  command=lambda: master.switch_frame(StartPage)).pack(side=tk.LEFT)

        tk.Label(self.frame, text="Wybierz posiłek", font=('Helvetica', 10)).grid(row=1, column=0)
        self.combo = ttk.Combobox(self.frame, values=['śniadanie', 'obiad', 'kolacja'], state="readonly")
        self.combo.grid(row=1, column=1)
        tk.Label(self.frame, text="Dodaj osoby", font=('Helvetica', 10)).grid(row=2, column=1)
        tk.Label(self.frame, text="Dodaj wagę", font=('Helvetica', 10)).grid(row=2, column=2)
        self.another_user()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def another_user(self):
        tk.Label(self.frame, text=f"User:{self.user_count + 1}", font=('Helvetica', 10)).grid(row=self.user_count + 3,
                                                                                        column=0)
        name = ttk.Combobox(self.frame, values=self.left_users, state="readonly")
        name.grid(row=self.user_count + 3, column=1, pady=(10, 10))
        name.bind('<<ComboboxSelected>>', self.changed)
        weight = tk.Entry(self.frame)
        weight.grid(row=self.user_count + 3, column=2, padx=(10, 10))
        self.chosen_users.append([name, weight])
        self.user_count += 1

    def changed(self, value):
        self.left_users = deepcopy(self.users)
        for i in self.chosen_users:
            if i[0].get() != '':
                self.left_users.pop(self.left_users.index(i[0].get()))
        for i in self.chosen_users:
            i[0]['values'] = self.left_users

    def next_page(self):
        users = []
        meal = self.combo.get()
        if meal == '':
            self.error['text'] = 'Wybierz posiłek'
            return
        try:
            for i in self.chosen_users:
                if i[0].get() != '':
                    users.append([i[0].get(), int(i[1].get())])
        except ValueError:
            self.error['text'] = 'Wpisz odpowiednią wagę'
            return
        if len(users) == 0:
            self.error['text'] = 'Musisz wybrać przynajmniej jednego użytkownika'
            return

        # users, meals
        self.master.switch_frame(StartPage)


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
        tk.Frame.__init__(self, master)
        print(self.master.new_user)
        self.actual = 'taste'
        self.master.database.c.execute("SELECT * FROM pref")
        data = self.master.database.c.fetchall()
        self.taste = [i[1] for i in data if i[0] == 'smak']
        self.type = [i[1] for i in data if i[0] == 'typ']
        self.cuisine = [i[1] for i in data if i[0] == 'kuchnia']
        self.title = tk.Label(self, text="Ustaw smak od najlepszego do najgorszego", font=('Helvetica', 10, "bold"))
        self.title.grid(column=1, columnspan=3)
        self.list_box = tk.Listbox(self, selectmode=tk.SINGLE)
        if len(master.new_user['pref']['smak']) == 0:
            self.instert_to_list(self.taste)
        else:
            self.actual = 'type'
            self.prev_page()
        self.list_box.grid(row=1, column=2, rowspan=8)

        tk.Button(self, text="up",
                  command=self.up).grid(row=3, column=3)
        tk.Button(self, text="down",
                  command=self.down).grid(row=4, column=3)

        self.next_button = tk.Button(self, text="dalej", command=self.next_page)
        self.next_button.grid(row=9, column=3)
        tk.Button(self, text="powrót", command=self.prev_page).grid(row=9, column=1)

    def prev_page(self):
        if self.actual == 'taste':
            self.master.switch_frame(AddNewUserPageThree)
        elif self.actual == 'type':
            self.title['text'] = "Ustaw smak od najlepszego do najgorszego"
            self.clear_list()
            self.actual = 'taste'
            _list = sorted(self.master.new_user['pref']['smak'].items(), key=lambda x: x[1], reverse=True)
            self.instert_to_list([i[0] for i in _list])
        else:
            self.title['text'] = "Ustaw typ od najlepszego do najgorszego"
            self.next_button['text'] = 'dalej'
            self.clear_list()
            self.actual = 'type'
            _list = sorted(self.master.new_user['pref']['typ'].items(), key=lambda x: x[1], reverse=True)
            self.instert_to_list([i[0] for i in _list])

    def next_page(self):
        if self.actual == 'taste':
            self.title['text'] = "Ustaw typ od najlepszego do najgorszego"
            for i in self.taste:
                self.master.new_user['pref']['smak'][i] = self.list_box.index(tk.END) \
                                                          - self.list_box.get(0, "end").index(i)
            self.actual = 'type'
            self.clear_list()
            self.instert_to_list(self.type)
        elif self.actual == 'type':
            self.title['text'] = "Ustaw kuchnie od najlepszego do najgorszego"
            for i in self.type:
                self.master.new_user['pref']['typ'][i] = self.list_box.index(tk.END) \
                                                         - self.list_box.get(0, "end").index(i)
            self.actual = 'cuisine'
            self.clear_list()
            self.instert_to_list(self.cuisine)
            self.next_button['text'] = 'Zapisz'
        else:
            for i in self.cuisine:
                self.master.new_user['pref']['kuchnia'][i] = self.list_box.index(tk.END) \
                                                             - self.list_box.get(0, "end").index(i)

            self.master.database.save_user(self.master.new_user)
            self.master.switch_frame(StartPage)
        print(self.master.new_user)

    def clear_list(self):
        while self.list_box.index(tk.END) > 0:
            print(self.list_box.index(tk.END))
            self.list_box.delete(0)

    def instert_to_list(self, _list):
        for i in _list:
            self.list_box.insert(tk.END, i)

    def up(self):
        active = self.list_box.index(tk.ACTIVE)
        if active != 0:
            text = self.list_box.get(active)
            self.list_box.delete(active)
            self.list_box.insert(active - 1, text)
            self.list_box.activate(active - 1)

    def down(self):
        active = self.list_box.index(tk.ACTIVE)
        text = self.list_box.get(active)
        self.list_box.delete(active)
        self.list_box.insert(active + 1, text)
        self.list_box.activate(active + 1)


if __name__ == '__main__':
    app = App()
    app.geometry("400x300")
    app.mainloop()
