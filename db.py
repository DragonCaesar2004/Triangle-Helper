import sqlite3 as sql
insert = 'INSERT OR IGNORE INTO '
create = 'CREATE TABLE IF NOT EXISTS '

class DB:

    def __init__(self):
        self.connection = sql.connect('db.db')
        self.cursor = self.connection.cursor()

    def save(self):
        self.connection.commit()

    def close(self):
        self.save()
        self.cursor.close()

    def create_tables(self):
        self.cursor.execute(create+'users (user_id INTEGER UNIQUE NOT NULL)')
        self.cursor.execute(create+'statistic (name TEXT UNIQUE NOT NULL, users_count INTEGER DEFAULT 0)')
        self.cursor.execute(create + 'last_data (data TEXT, id INTEGER UNIQUE NOT NULL DEFAULT 1)')
        self.cursor.execute(insert + 'last_data (data) VALUES (?)',['test'] )
        self.cursor.execute(create + 'user_last_data (user_id INTEGER UNIQUE NOT NULL, value TEXT)')
        #self.cursor.execute('DROP TABLE user_values')
        self.cursor.execute(create + '''user_values (
        user_id INTEGER UNIQUE NOT NULL,
        a REAL,
        b REAL,
        c REAL,
        cora REAL,
        corb REAL,
        corc REAL,
        s REAL,
        R REAL,
        rr REAL,
        p REAL,
        sina REAL,
        sinb REAL,
        sinc REAL,
        cosa REAL,
        cosb REAL,
        cosc REAL,
        ha REAL,
        hb REAL,
        hc REAL,
        bisa REAL,
        bisb REAL,
        bisc REAL,
        meda REAL,
        medb REAL,
        medc REAL
        )''')
        self.save()
        self.close()

    def insert_user(self, user_id):
        self.cursor.execute(insert + 'users VALUES (?)', [user_id])
        self.save()

    def create_statistic_name(self, name):
        self.cursor.execute(insert + 'statistic VALUES (?)', [name])
        self.save()

    def insert_statistic(self, name):
        self.create_statistic_name(name)
        self.cursor.execute('UPDATE statistic SET users_count = users_count + 1 WHERE name = (?)', [name])
        self.save()

    def extract_statistic(self):
        return self.cursor.execute('SELECT * FROM statistic').fetchall()

    def extract_users(self):
        users = self.cursor.execute('SELECT * FROM users').fetchall()
        return [u[0] for u in users]

    def delete_user(self, user_id):
        self.cursor.execute('DELETE * FROM users WHERE user_id = (?)', [user_id])
        self.save()

    def insert_data(self, data):
        self.cursor.execute('UPDATE last_data SET data = (?) WHERE id IS 1', [data])
        self.save()

    def extract_data(self):
        return self.cursor.execute('SELECT data FROM last_data WHERE id IS 1').fetchone()[0]

    def insert_user_last_data(self, user_id, value):
        self.cursor.execute(insert + 'user_last_data VALUES (?, ?)', (user_id, value))
        try:self.cursor.execute(f'UPDATE user_last_data SET value = (?) WHERE user_id = {user_id}', [value])
        except Exception as e: print(e)
        self.save()

    def extract_user_last_data(self, user_id):
        data = self.cursor.execute(f'SELECT value FROM user_last_data WHERE user_id = {user_id}').fetchone()
        return data[0]

    def set_user_values(self, user_id):
        self.cursor.execute(f'DELETE FROM user_values WHERE user_id = {user_id}')
        self.cursor.execute(insert + 'user_values (user_id) VALUES (?)', [user_id])
        self.save()

    def update_value(self, user_id, value):
        value_type = self.extract_user_last_data(user_id)
        self.cursor.execute(f'UPDATE user_values SET {value_type} = "{value}" WHERE user_id = {user_id}')
        self.save()

    def extract_values(self, user_id):
        data = self.cursor.execute(f'SELECT * FROM user_values WHERE user_id = {user_id}').fetchall()
        return data[0]


DB().create_tables()

