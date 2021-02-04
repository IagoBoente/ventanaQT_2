import var
import conexion
from PyQt5 import QtWidgets, QtCore
from time import sleep


class Ventas:

    def altaFactura(self):
        """

        Módulo que graba una factura previa al proceso de ventas.

        :return: None
        :rtype: None

        Una vez grabada recarga la tabla Factura
        Y prepara la tabla de Ventas.

        """
        try:
            dni = var.ui.ltCodCli.text()
            fecha = var.ui.ltCalendar_2.text()
            apel = var.ui.ltNombreCli.text()
            if dni != '' and fecha != '':
                conexion.Conexion.altaFac(dni, fecha, apel)
            conexion.Conexion.mostrarFacturas(self)
            conexion.Conexion.cargarFac2(self)
            #Ventas.prepararTablaventas(0)

        except Exception as error:
            print('Error alta factura %s' % str(error))
            return None

    def abrirCalendar(self):
        """

        Abrir la ventana calendario

        """
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

    def cargarFechafac(qDate):
        """

        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked de calendar

        """
        try:
            # if var.ui.tabWidget.currentIndex() == 1:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.ltCalendar_2.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha factura: %s ' % str(error))

    def cargarFact(self):
        """

        Módulo que carga los datos de la factura y cliente al clickear en la tabla Factura

        :return:None
        :type: None

        """
        try:
            var.subfac = 0.00
            var.fac = 0.00
            var.iva = 0.00
            fila = var.ui.tableFac.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codf = fila[0]
            var.ui.lblCodFact.setText(str(codf))
            var.ui.ltCalendar_2.setText(str(fila[1]))
            conexion.Conexion.cargarFac(str(codf))
            var.ui.lblstatus.setText('Factura cargada')
        except Exception as error:
            print('Error cargar Factura: %s ' % str(error))



    def borrarFactura(self):
        """

        Módulo que borra la factura seleccionada

        :return: None
        :rtype: None

        """
        try:
            codfac = var.ui.lblCodFact.text()
            conexion.Conexion.borraFac(self, codfac)
            Ventas.prepararTablaventas(0)
            var.ui.lblstatus.setText('Factura borrada ')
        except Exception as error:
            print('Error Borrar Factura en Cascada: %s ' % str(error))

    def procesoVenta(self):

        """

        Módulo que guarda una venta

        :return: None
        :rtype: None

        """
        try:
            var.subfac = 0.00
            var.venta = []
            codfac = var.ui.lblCodFact.text()
            var.venta.append(int(codfac))
            articulo = var.cmbventa.currentText()
            dato = conexion.Conexion.obtenCodPrec(articulo)
            var.venta.append(int(dato[0]))
            var.venta.append(articulo)
            row = var.ui.tableVenta.currentRow()
            cantidad = var.ui.tableVenta.item(row, 2).text()
            cantidad = cantidad.replace(',', '.')
            var.venta.append(int(cantidad))
            precio = dato[1].replace(',', '.')
            var.venta.append(round(float(precio), 2))
            subtotal = round(float(cantidad) * float(dato[1]), 2)
            var.venta.append(subtotal)
            var.venta.append(row)
            # sleep(1)
            if codfac != '' and articulo != '' and cantidad != '':
                conexion.Conexion.altaVenta(self)
                var.subfac = round(float(subtotal) + float(var.subfac), 2)
                var.ui.lblFactSubtotal.setText(str(var.subfac))
                var.iva = round(float(var.subfac) * 0.21, 2)
                var.ui.lblFactIVA.setText(str(var.iva))
                var.fac = round(float(var.iva) + float(var.subfac), 2)
                var.ui.lblFactTotal.setText(str(var.fac))
                Ventas.mostrarVentasfac(self)
                var.ui.lblstatus.setText('Venta guardada ')
            else:
                var.ui.lblstatus.setText('Faltan Datos de la Factura')

        except Exception as error:
            print('Error proceso venta: %s ' % str(error))

    def prepararTablaventas(index):
        """

        Modulo que prepara tabla Ventas

        :param: index fila de la tabla
        :type: int
        :return: None
        :type: None

        Carga un combo en la tabla Ventas con los datos del producto e inserta nueva fila en la tabal

        """
        try:
            var.cmbventa = QtWidgets.QComboBox()
            conexion.Conexion.cargarCmbventa(var.cmbventa)
            var.ui.tableVenta.setRowCount(index + 1)
            var.ui.tableVenta.setItem(index, 0, QtWidgets.QTableWidgetItem())
            var.ui.tableVenta.setCellWidget(index, 1, var.cmbventa)
            var.ui.tableVenta.setItem(index, 2, QtWidgets.QTableWidgetItem())
            var.ui.tableVenta.setItem(index, 3, QtWidgets.QTableWidgetItem())
            var.ui.tableVenta.setItem(index, 4, QtWidgets.QTableWidgetItem())
        except Exception as error:
            print('Error Preparar tabla de ventas: %s ' % str(error))

    def mostrarVentasfac(self):
        """

        Módulo que muestra las ventas de cada factura

        :return: None
        :rtype: None

        """
        try:
            var.cmbventa = QtWidgets.QComboBox()
            codfac = var.ui.lblCodFact.text()
            conexion.Conexion.listadoVentasfac(codfac)
            conexion.Conexion.cargarCmbventa(var.cmbventa)
        except Exception as error:
            print('Error proceso mostrar ventas por factura: %s' % str(error))

    def anularVenta(self):
        """

        Módulo que anula el proceso de venta

        :return: None
        :rtype: None

        """
        try:
            fila = var.ui.tableVenta.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            codventa = int(fila[0])
            conexion.Conexion.anulaVenta(codventa)
            Ventas.mostrarVentasfac(self)
            var.ui.lblstatus.setText('Venta  anulada ')

        except Exception as error:
            print('Error proceso anular venta de una factura: %s' % str(error))
