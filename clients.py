from PyQt5 import QtWidgets

import conexion
import var
import events


class Clientes:

    def validardni(dni):
        try:
            table = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and table[int(dni) % 23] == dig_control
            return False
        except:
            print("error en la app")
            return None

    def selSexo(self):
        try:
            if var.ui.rbtFemenino.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbtMasculino.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error:%s' % str(error))

    def selPago(self):
        try:
            var.pay = []
            for i, data in enumerate(var.ui.grpbtnPay.buttons()):
                if data.isChecked() and i == 0:
                    var.pay.append('Efectivo')
                if data.isChecked() and i == 1:
                    var.pay.append('Tarjeta')
                if data.isChecked() and i == 2:
                    var.pay.append('Transferencia')
            return var.pay
        except Exception as error:
            print('Error:%s' % str(error))

    def selProv(prov):
        try:
            global vpro
            vpro = prov
            '''return prov'''
        except Exception as error:
            print('Error:%s' % str(error))

        '''
        Abrir la ventana calendario
        '''

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
            var.ui.ltCalendar.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altaClientes(self):
        if var.ui.lblValido.text() == 'V':
            var.ui.lblstatus.setText('DNI válido')
            try:

                newcli = []
                tableCli = []  # sera lo que cargamos en la table
                client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion,var.ui.ltCalendar]

                k = 0

                for i in client:
                    newcli.append(i.text())  # cargamos los valores que hay en los editline
                    if k < 3:
                        tableCli.append(i.text())
                        k += 1
                newcli.append(var.ui.cbProvincia.currentText())
                # elimina duplicados
                var.pay = set(var.pay)
                #var.pay2 = Clientes.selPago(self)
                newcli.append(var.sex)
                #newcli.append(var.pay2)
                newcli.append(var.pay)
                newcli.append(var.ui.spinEdad.value())
                if client:
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
                    Clientes.limpiarCli(self)

                '''
                for j in var.pay:
                    newcli.append(j)
                newcli.append(var.sex)
                print(newcli)
                print(tableCli)
                # aqui empieza como trabajar con la TableWidget
                row = 0  # posicion de la fila, problrma: coloca al ultimo como primero en cada click
                column = 0  # posicion de la columna
                var.ui.tableCli.insertRow(row)  # insertamos una fila nueva con cada click de boton
                for registro in tableCli:
                    cell = QtWidgets.QTableWidgetItem(registro)
                    var.ui.tableCli.setItem(row, column, cell)
                    column += 1
                '''
            except Exception as error:
                print('Error:%s' % str(error))
        else:
            var.ui.lblstatus.setText('Error al validar DNI')

    def limpiarCli(self):
        client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
        try:
            for i in range(len(client)):
                client[i].setText('')
            #var.ui.grpbtnSex.setExclusive(False)
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

            #var.ui.tableCli.removeRow(0)

        except Exception as error:
            print('Error:%s' % str(error))

    def limpiarTodo(self):
        client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
        try:
            for i in range(len(client)):
                client[i].setText('')
            #var.ui.grpbtnSex.setExclusive(False)
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

    def cargarCliente(self):
        try:
            fila = var.ui.tableCli.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            print(fila)
            var.ui.ltDNI.setText(fila[0])
            conexion.Conexion.mostrarClientes2(self)
            events.Eventos.valido(self)
        except Exception as error:
            print('Error:%s' % str(error))

    def bajaCliente(self):
        dni = var.ui.ltDNI.text()
        try:
            if len(dni) > 0:
                aviso = events.Eventos.avisoAccion(self)
                if aviso:
                    conexion.Conexion.bajaCli(dni)
                    Clientes.limpiarTodo(self)
                    var.ui.lblstatus.setText('Cliente con dni: ' + dni + ' dado de baja')
                    conexion.Conexion.mostrarClientes(self)
                else:
                    var.ui.lblstatus.setText('Eliminar cliente CANCELADO')
            else:
                var.ui.lblstatus.setText('Cliente inexistente')
        except Exception as error:
            print('Error:%s' % str(error))

    def modifCliente(self):
        try:
            newdata = []
            client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre,  var.ui.ltDireccion,var.ui.ltCalendar]
            for i in client:
                newdata.append(i.text())
            newdata.append(var.ui.cbProvincia.currentText())
            newdata.append(var.sex)
            newdata.append(var.pay)
            newdata.append(var.ui.spinEdad.value())
            cod = var.ui.lblCodcli.text()
            conexion.Conexion.modifCli(cod, newdata)
            conexion.Conexion.mostrarClientes(self)
        except Exception as error:
            print('Error al cargar clientes:%s' % str(error))

    def reloadCli(self):
        try:
            Clientes.limpiarTodo(self)
            conexion.Conexion.mostrarClientes(self)
            var.ui.lblstatus.setText('Datos recargados')
        except Exception as error:
            print('Error al recargar clientes%s' % str(error))

    def buscarCli(self):
        try:
            dni = var.ui.ltDNI.text()
            Clientes.limpiarTodo(self)
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error al buscar cliente %s' % str(error))