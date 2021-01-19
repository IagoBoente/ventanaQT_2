from PyQt5 import QtWidgets

import conexion
import var
import events


class Facturacion:

    def abrirCalendar(self):
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

        '''
        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
        '''

    def cargarFecha(qDate):
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.ltCalendar_2.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def selArticulo(art):
        try:
            global varticulo
            varticulo = art
            '''return prov'''
        except Exception as error:
            print('Error:%s' % str(error))

    def altaFacturacion(self):
        if var.ui.lblValido.text() == 'V':
            var.ui.lblstatus.setText('DNI válido')
            try:

                newcli = []
                tableCli = []  # sera lo que cargamos en la table
                factura = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]

                k = 0

                for i in factura:
                    newcli.append(i.text())  # cargamos los valores que hay en los editline
                    if k < 3:
                        tableCli.append(i.text())
                        k += 1
                newcli.append(var.ui.cbProvincia.currentText())
                # elimina duplicados
                var.pay = set(var.pay)
                # var.pay2 = Facturacion.selPago(self)
                newcli.append(var.sex)
                # newcli.append(var.pay2)
                newcli.append(var.pay)
                newcli.append(var.ui.spinEdad.value())
                if factura:
                    row = 0  # posicion de la fila, problrma: coloca al ultimo como primero en cada click
                    column = 0  # posicion de la columna
                    var.ui.tableCli.insertRow(row)  # insertamos una fila nueva con cada click de boton
                    for registro in tableCli:
                        cell = QtWidgets.QTableWidgetItem(registro)
                        var.ui.tableCli.setItem(row, column, cell)
                        column += 1
                    conexion.Conexion.cargarCli(newcli)

                else:
                    print('Faltan datos')
                    Facturacion.limpiarFact(self)

            except Exception as error:
                print('Error:%s' % str(error))
        else:
            var.ui.lblstatus.setText('Error al validar DNI')

    def limpiarFact(self):
        factura = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
        try:
            for i in range(len(factura)):
                factura[i].setText('')
            # var.ui.grpbtnSex.setExclusive(False)
            var.ui.rbtFemenino.setChecked(True)
            var.ui.rbtMasculino.setChecked(False)
            var.ui.grpbtnPay.setExclusive(False)
            for dato in var.rbtsex:
                dato.setChecked(False)
            for datos in var.chkpago:
                datos.setChecked(False)
            var.ui.cbProvincia.setCurrentIndex(0)
            var.ui.lblValido.setText('')
            var.ui.lblstatus.setText('')
            var.ui.lblCodcli.setText('')
            var.ui.spinEdad.setValue(0)

            # var.ui.tableCli.removeRow(0)

        except Exception as error:
            print('Error:%s' % str(error))

    def limpiarTodo(self):
        factura = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
        try:
            for i in range(len(factura)):
                factura[i].setText('')
            # var.ui.grpbtnSex.setExclusive(False)
            var.ui.rbtFemenino.setChecked(True)
            var.ui.rbtMasculino.setChecked(False)
            var.ui.grpbtnPay.setExclusive(False)
            for dato in var.rbtsex:
                dato.setChecked(False)
            for datos in var.chkpago:
                datos.setChecked(False)
            var.ui.cbProvincia.setCurrentIndex(0)
            var.ui.lblValido.setText('')
            var.ui.lblstatus.setText('')
            var.ui.lblCodcli.setText('')
            var.ui.spinEdad.setValue(0)
            var.ui.tableCli.setRowCount(0)

        except Exception as error:
            print('Error:%s' % str(error))

    def cargarfacturas(self):
        try:
            fila = var.ui.tableCli.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            print(fila)
            var.ui.ltDNI.setText(fila[0])
            conexion.Conexion.mostrarFacturacion2(self)
            events.Eventos.valido(self)
            var.ui.lblstatus.setText('facturas cargado')
        except Exception as error:
            print('Error:%s' % str(error))

    def bajafacturas(self):
        dni = var.ui.ltDNI.text()
        try:
            if len(dni) > 0:
                aviso = events.Eventos.avisoAccion(self)
                if aviso:
                    conexion.Conexion.bajaCli(dni)
                    Facturacion.limpiarTodo(self)
                    var.ui.lblstatus.setText('facturas con dni: ' + dni + ' dado de baja')
                    conexion.Conexion.mostrarFacturacion(self)
                else:
                    var.ui.lblstatus.setText('Eliminar facturas CANCELADO')
            else:
                var.ui.lblstatus.setText('facturas inexistente')
        except Exception as error:
            print('Error:%s' % str(error))

    def modiffacturas(self):
        try:
            newdata = []
            factura = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
            for i in factura:
                newdata.append(i.text())
            newdata.append(var.ui.cbProvincia.currentText())
            newdata.append(var.sex)
            newdata.append(var.pay)
            newdata.append(var.ui.spinEdad.value())
            cod = var.ui.lblCodcli.text()
            conexion.Conexion.modifCli(cod, newdata)
            conexion.Conexion.mostrarFacturacion(self)
        except Exception as error:
            print('Error al cargar Facturacion:%s' % str(error))

    def reloadCli(self):
        try:
            Facturacion.limpiarTodo(self)
            conexion.Conexion.mostrarFacturacion(self)
            var.ui.lblstatus.setText('Datos recargados')
        except Exception as error:
            print('Error al recargar Facturacion%s' % str(error))

    def buscarCli(self):
        try:
            dni = var.ui.ltDNI.text()
            Facturacion.limpiarTodo(self)
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error al buscar facturas %s' % str(error))

    def borrarFactura(self):
        try:
            codfac = var.ui.lblNumFact.text()
            conexion.Conexion.borraFact(codfac)
        except Exception as error:
            print('Error borrar factura en cascada: %s' % str(error))
