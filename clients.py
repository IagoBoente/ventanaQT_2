from PyQt5 import QtWidgets

import var


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
            if var.ui.chkEfectivo.isChecked():
                var.pay.append('Efectivo')
            if var.ui.chkTarjeta.isChecked():
                var.pay.append('Tarjeta')
            if var.ui.chkTransfer.isChecked():
                var.pay.append('Transferencia')
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

    def showClientes(self):
        try:
            '''cargar clientes de la table
                :return: none
            '''
            '''preparamos el registro'''
            newcli = []
            tableCli = []  # sera lo que cargamos en la table
            client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltCalendar, var.ui.ltDireccion]
            k = 0

            for i in client:
                newcli.append(i.text())  # cargamos los valores que hay en los editline
                if k < 3:
                    tableCli.append(i.text())
                    k += 1
            newcli.append(vpro)
            # elimina duplicados
            var.pay = set(var.pay)

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


        except Exception as error:
            print('Error:%s' % str(error))

    def limpiarCli(listaeditCli, listaRbtsex, listaChkpay):
        try:
            for i in range(len(listaeditCli)):
                listaeditCli[i].setText('')
            var.ui.grpbtnSex.setExclusive(False)
            for dato in listaRbtsex:
                dato.setChecked(False)
            for data in listaChkpay:
                data.setChecked(False)
            var.ui.cbProvincia.setCurrentIndex(0)
            var.ui.lblValido.setText('')

        except Exception as error:
            print('Error:%s' % str(error))

    def cargarCliente(self):
        try:
            fila = var.ui.tableCli.selectedItems()
            client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre]
            if fila:
                fila = [dato.text() for dato in fila]
            print(fila)
            i = 0
            for i, dato in enumerate(client):
                dato.setText(fila[i])
        except Exception as error:
            print('Error:%s' % str(error))
