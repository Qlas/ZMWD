import sqlite3
import pandas as pd


class Database:
    def __init__(self):
        database_name = 'data.db'
        self.connect = sqlite3.connect(database_name)
        self.c = self.connect.cursor()
        self._create_new_database()

    def _create_new_database(self):
        try:
            self.c.execute("SELECT * FROM users")
        except sqlite3.OperationalError:
            self.c.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT NOT NULL)")
            self.c.execute("CREATE TABLE ahp_pref(ahp_pref_name TEXT PRIMARY KEY)")
            self.c.execute("CREATE TABLE res(res_name TEXT PRIMARY KEY)")
            self.c.execute("CREATE TABLE pref(type_name TEXT, subtype TEXT, PRIMARY KEY(type_name, subtype))")
            self.c.execute("CREATE TABLE user_ahp_pref(user_id INTEGER, ahp_pref_name TEXT, value REAL, FOREIGN KEY("
                           "user_id) REFERENCES users(id), FOREIGN KEY (ahp_pref_name) REFERENCES ahp_pref("
                           "ahp_pref_name), PRIMARY KEY (user_id, ahp_pref_name))")
            self.c.execute("CREATE TABLE user_res(user_id INTEGER, res_name TEXT, value REAL, FOREIGN KEY(user_id) "
                           "REFERENCES "
                           "users(id), FOREIGN KEY(res_name) REFERENCES res(res_name), PRIMARY KEY(user_id, "
                           "res_name))")
            self.c.execute("CREATE TABLE user_pref(user_id INTEGER, type_name TEXT, subtype TEXT, value REAL, "
                           "FOREIGN KEY( "
                           "user_id) REFERENCES users(id), FOREIGN KEY(type_name) REFERENCES pref(type_name), "
                           "FOREIGN KEY(subtype) REFERENCES pref(subtype), PRIMARY KEY(user_id, type_name, subtype))")
            self.c.execute("CREATE TABLE meals(id INTEGER PRIMARY KEY, name TEXT, wegetarianin INTEGER, weganin "
                           "INTEGER, "
                           "ryby INTEGER, nabiał INTEGER, orzechy INTEGER, gluten INTEGER, jajka INTEGER, "
                           "nasiona INTEGER, słony INTEGER, słodki INTEGER, ostry INTEGER, kwaśny INTEGER, "
                           "polska INTEGER, włoska INTEGER, japońska INTEGER, indyjska INTEGER, chińska INTEGER, "
                           "amerykańska INTEGER, śniadanie INTEGER, obiad INTEGER, kolacja INTEGER, zupa INTEGER, "
                           "sałatka INTEGER, makaron INTEGER, 'danie główne' INTEGER, deser INTEGER)")
            self._fill_data()
            self.connect.commit()

    def _fill_data(self):
        self.c.execute("INSERT INTO ahp_pref(ahp_pref_name) VALUES('kuchnia-smak'), ('typ-kuchnia'), ('typ-smak')")
        self.c.execute("INSERT INTO res(res_name) VALUES('nabiał'), ('orzechy'), ('gluten'), ('jajka i produkty "
                       "pochodne'), ('nasiona sezamu'), ('mięso'), ('wegetarianin'), ('weganin'), ('ryby')")
        self.c.execute("INSERT INTO pref(type_name, subtype) VALUES('smak', 'słony'), ('smak', 'słodki'), ('smak', "
                       "'kwaśny'), ('smak', 'ostry'), ('typ', 'zupa'), ('typ', 'sałatka'), ('typ', 'makaron'), "
                       "('typ', 'deser'), ('typ', 'danie główne'), ('kuchnia', 'polska'), ('kuchnia', 'włoska'), "
                       "('kuchnia', 'japońska'), ('kuchnia', 'indyjska'), ('kuchnia', 'chińska'), ('kuchnia', "
                       "'amerykańska')")
        data = read_xls()
        print(data[0])
        for i in data:
            self.c.execute("INSERT INTO meals VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?, ?)", i)

    def close_connection(self):
        self.connect.commit()
        self.connect.close()

    def save_user(self, data):
        print(data)
        self.c.execute("INSERT INTO users(name) VALUES(?)", (data['name'],))
        self.c.execute("SELECT id FROM users WHERE name = ?", (data['name'],))
        user_id = self.c.fetchall()[0][0]
        for key, value in data['const'].items():
            self.c.execute("INSERT INTO user_res(user_id, res_name, value) VALUES(?, ?, ?)", (user_id, key, value))
        for key, value in data['allergy'].items():
            self.c.execute("INSERT INTO user_res(user_id, res_name, value) VALUES(?, ?, ?)", (user_id, key, value))
        for key, value in data['ahp'].items():
            self.c.execute("INSERT INTO user_ahp_pref(user_id, ahp_pref_name, value) "
                           "VALUES(?, ?, ?)", (user_id, key, value))
        for key_type, value_type in data['pref'].items():
            for key, value in value_type.items():
                self.c.execute("INSERT INTO user_pref(user_id, type_name, subtype, value) "
                               "VALUES (?, ?, ?, ?)", (user_id, key_type, key, value))
        self.connect.commit()

    def get_user(self, name):
        user = {'name': name, 'const': {}, 'allergy': {}, 'ahp': {}, 'pref': {'smak': {}, 'typ': {}, 'kuchnia': {}}}
        self.c.execute("SELECT id FROM users WHERE name = ?", (name,))
        user_id = self.c.fetchall()[0][0]

        self.c.execute("SELECT ahp_pref_name, value FROM user_ahp_pref WHERE user_id = ?", (user_id,))
        for i in self.c.fetchall():
            user['ahp'][i[0]] = i[1]

        self.c.execute("SELECT type_name, subtype, value FROM user_pref WHERE user_id = ?", (user_id,))
        for i in self.c.fetchall():
            user['pref'][i[0]][i[1]] = i[2]

        self.c.execute("SELECT res_name, value FROM user_res WHERE user_id = ?", (user_id,))
        for i in self.c.fetchall():
            if i[0] in ('ryby', 'mięso', 'wegetarianin', 'weganin'):
                user['const'][i[0]] = int(i[1])
            else:
                user['allergy'][i[0]] = int(i[1])
        return user

    def update_user(self, data):
        self.c.execute("SELECT id FROM users WHERE name = ?", (data['name'],))
        user_id = self.c.fetchall()[0][0]

        for key, value in data['const'].items():
            self.c.execute("UPDATE user_res SET value = ? WHERE user_id = ? AND res_name = ?", (value, user_id, key))
        for key, value in data['allergy'].items():
            self.c.execute("UPDATE user_res SET value = ? WHERE user_id = ? AND res_name = ?", (value, user_id, key))
        for key, value in data['ahp'].items():
            self.c.execute("UPDATE user_ahp_pref SET value = ? WHERE user_id = ? AND ahp_pref_name = ?",
                           (value, user_id, key))
        for key_type, value_type in data['pref'].items():
            for key, value in value_type.items():
                self.c.execute("UPDATE user_pref SET value = ? WHERE user_id = ? AND type_name = ? AND subtype = ?",
                               (value, user_id, key_type, key))
        self.connect.commit()

    def add_meal(self, data):
        _list = [data['name']]
        if data['diet'].get() == 1:
            _list.append(0)
            _list.append(0)
        elif data['diet'].get() == 2:
            _list.append(1)
            _list.append(0)
        else:
            _list.append(0)
            _list.append(1)
        _list.append(data['fish'].get())
        for key, value in data['allergens'].items():
            _list.append(value.get())
        for key, value in data['smak'].items():
            _list.append(value.get())
        for key, value in data['kuchnia'].items():
            _list.append(value.get())
        for key, value in data['rodzaj'].items():
            _list.append(value.get())
        for key, value in data['typ'].items():
            _list.append(value.get())

        self.c.execute("INSERT INTO meals(name, wegetarianin, weganin, ryby, nabiał, orzechy, gluten, jajka, nasiona, "
                       "słony, słodki, ostry, kwaśny, polska, włoska, japońska, indyjska, chińska, amerykańska, "
                       "śniadanie, obiad, kolacja, zupa, sałatka, makaron, 'danie główne', deser) VALUES (?, ?, ?, ?, "
                       "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, "
                           "?, ?, ?, ?, ?, ?)", _list)
        self.connect.commit()


def read_xls():
    df = pd.read_excel('potrawy.xlsx', 'Arkusz1', skiprows=1)
    df.pop('link')
    df = df.transpose()
    return [df[i] for i in df if not pd.isnull(df[i][1]) and df[i][1] not in ('Nazwa', 'SUMA')]
