import sys
import clients
import conexion
import events
import var
from datetime import datetime
from ventana import *
from ventanaSalir import *
from vencalendar import *


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_Proyecto1()
        var.ui.setupUi(self)
        var.ui.centralwidget.show()
        var.avisoSalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()

        '''coleccion de datos'''
        var.rbtsex = (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago = (var.ui.chkEfectivo, var.ui.chkTransfer, var.ui.chkTarjeta)

        '''acciones'''
        var.ui.actionSalir_2.triggered.connect(events.Eventos.salir)
        var.ui.btnAceptar.clicked.connect(events.Eventos.saludo)
        var.ui.btnSalir.clicked.connect(events.Eventos.salir)
        var.ui.btnAceptar_2.clicked.connect(events.Eventos.valido)
        var.ui.btnAceptar_2.clicked.connect(clients.Clientes.showClientes)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCliente)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        conexion.Conexion.db_connect(var.filebd)

        '''Llamada a modulos iniciales'''
        events.Eventos.cargarProv(self)

    def closeEvent(self, event):
        events.Eventos.salir(event)


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.avisoSalir = Ui_btnBox()
        var.avisoSalir.setupUi(self)
        var.avisoSalir.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.salir)


class DialogCalendar(QtWidgets.QDialog):
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_calendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.calendar_2.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.calendar_2.clicked.connect(clients.Clientes.cargarFecha)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.show()
    '''window.showFullScreen()'''
    sys.exit(app.exec())
