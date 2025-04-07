import sqlite3

# Klasė valdyti duomenų bazę
class Db():
    def __init__(self):
        # Prisijungimas
        self.conn = sqlite3.connect('database/database.db')

        # Kursorius
        self.c = self.conn.cursor()

    # Funkcija sukurti duomenu bazė jeigu egzistuoja
    def create_database(self) -> None:
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
    
    # Funkcija pridėti naują įrašą
    def add_new_record(self, data) -> None:
        columns = ', '.join([d for d in data])
        values = ', '.join(["'" + d + "'" for d in data.values()])

        self.c.execute(F'INSERT INTO keliones ({columns}) VALUES({values})')

        self.conn.commit()

    
    # Funkcija pasiimti visus įrašus
    def get_records(self, filtrai: list=[]) -> list:
        query = 'SELECT * FROM keliones '
        if any([filtras['laukelis'].text() != '' for filtras in filtrai]):

            query += 'WHERE '
            arPirmas = True
            for filtras in filtrai:

                reiksme = filtras['laukelis'].text()

                if reiksme != '': 
                    if arPirmas:
                        query += f"{filtras['stulpelis']} LIKE '%{filtras['laukelis'].text()}%'"
                        arPirmas = False
                    else:
                        query += f" AND {filtras['stulpelis']} LIKE '%{filtras['laukelis'].text()}%'"

        return self.c.execute(query).fetchall()
    
    # Funkcija pasiimti stulpeliu pavadinimus
    def get_columns(self) -> list:
        info = self.c.execute('PRAGMA table_info(keliones)').fetchall()
        columns = [col[1] for col in info]
        return columns

    # Funkcija skirta ištrinti įrašui
    def delete_record(self, id: int=0, delete_all: bool=False) -> None:
        self.c.execute(f"DELETE FROM keliones {f"WHERE id = {id}" if not delete_all else ''}")
        self.conn.commit()

    # Funkcija skirta atnaujinti irasa
    def update_item(self, id:int, column:int, value:str) -> None: 
        print(id, column, value)
        self.c.execute(f"UPDATE keliones SET {column} = '{value}' WHERE id = {id}")
        self.conn.commit()