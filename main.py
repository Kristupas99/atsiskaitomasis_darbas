from designer import Ui_MainWindow
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

class Window(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print("Veikia")
    

app = QApplication([])
window = Window()
window.show()
app.exec()