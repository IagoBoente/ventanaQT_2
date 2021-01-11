import sys
import clients
import conexion
import events
import productos
import var
from datetime import datetime, date
from ventana import *
from ventanaSalir import *
from ventanaAviso import *
from ventanaAbout import *
from vencalendar import *
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
        var.avisoAccion = DialogAccion()
        var.mensAbout = DialogAbout()
        var.dlgcalendar = DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()

        '''Centrar ventana'''
        fg = var.ui.tabWidget.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        tp = QDesktopWidget().availableGeometry().top()
        fg.moveCenter(cp)
        fg.moveTop(tp + 50)
        var.ui.tabWidget.move(fg.topLeft())
        ''''''

        '''coleccion de datos'''
        var.rbtsex = (var.ui.rbtFemenino, var.ui.rbtMasculino)
        var.chkpago = (var.ui.chkEfectivo, var.ui.chkTarjeta, var.ui.chkTransfer)

        '''acciones'''
        var.ui.actionSalir_2.triggered.connect(events.Eventos.salir)
        var.ui.btnSalir.clicked.connect(events.Eventos.salir)
        var.ui.toolbarSalir.triggered.connect(events.Eventos.salir)
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

        '''acciones_2'''
        var.ui.btnAlta_2.clicked.connect(productos.Productos.altaProductos)
        var.ui.btnEliminar_2.clicked.connect(productos.Productos.bajaproductos)
        var.ui.btnLimpiar_2.clicked.connect(productos.Productos.limpiarTodo)
        var.ui.btnSalir_2.clicked.connect(events.Eventos.salir)
        var.ui.btnRecargar_2.clicked.connect(productos.Productos.reloadPro)
        var.ui.btnModificar_2.clicked.connect(productos.Productos.modifproductos)
        var.ui.actionAbout.triggered.connect(events.Eventos.avisoAbout)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCliente)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tablePro.clicked.connect(productos.Productos.cargarproductos)
        var.ui.tablePro.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        conexion.Conexion.db_connect(var.filebd)
        conexion.Conexion.mostrarClientes(self)
        conexion.Conexion.mostrarProductos(self)

        '''Llamada a modulos iniciales'''
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 20)
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus_2, 1)
        var.ui.lblstatus.setText('Bienvenido a 2ºDAM')

        events.Eventos.MostrarFecha(self)
        events.Eventos.cargarProv(self)

    def closeEvent(self, event):
        events.Eventos.salir(event)


class DialogSalir(QtWidgets.QDialog):
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.avisoSalir = Ui_btnBox()
        var.avisoSalir.setupUi(self)
        var.avisoSalir.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.salir)


class DialogAccion(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAccion, self).__init__()
        var.avisoAccion = Ui_btnBoxAccion()
        var.avisoAccion.setupUi(self)
        var.avisoAccion.buttonBoxAccion.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            events.Eventos.avisoAccion)


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


class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        super(DialogAbout, self).__init__()
        var.mensAbout = Ui_btnBoxAbout()
        var.mensAbout.setupUi(self)
        var.mensAbout.buttonBoxAbout.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(events.Eventos.avisoAbout)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
