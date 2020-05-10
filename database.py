import sqlite3


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
