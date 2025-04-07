from designer import Ui_MainWindow
from database.db_class import Db

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton



class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.db = Db()
        self.db.create_database()
        self.columns = self.db.get_columns()
        self.cell_editable = False
        
        self.filtrai = [
            {'laukelis': self.filterby_vardas, 'stulpelis': 'vardas'}, 
            {'laukelis': self.filterby_isvykimovieta, 'stulpelis': 'isvykimo_vieta'}, 
            {'laukelis': self.filterby_atvykimovieta, 'stulpelis': 'atvykimo_vieta'}, 
        ]

        for filtras in self.filtrai:
            filtras['laukelis'].textChanged.connect(self.set_items)

        self.delete_all.clicked.connect(lambda: self.function_with_item_refresh())
        self.delete_all.clicked.connect(self.delete_all_action)
        self.add_new.clicked.connect(self.validate_inputs)
        self.all_travels.cellDoubleClicked.connect(self.is_cell_editable)
        self.all_travels.cellChanged.connect(self.update_item_value)
        self.clear_filters.clicked.connect(self.clear_filters_action)

        self.set_items()


    # Istrinami visi irasai
    def delete_all_action(self):
        self.db.delete_record(delete_all=True)
        self.set_items()
    
    # Isvalomi filtru laukeliai
    def clear_filters_action(self) -> None:
        for filtras in self.filtrai:
            filtras['laukelis'].setText('')

    # Nustatoma ar laukelis redaguojamas
    def is_cell_editable(self) -> None:
        self.cell_editable = True
    
    # Paruosiama informacija duomenu bazes klases metodui
    def update_item_value(self, row:int, col:int) -> None:
        if not self.cell_editable:
            return

        if self.all_travels.currentItem().text() == '':
            
            return 

        id = self.data[row][0]
        column_name = self.columns[col + 1]
        value = self.all_travels.currentItem().text()

        self.db.update_item(id, column_name, value)

        self.cell_editable = False
    
    # Patikrinama ar pagrindines formos duomenys teisingai uzpildyti
    def validate_inputs(self) -> None:
        data = self.get_values()
        errors = ''
        valid = True
        for key, value in data.items():
            if value == '':
                errors += f"Uzpildykite laukeli: {key.replace('_', ' ')}\n"
                valid = False
        
        if valid:
            for key, value in data.items():
                if key == 'tel_nr':
                    if any([letter.isalpha() for letter in value]):
                        errors += f"Laukelis netinkamo formato: tel. nr.\n"
                        valid = False

                if key == 'el_pastas':
                    if '@' not in value:
                        errors += f"Laukelis netinkamo formato: el. pastas\n"
                        valid = False

        if not valid:
            self.message.setText(errors)
            return
        
        if not valid:
            self.message.setText(errors)
            return

        self.db.add_new_record(data)
        self.reset_form()
        self.set_items()

    # Funkcija skirta gauti pagrindines formos reiksmes
    def get_values(self) -> dict:
        vardas = self.new_vardas.text()
        pavarde = self.new_pavarde.text()
        el_pastas = self.new_elpastas.text()
        tel_nr = self.new_telnr.text()
        isvykimo_vieta = self.new_isvykimovieta.text()
        atvykimo_vieta = self.new_atvykimovieta.text()

        return {
            "vardas":vardas,
            "pavarde":pavarde,
            "el_pastas":el_pastas,
            "tel_nr":tel_nr,
            "isvykimo_vieta":isvykimo_vieta,
            "atvykimo_vieta":atvykimo_vieta,
        }
    
    # Funkcija skirta atsatyti pagrindine forma i pradine busena
    def reset_form(self) -> None:
        self.new_vardas.setText('')
        self.new_pavarde.setText('')
        self.new_elpastas.setText('')
        self.new_telnr.setText('')
        self.new_isvykimovieta.setText('')
        self.new_atvykimovieta.setText('')
        self.message.setText('')

    # Funkcija skirta atvaizduoti duomenis lenteleje
    def set_items(self) -> None:
        self.data = self.db.get_records(self.filtrai)
        self.all_travels.setRowCount(len(self.data))
        if len(self.data) == 0:
            return
        for row_id, row_values in enumerate(self.data):
            for column_id, record in enumerate(row_values):
                item = QTableWidgetItem(record)
                self.all_travels.setItem(row_id, column_id-1, item)

            btn = QPushButton()
            self.all_travels.setCellWidget(row_id, 7, btn)
            btn.setText("Ištrinti")
            btn.clicked.connect(lambda checked, rid=row_values[0]: self.delete_action(rid))

            
    # Funkcija skirta paruosti duomenis duomenu bazes klases istrinimo metodui
    def delete_action(self, id:int) -> None:
        self.db.delete_record(id)
        self.set_items()


# Aplikacijos paleidimas
app = QApplication([])
window = Window()
window.show()
app.exec()