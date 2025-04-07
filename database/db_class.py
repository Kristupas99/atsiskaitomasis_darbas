import sqlite3
class Db():
    def __init__(self):
        self.conn = sqlite3.connect('database/database.db')

        self.c = self.conn.cursor()

    def create_database(self):
        self.c.execute("""
CREATE TABLE IF NOT EXISTS keliones (
                  id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  vardas VARCHAR(30) NOT NULL, 
                  pavarde VARCHAR(30) NOT NULL, 
                  el_pastas VARCHAR(100),
                  tel_nr VARCHAR(12),
                  isvykimo_vieta TEXT,
                  atvykimo_vieta TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
""")
    
    def add_new_record(self, data):
        columns = ', '.join([d for d in data])
        values = ', '.join(["'" + d + "'" for d in data.values()])

        self.c.execute(F'INSERT INTO keliones ({columns}) VALUES({values})')

        self.conn.commit()

    
    def get_records(self, where = ''):
        return self.c.execute('SELECT * FROM keliones').fetchall()
    
    def get_columns(self):
        info = self.c.execute('PRAGMA table_info(keliones)').fetchall()
        columns = [col[1] for col in info]
        return columns

    def delete_record(self, id):
        self.c.execute(f"DELETE FROM keliones WHERE id = {id}")
        self.conn.commit()

    def update_item(self, id, column, value):
        print(id, column, value)
        self.c.execute(f"UPDATE keliones SET {column} = '{value}' WHERE id = {id}")
        self.conn.commit()