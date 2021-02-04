import sys
import clients
import conexion
import events
import productos
import var
import printer
import ventas
from datetime import datetime, date
from ventana import *
from ventanaSalir import *
from ventanaAviso import *
from ventanaAbout import *
from vencalendar import *
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from PyQt5 import QtPrintSupport
import locale

locale.setlocale(locale.LC_ALL, 'es-ES')


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        """

        Clase que instancia todas las ventanas del programa .
        Genera y conecta todos los eventos de los botones , tablas y otros widgets.
        Cuendo se lanza se conecta con la base de datos.
        Carga todos los articulos , facturas y clientes de la BBDD en las ventanas
        correspondientes.

        """

        super(Main, self).__init__()
        '''
        
        
        
        '''
        var.ui = Ui_Proyecto1()
        var.ui.setupUi(self)

        var.ui.centralwidget.show()
        var.avisoSalir = DialogSalir()
        var.avisoAccion = DialogAccion()
        var.mensAbout = DialogAbout()
        var.dlgcalendar = DialogCalendar()
        var.filedlgabrir = FileDialogAbrir()
        var.dlgImprimir = PrintDialogAbrir()
        var.cmbventa = QtWidgets.QComboBox()

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

        '''acciones_Clientes-Eventos'''
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
        var.ui.toolbarBackup.triggered.connect(events.Eventos.Backup)
        var.ui.toolbarImprimir.triggered.connect(events.Eventos.AbrirPrinter)
        var.ui.toolbarRestaurar.triggered.connect(events.Eventos.restaurarBD)

        '''acciones_Productos'''
        var.ui.btnAlta_2.clicked.connect(productos.Productos.altaProductos)
        var.ui.btnEliminar_2.clicked.connect(productos.Productos.bajaproductos)
        var.ui.btnLimpiar_2.clicked.connect(productos.Productos.limpiarTodo)
        var.ui.btnSalir_2.clicked.connect(events.Eventos.salir)
        var.ui.btnRecargar_2.clicked.connect(productos.Productos.reloadPro)
        var.ui.btnModificar_2.clicked.connect(productos.Productos.modifproductos)
        var.ui.actionAbout.triggered.connect(events.Eventos.avisoAbout)

        'acciones_Informes'
        var.ui.btnInformeCli.clicked.connect(printer.Printer.reportCli)
        var.ui.actionClientes.triggered.connect(printer.Printer.reportCli)
        var.ui.actionProductos.triggered.connect(printer.Printer.reportPro)
        var.ui.btnInformePro.clicked.connect(printer.Printer.reportPro)
        var.ui.btnInformeFac.clicked.connect(printer.Printer.reportFac)

        'acciones_Facturas'
        var.ui.btnFacturar.clicked.connect(ventas.Ventas.altaFactura)
        var.ui.btnBuscar_2.clicked.connect(conexion.Conexion.mostrarFacturascli)
        var.ui.btnRecargar_3.clicked.connect(conexion.Conexion.mostrarFacturas)
        var.ui.btnCalendar_2.clicked.connect(ventas.Ventas.abrirCalendar)
        var.ui.btnAnular.clicked.connect(ventas.Ventas.borrarFactura)
        var.ui.btnConfirmar.clicked.connect(ventas.Ventas.procesoVenta)
        var.ui.btnCancelar.clicked.connect(ventas.Ventas.anularVenta)

        # events.Eventos.cargarArt(self)

        for i in var.rbtsex:
            i.toggled.connect(clients.Clientes.selSexo)
        for i in var.chkpago:
            i.stateChanged.connect(clients.Clientes.selPago)
        var.ui.cbProvincia.activated[str].connect(clients.Clientes.selProv)
        var.ui.tableCli.clicked.connect(clients.Clientes.cargarCliente)
        var.ui.tableCli.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tablePro.clicked.connect(productos.Productos.cargarproductos)
        var.ui.tablePro.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tableFac.clicked.connect(ventas.Ventas.cargarFact)
        var.ui.tableFac.clicked.connect(ventas.Ventas.mostrarVentasfac)
        var.ui.tableFac.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        var.ui.tableVenta.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)

        conexion.Conexion.db_connect(var.filebd)
        conexion.Conexion.mostrarClientes(self)
        conexion.Conexion.mostrarProductos(self)
        conexion.Conexion.mostrarFacturas(self)
        var.cmbventa = QtWidgets.QComboBox()
        conexion.Conexion.cargarCmbventa(CmbVenta)
        var.ui.tabWidget.setCurrentIndex(0)

        '''Llamada a modulos iniciales'''
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus, 20)
        var.ui.statusbar.addPermanentWidget(var.ui.lblstatus_2, 1)
        var.ui.lblstatus.setText('Bienvenido a 2ºDAM')

        events.Eventos.MostrarFecha(self)
        events.Eventos.cargarProv(self)

    def closeEvent(self, event):
        events.Eventos.salir(event)


class DialogSalir(QtWidgets.QDialog):
    """

    Clase que instancia la ventana de aviso al salir

    """
    def __init__(self):
        super(DialogSalir, self).__init__()
        var.avisoSalir = Ui_btnBox()
        var.avisoSalir.setupUi(self)
        var.avisoSalir.buttonBox.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(events.Eventos.salir)


class DialogAccion(QtWidgets.QDialog):
    """

    Clase que instancia la ventana de aviso de accion

    """
    def __init__(self):
        super(DialogAccion, self).__init__()
        var.avisoAccion = Ui_btnBoxAccion()
        var.avisoAccion.setupUi(self)
        var.avisoAccion.buttonBoxAccion.button(QtWidgets.QDialogButtonBox.Yes).clicked.connect(
            events.Eventos.avisoAccion)


class DialogCalendar(QtWidgets.QDialog):
    """

    Clase que instancia la ventana del calendario

    """
    def __init__(self):
        super(DialogCalendar, self).__init__()
        var.dlgcalendar = Ui_calendar()
        var.dlgcalendar.setupUi(self)
        diaactual = datetime.now().day
        mesactual = datetime.now().month
        anoactual = datetime.now().year
        var.dlgcalendar.calendar_2.setSelectedDate((QtCore.QDate(anoactual, mesactual, diaactual)))
        var.dlgcalendar.calendar_2.clicked.connect(clients.Clientes.cargarFecha)
        var.dlgcalendar.calendar_2.clicked.connect(ventas.Ventas.cargarFechafac)

class DialogAbout(QtWidgets.QDialog):
    def __init__(self):
        """

        Clase que instancia la ventana about

        """
        super(DialogAbout, self).__init__()
        var.mensAbout = Ui_btnBoxAbout()
        var.mensAbout.setupUi(self)
        var.mensAbout.buttonBoxAbout.button(QtWidgets.QDialogButtonBox.Close).clicked.connect(events.Eventos.avisoAbout)


class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de direcotrio

        """
        super(FileDialogAbrir, self).__init__()


class PrintDialogAbrir(QtPrintSupport.QPrintDialog):
    def __init__(self):
        """

        Clase que instancia la ventana de impresión

        """
        super(PrintDialogAbrir, self).__init__()


class CmbVenta(QtWidgets.QComboBox):
    def __init__(self):
        """

        Clase que instancia el combo de artículos

        """
        super(CmbVenta, self).__init__()
        var.cmbventa = QtWidgets.QComboBox()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
