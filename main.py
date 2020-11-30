import sys
import clients
import conexion
import events
import var
from datetime import datetime, date
from ventana import *
from ventanaSalir import *
from vencalendar import *
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
import locale

locale.setlocale(locale.LC_ALL, 'es-ES')


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_Proyecto1()
        var.ui.setupUi(self)

        var.ui.centralwidget.show()
        var.avisoSalir = DialogSalir()
        var.dlgcalendar = DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()

        '''Centrar ventana'''
        fg = var.ui.tabWidget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        var.ui.tabWidget.move(fg.topLeft())
        ''''''

        '''coleccion de datos'''
        var.rbtsex = (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago = (var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransfer)

        '''acciones'''
        var.ui.actionSalir_2.triggered.connect(events.Eventos.salir)
        var.ui.btnSalir.clicked.connect(events.Eventos.salir)
        var.ui.toolbarSalir.triggered.connect(events.Eventos.salir)
        var.ui.btnAceptar_2.clicked.connect(events.Eventos.valido)
        var.ui.ltDNI.textEdited.connect(events.Eventos.valido)
        var.ui.btnCalendar.clicked.connect(clients.Clientes.abrirCalendar)
        var.ui.btnAlta.clicked.connect(clients.Clientes.altaClientes)
        var.ui.btnLimpiar.clicked.connect(clients.Clientes.limpiarTodo)
        var.ui.btnEliminar.clicked.connect(clients.Clientes.bajaCliente)
        var.ui.btnModificar.clicked.connect(clients.Clientes.modifCliente)
        var.ui.btnBuscar.clicked.connect(clients.Clientes.buscarCli)
        var.ui.btnRecargar.clicked.connect(clients.Clientes.reloadCli)
        var.ui.toolbarAbrir.triggered.connect(events.Eventos.AbrirDir)
        var.ui.actionAbrir.triggered.connect(events.Eventos.AbrirDir)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCliente)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        conexion.Conexion.db_connect(var.filebd)
        conexion.Conexion.mostrarClientes(self)

        '''Llamada a modulos iniciales'''
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 1)
        var.ui.lblstatus.setText('Bienvenido a 2ºDAM')
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


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
