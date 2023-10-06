import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  

    @classmethod
    def create_table(cls):
        CURSOR.execute('''CREATE TABLE IF NOT EXISTS dogs (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            breed TEXT
                        )''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS dogs')
        CONN.commit()

    def save(self):
        CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
        CONN.commit()
        self.id = CURSOR.lastrowid  
        return self

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        return dog.save()

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM dogs')
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute('SELECT * FROM dogs WHERE id = ?', (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

# Create the dogs table if it doesn't exist
Dog.create_table()
pass
