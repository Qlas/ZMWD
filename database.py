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
            self.c.execute("CREATE TABLE user_ahp_pref(user_id INTEGER, ahp_pref_name TEXT, FOREIGN KEY("
                           "user_id) REFERENCES users(id), FOREIGN KEY (ahp_pref_name) REFERENCES ahp_pref("
                           "ahp_pref_name), PRIMARY KEY (user_id, ahp_pref_name))")
            self.c.execute("CREATE TABLE user_res(user_id INTEGER, res_name TEXT, FOREIGN KEY(user_id) REFERENCES "
                           "users(id), FOREIGN KEY(res_name) REFERENCES res(res_name), PRIMARY KEY(user_id, "
                           "res_name))")
            self.c.execute("CREATE TABLE user_pref(user_id INTEGER, type_name TEXT, subtype TEXT, FOREIGN KEY("
                           "user_id) REFERENCES users(id), FOREIGN KEY(type_name) REFERENCES pref(type_name), "
                           "FOREIGN KEY(subtype) REFERENCES pref(subtype), PRIMARY KEY(user_id, type_name, subtype))")
            self._fill_data()

            self.connect.commit()

    def _fill_data(self):
        self.c.execute("INSERT INTO ahp_pref(ahp_pref_name) VALUES('kuchnia-smak'), ('kuchnia-typ'), ('smak-typ')")
        self.c.execute("INSERT INTO res(res_name) VALUES('nabiał'), ('orzechy'), ('gluten'), ('jajka i produkty "
                       "pochodne'), ('nasiona sezamu'), ('wegetarianin'), ('weganin'), ('ryby')")
        self.c.execute("INSERT INTO pref(type_name, subtype) VALUES('smak', 'słony'), ('smak', 'słodki'), ('smak', "
                       "'kwaśny'), ('smak', 'ostry'), ('typ', 'zupa'), ('typ', 'sałatka'), ('typ', 'makaron'), "
                       "('typ', 'deser'), ('typ', 'danie główne'), ('kuchnia', 'polska'), ('kuchnia', 'włoska'), "
                       "('kuchnia', 'japońska'), ('kuchnia', 'indyjska'), ('kuchnia', 'chińska'), ('kuchnia', "
                       "'amerykańska')")

    def close_connection(self):
        self.connect.commit()
        self.connect.close()
