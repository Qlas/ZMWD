import tkinter as tk
import tkinter.ttk as ttk
from database import Database


class App(tk.Tk):
    users = []

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
        tk.Label(self, text="Start page", font=('Helvetica', 18, "bold")).grid(row=0, column=0)
        tk.Button(self, text="Znajdź obiad",
                  command=lambda: master.switch_frame(AmountPeople)).grid(row=1, column=0)
        tk.Button(self, text="Dodaj użytkownika",
                  command=lambda: master.switch_frame(AddNewUser_PageOne)).grid(row=2, column=0)


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

w = 0
class AddNewUser_PageOne(tk.Frame):
    def __init__(self, master):
        self.master = master
        global w
        w = tk.IntVar()
        tk.Frame.__init__(self, master)
        tk.Label(self, text="Imię", font=('Helvetica', 10)).grid(row=0, column=1)
        self.n_entry = tk.Entry(self)
        self.n_entry.grid(row=1, column=1, pady=(10, 10))
        tk.Label(self, text="Zaznacz czy..", font=('Helvetica', 18, "bold")).grid(row=2, column=1)
        tk.Radiobutton(self, text="Jesz mięso", variable=w, value=1).grid(row=3, column=1)
        tk.Radiobutton(self, text="Jesz ryby", variable=w, value=2).grid(row=4, column=1)
        tk.Radiobutton(self, text="Jesteś wegetarianinem", variable=w, value=3).grid(row=5, column=1)
        tk.Radiobutton(self, text="Jesteś weganinem", variable=w, value=4).grid(row=6, column=1)
        tk.Button(self, text="Dalej",
                  command=lambda: master.switch_frame(AddNewUser_PageTwo)).grid(row=7, column=2)
        tk.Button(self, text="Powrót",
                  command=lambda: master.switch_frame(StartPage)).grid(row=7, column=0)


class AddNewUser_PageTwo(tk.Frame):
    def __init__(self, master):
        self.master = master
        self.allergy = [tk.IntVar(), tk.IntVar(), tk.IntVar(), tk.IntVar()]

        tk.Frame.__init__(self, master)
        tk.Label(self, text="Jestem uczulony na ...", font=('Helvetica', 18, "bold")).grid(row=0, column=1)
        rb1 = tk.Checkbutton(self, text="nabiał", variable=self.allergy[0])

        rb1.grid(row=1, column=1)
        tk.Checkbutton(self, text="orzechy", variable=self.allergy[1]).grid(row=2, column=1)
        tk.Checkbutton(self, text="gluten", variable=self.allergy[2]).grid(row=3, column=1)
        tk.Checkbutton(self, text="jajka", variable=self.allergy[3]).grid(row=4, column=1)
        tk.Button(self, text="Dalej",
                  command=lambda: master.switch_frame(AddNewUser_PageThree)).grid(row=5, column=2)
        tk.Button(self, text="Powrót",
                  command=lambda: master.switch_frame(AddNewUser_PageOne)).grid(row=5, column=0)
        tk.Button(self, text="Wyczyść",
                  command=self.reset).grid(row=5, column=1)

    def reset(self):
        for i in self.allergy:
            i.set(0)



class AddNewUser_PageThree(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        y = tk.DoubleVar()
        f = tk.DoubleVar()
        g = tk.DoubleVar()
        tk.Label(self, text="Co wolisz bardziej", font=('Helvetica', 18, "bold")).grid(column=1)
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
                  command=lambda: master.switch_frame(AddNewUser_PageTwo)).grid(row=5, column=0)


if __name__ == '__main__':
    app = App()
    app.geometry("400x300")
    app.mainloop()
