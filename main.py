import sys

import clients
import events
import var
from ventana import *


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_Proyecto1()
        var.ui.setupUi(self)
        '''coleccion de datos'''
        var.rbtsex =(var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago = (var.ui.chkEfectivo, var.ui.chkTransfer, var.ui.chkTarjeta)

        '''acciones'''
        var.ui.actionSalir_2.triggered.connect(events.Eventos.salir)
        var.ui.btnAceptar.clicked.connect(events.Eventos.saludo)
        var.ui.btnSalir.clicked.connect(events.Eventos.salir)
        var.ui.btnAceptar_2.clicked.connect(events.Eventos.valido)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cbProvincia.activated[str].connect(clients.Clientes.selProv)

        '''Llamada a modulos iniciales'''
        events.Eventos.cargarProv(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    sys.exit(app.exec())
