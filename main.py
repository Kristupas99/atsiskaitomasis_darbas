from designer import Ui_MainWindow
from database.db_class import Db

from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton



class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        

        self.db = Db()
        self.db.create_database()
        self.set_items()
        self.columns = self.db.get_columns()
        self.cell_editable = False
        self.add_new.clicked.connect(self.validate_inputs)


        self.all_travels.cellDoubleClicked.connect(self.is_cell_editable)


    
        self.all_travels.cellChanged.connect(self.update_item_value)


    def is_cell_editable(self):
        print('DOUBLE CLICKED')
        self.cell_editable = True
    

    def update_item_value(self, row, col):
        if not self.cell_editable:
            return

        if self.all_travels.currentItem().text() == '':
            print("Tuscias")
            return 

        id = self.data[row][0]
        column_name = self.columns[col + 1]
        value = self.all_travels.currentItem().text()

        self.db.update_item(id, column_name, value)
        # self.set_items()
        self.cell_editable = False
    

    
    def validate_inputs(self):
        data = self.get_values()
        errors = ''
        valid = True
        for key, value in data.items():
            if value == '':
                errors += f"Uzpildykite laukeli: {key.replace('_', ' ')}\n"
                valid = False

        if not valid:
            self.message.setText(errors)
            return

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


        self.db.add_new_record(data)
        self.reset_form()
        self.set_items()


    def get_values(self):
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
    

    def reset_form(self):
        self.new_vardas.setText('')
        self.new_pavarde.setText('')
        self.new_elpastas.setText('')
        self.new_telnr.setText('')
        self.new_isvykimovieta.setText('')
        self.new_atvykimovieta.setText('')
        self.message.setText('')

    def set_items(self):
        self.data = self.db.get_records()
        
        self.all_travels.setRowCount(len(self.data))
        for row_id, row_values in enumerate(self.data):
            for column_id, record in enumerate(row_values):
                item = QTableWidgetItem(record)
                self.all_travels.setItem(row_id, column_id-1, item)
                # item.setText(str(record))
            
            btn = QPushButton()
            self.all_travels.setCellWidget(row_id, 7, btn)
            btn.setText("Ištrinti")
            btn.clicked.connect(lambda checked, rid=row_values[0]: self.delete_action(rid))

            
        
    def delete_action(self, id):
        self.db.delete_record(id)
        self.set_items()



app = QApplication([])
window = Window()
window.show()
app.exec()