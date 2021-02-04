from PyQt5 import QtWidgets

import conexion
import var
import events


class Clientes:

    def validardni(dni):
        """

        Modulo que valida la letra de un dni segun sea nacional o extranjero

        :param dni: dni
        :type: String
        :return: None
        :rtype: bool

        Pone la letra en mayúsculas, comprueba que son nueve caracteres. Toma los 8 primeros, si extranjero
        cambia la letra por el número, y aplica el algoritmo de comprobación de la letra basado en la normativa
        Si es correcto devuelve True, si es falso devuelva False

        """
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
        """

        Modulo que según checkemos el rbtbutton Fem o Masc carga el texto correspondiente de Mujer o Hombre a la
        variable var.sex que luego se añade a la lista de los datos del cliente a incluir en la BBDD

        :return: None
        :rtype: None

        """
        try:
            if var.ui.rbtFemenino.isChecked():
                var.sex = 'Mujer'
            if var.ui.rbtMasculino.isChecked():
                var.sex = 'Hombre'
        except Exception as error:
            print('Error:%s' % str(error))

    def selPago(self):
        """

        Cheque que valores de paga seleccion en el checkbos y los añade a una variable lista var.py

        :return: None

        En QtDesigner se debe agrupar los checkbox en un ButtonGroup

        """

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
        """

        Al seleccion una provincia en el combo de provincias llamba al evento cmbProv.activated que devuelve
        la provincia selecccionada

        :param a: provincia seleccionada
        :type a: string
        :return: None
        :rtype: None

        """
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
        """

        Modulo que abre la ventana calendario

        """
        try:
            var.dlgcalendar.show()
        except Exception as error:
            print('Error: %s ' % str(error))

        '''
        Este módulo se ejecuta cuando clickeamos en un día del calendar, es decir, clicked.connect de calendar
        '''

    def cargarFecha(qDate):
        """

        Módulo que carga la fecha marcada en el widget Calendar

        :parama a: librería python para formateo de fehcas
        :return: None
        :rtype: formato de fechas python

        A partir de los eventos Calendar.clicked.connect al clickear en una fecha, captura y la carga el widget edit
        que almacena la fecha

        """
        try:
            data = ('{0}/{1}/{2}'.format(qDate.day(), qDate.month(), qDate.year()))
            var.ui.ltCalendar.setText(str(data))
            var.dlgcalendar.hide()
        except Exception as error:
            print('Error cargar fecha: %s ' % str(error))

    def altaClientes(self):
        """

        Modulo que carga los datos del cliente

        Se crea una lista que contendrá datos del cliente que se introduzcan en los widgets,
        esta lista se pasa como argumento al método cargarCli del módulo conexión.
        El módulo llama a la función limpiarCli que vacía el contenido de los widgets.

        """
        if var.ui.lblValido.text() == 'V':
            var.ui.lblstatus.setText('DNI válido')
            try:

                newcli = []
                tableCli = []
                client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]

                k = 0

                for i in client:
                    newcli.append(i.text())  # cargamos los valores que hay en los editline
                    if k < 3:
                        tableCli.append(i.text())
                        k += 1
                newcli.append(var.ui.cbProvincia.currentText())
                # elimina duplicados
                var.pay = set(var.pay)
                # var.pay2 = Clientes.selPago(self)
                newcli.append(var.sex)
                # newcli.append(var.pay2)
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

            except Exception as error:
                print('Error:%s' % str(error))
        else:
            var.ui.lblstatus.setText('Error al validar DNI')

    def limpiarCli(self):
        """

        Modulo que vacía o limpia los datos del formulario cliente

        :return: None

        En los checkbox y radiobutton los pone a False.

        """
        client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
        try:
            for i in range(len(client)):
                client[i].setText('')
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
        """

        Modulo que vacía o limpia los datos del formulario cliente y la tabla

        :return: None

        En los checkbox y radiobutton los pone a False.

        """
        client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
        try:
            for i in range(len(client)):
                client[i].setText('')
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

    def cargarCliente(self):
        """

        Modulo que se activa con el evento clicked.connec y setSelectionBehavior del widget TtableCli

        :return: None
        :rtype: None

        Al generarse el evento se llama al módulo de Conexion mostrarClientes2 que carga los datos del cliente
        seleccionado haciendo una llamada a la BBDD

        """
        try:
            fila = var.ui.tableCli.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            print(fila)
            var.ui.ltDNI.setText(fila[0])
            var.ui.ltCodCli.setText(fila[0])
            var.ui.ltNombreCli.setText(fila[1])
            conexion.Conexion.mostrarClientes2(self)
            events.Eventos.valido(self)
            var.ui.lblstatus.setText('Cliente cargado')
        except Exception as error:
            print('Error:%s' % str(error))

    def bajaCliente(self):
        """

        Módulo que da de baja un cliente a partir del dni. Además recarga el widget tablaCli con los datos actualizados
        desde la BBDD

        :return: None
        :rtype: None

        Toma el dni cargado en el widget editDni se lo pasa al módulo bajaCli de la clase Conexión y da de bja el cliente.
        Limpia los datos del formulario y recarga tablaCli

        """
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
        """

        Modulo para modificar datos de un cliente con un determinado codigo

        :return: None
        :rtype: None

        A partir del código del cliente , lee los nuevos datos de los widgets que se han
        cargado y modificado , llama al método midifCli de la clase Conexion para actualizar los
        datos en la BBDD pasandole una lista con los nuevos datos.

        """
        try:
            newdata = []
            client = [var.ui.ltDNI, var.ui.ltApellidos, var.ui.ltNombre, var.ui.ltDireccion, var.ui.ltCalendar]
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
        """

        Limpia datos formulario y recarga la tabla de clientes llamando al módulo mostrarClientes de la clase
        Conexion

        :return: None

        """
        try:
            Clientes.limpiarTodo(self)
            conexion.Conexion.mostrarClientes(self)
            var.ui.lblstatus.setText('Datos recargados')
        except Exception as error:
            print('Error al recargar clientes%s' % str(error))

    def buscarCli(self):
        """

        Busca un Cliente a partir de un dni que introduce el usuario

        :return: None
        :rtype: None

        Toma el dni del widget ltDni y llama a la función buscaCli de la clase Conexión a la que le pasa el dni.

        """
        try:
            dni = var.ui.ltDNI.text()
            Clientes.limpiarTodo(self)
            conexion.Conexion.buscaCli(dni)
        except Exception as error:
            print('Error al buscar cliente %s' % str(error))
