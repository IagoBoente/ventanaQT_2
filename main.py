import sys
import events
import var
from ventana import *


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_Proyecto1()
        var.ui.setupUi(self)
        var.ui.actionSalir_2.triggered.connect(events.Eventos.salir)
        var.ui.btnAceptar.clicked.connect(events.Eventos.saludo)
        var.ui.btnSalir.clicked.connect(events.Eventos.salir)
        var.ui.btnAceptar_2.clicked.connect(events.Eventos.valido)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
