from builtins import str

from PyQt5 import QtWidgets, QtSql

import clients
import var
import ventas


class Conexion():
    def db_connect(filename):
        """

        Módulo que realiza la conexión de la aplicación con la BBDD

        :param filename: nombre de la BBDD
        :type: string
        :return: True o False
        :rtype: bool

        Utiliza la librería de QtSql y el gestor de la BBDD es QSQlite. En caso de error muestra pantalla
        de aviso.

        """
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la BBDD', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexion Establecida')
        return True

    def cargarCli(cliente):
        """

        Da de alta un cliente cuyos datos se pasan por una lista.
        Muestra mensaje de resultado en el barra de estado.
        Recarga la tabla actualizada de clientes

        :param: cliente
        :type: lista
        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into clientes (dni, apellidos, nombre , fechalta,direccion, provincia, sexo , formaspago , edad)'
            'VALUES (:dni, :apellidos, :nombre,:fechalta, :direccion, :provincia, :sexo, :formaspago, :edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':fechalta', str(cliente[3]))
        query.bindValue(':direccion', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':formaspago', str(cliente[7]))
        query.bindValue(':edad', cliente[8])

        var.ui.tableCli.setRowCount(1)

        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Cliente con dni ' + cliente[0] + ' dado de alta')
        else:
            print("Error: ", query.lastError().text())
            var.ui.lblstatus.setText(
                'Inserción fallida, pruebe a introducir datos de nuevo comprobando que el DNI no sea repetido.')

        Conexion.mostrarClientes(None)

    def mostrarClientes(self):
        '''

        Módulo que carga los datos del cliente en la tabla Clientes

        :return: None
        :rtype: None

        '''
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos, nombre from clientes')
        if query.exec_():
            while query.next():
                dni = query.value(0)
                apellidos = query.value(1)
                nombre = query.value(2)
                var.ui.tableCli.setRowCount(index + 1)
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                index += 1
        else:
            print("Error mostrar clientes:", query.lastError().text())

    def mostrarClientes2(self):
        """

        Módulo que carga los datos del cliente seleccionado en la tabla Clientes

        :return: None
        :rtype: None

        """
        dni = var.ui.ltDNI.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni =:dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.ltDNI.setText(str(query.value(1)))
                var.ui.ltApellidos.setText(str(query.value(2)))
                var.ui.ltNombre.setText(str(query.value(3)))
                var.ui.ltCalendar.setText(str(query.value(4)))
                var.ui.ltDireccion.setText(str(query.value(5)))
                var.ui.cbProvincia.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFemenino.setChecked(True)
                    var.ui.rbtMasculino.setChecked(False)
                else:
                    var.ui.rbtMasculino.setChecked(True)
                    var.ui.rbtFemenino.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(query.value(9))

    def bajaCli(dni):
        """'

        Módulo para eliminar cliente.

        :param dni
        :type: string
        :return None
        :rtype None

        Se pasa como argumento el dni del cliente a eliminar.
        A continuación recarga la tablaCli actualizada
        Muestra mensje resultado en la barra de estado

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print(("Error mostrar clientes:", query.lastError().text()))

    def modifCli(codigo, newdata):
        """

        Módulo que actualiza datos de cliente

        :param codigo: código cliente
        :type codigo: int
        :param newdata: datos cliente
        :type newdata: lista
        :return: None
        :rtype: None

        Recibe como parámetros el código del cliente a modificar así como los datos que deseamos modificar.
        En realidad toma todos los datos que hay en los widgets de la pantalla clientes.

        """
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare(
            'update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre,fechalta=:fechalta,direccion=:direccion, provincia=:provincia , sexo=:sexo,formaspago=:formaspago ,edad=:edad where codigo =:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':fechalta', str(newdata[3]))
        query.bindValue(':direccion', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':formaspago', str(newdata[7]))
        query.bindValue(':edad', newdata[8])
        if query.exec_():
            print("Modificacion Correcta")
            var.ui.lblstatus.setText('Cliente con dni: ' + str(newdata[0]) + ' modificado')
        else:
            print("Error: ", query.lastError().text())

    def buscaCli(dni):
        """

        Módulos que busca un cliente y carga sus datos en la pantalla cliente

        :param dni: dni cliente a buscar
        :type dni: string
        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select * from clientes where dni =:dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            while query.next():
                var.ui.lblCodcli.setText(str(query.value(0)))
                var.ui.ltDNI.setText(str(query.value(1)))
                var.ui.ltApellidos.setText(str(query.value(2)))
                var.ui.ltNombre.setText(str(query.value(3)))
                var.ui.ltCalendar.setText(str(query.value(4)))
                var.ui.ltDireccion.setText(str(query.value(5)))
                var.ui.cbProvincia.setCurrentText(str(query.value(6)))
                if str(query.value(7)) == 'Mujer':
                    var.ui.rbtFemenino.setChecked(True)
                    var.ui.rbtMasculino.setChecked(False)
                else:
                    var.ui.rbtMasculino.setChecked(True)
                    var.ui.rbtFemenino.setChecked(False)
                for data in var.chkpago:
                    data.setChecked(False)
                if 'Efectivo' in query.value(8):
                    var.chkpago[0].setChecked(True)
                if 'Tarjeta' in query.value(8):
                    var.chkpago[1].setChecked(True)
                if 'Transferencia' in query.value(8):
                    var.chkpago[2].setChecked(True)
                var.ui.spinEdad.setValue(query.value(9))

                dni = query.value(1)
                apellidos = query.value(2)
                nombre = query.value(3)
                var.ui.tableCli.setRowCount(index + 1)
                var.ui.tableCli.setItem(index, 0, QtWidgets.QTableWidgetItem(dni))
                var.ui.tableCli.setItem(index, 1, QtWidgets.QTableWidgetItem(apellidos))
                var.ui.tableCli.setItem(index, 2, QtWidgets.QTableWidgetItem(nombre))
                # # # # var.ui.tableCli.setCellItem(index,x,item)
                index += 1
                var.ui.lblstatus.setText('Cliente con dni: ' + dni + ' encontrado')
        else:
            print("Error mostrar cliente:", query.lastError().text())

    def cargarPro(producto):
        """

        Da de alta un producto cuyos datos se pasan por una lista.
        Muestra mensaje de resultado en el barra de estado.
        Recarga la tabla actualizada de productos

        :param: producto
        :type: lista
        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into productos (producto ,precio ,stock)'
            'VALUES (:producto,:precio,:stock)')
        query.bindValue(':producto', str(producto[0]))
        query.bindValue(':precio', str(producto[1]))
        query.bindValue(':stock', str(producto[2]))
        var.ui.tablePro.setRowCount(1)

        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Producto con nombre ' + producto[0] + ' dado de alta')
        else:
            print("Error: ", query.lastError().text())
            var.ui.lblstatus.setText(
                'Inserción fallida, pruebe a introducir datos de nuevo comprobando que el nombre no sea repetido.')
        clients.Clientes.limpiarTodo(None)
        Conexion.mostrarProductos(None)

    def bajaPro(producto):
        """'

        Módulo para eliminar producto del inventario.

        :param cod
        :type: int
        :return None
        :rtype None

        Se pasa como argumento el código del producto a eliminar.
        A continuación recarga la tablaProd actualizada
        Muestra mensaje resultado en la barra de estado

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from productos where producto = :producto')
        query.bindValue(':producto', producto)
        if query.exec_():
            print('Baja producto')
            var.ui.lblstatus.setText('Producto con nombre ' + producto + ' dado de baja')
        else:
            print(("Error al dar de baja productos:", query.lastError().text()))

    def mostrarProductos(self):
        """

        Módulo que carga los datos de los productos en la tabla Productos

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codigo , producto, precio , stock from productos')
        if query.exec_():
            while query.next():
                codigo = query.value(0)
                producto = query.value(1)
                precio = query.value(2)
                stock = query.value(3)
                var.ui.tablePro.setRowCount(index + 1)
                var.ui.tablePro.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codigo)))
                var.ui.tablePro.setItem(index, 1, QtWidgets.QTableWidgetItem(producto))
                var.ui.tablePro.setItem(index, 2, QtWidgets.QTableWidgetItem(str(precio)))
                var.ui.tablePro.setItem(index, 3, QtWidgets.QTableWidgetItem(str(stock)))
                index += 1
        else:
            print("Error mostrar productos:", query.lastError().text())

    def mostrarProductos2(self):
        """

        Módulo que carga los datos del producto seleccionado en la tabla Productos

        :return: None
        :rtype: None

        """
        producto = var.ui.ltNombrePro.text()
        query = QtSql.QSqlQuery()
        query.prepare('select * from productos where producto =:producto')
        query.bindValue(':producto', producto)
        if query.exec_():
            while query.next():
                var.ui.lblCodPro.setText(str(query.value(0)))
                var.ui.ltNombrePro.setText(str(query.value(1)))
                var.ui.ltPrecioPro.setText(str(query.value(2)))
                var.ui.ltStock.setText(str(query.value(3)))

    def modifPro(codigo, newdata):
        """

        Módulo que actualiza datos del producto

        :param cod: código producto
        :type cod: int
        :param newdata: datos producto
        :type newdata: lista
        :return: None
        :rtype: None

        Recibe como parámetros el código del producto a modificar así como los datos que deseemos modificar.
        En realidad toma todos los datos que hay en los widgets de la pantalla productos.
        El precio se formatea con dos decimales y punto.
        Muestra resultado en la barra de estado

        """
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update productos set producto=:producto, precio=:precio, stock=:stock where codigo =:codigo')
        query.bindValue(':codigo', int(codigo))
        query.bindValue(':producto', str(newdata[0]))
        query.bindValue(':precio', str(newdata[1]))
        query.bindValue(':stock', str(newdata[2]))

        if query.exec_():
            print("Modificacion Correcta")
            var.ui.lblstatus.setText('Producto con nombre: ' + str(newdata[0]) + ' modificado')
        else:
            print("Error: ", query.lastError().text())

    def borraFac(codfac):
        """

        Módulo que borra una factura y todas las ventas asociadas a esa factura

        :param: codfac o código de la factura
        :type: int
        :return: None
        :rtype: None

        En primer lugar borra la factura y luego vuelve a realizar una llamada a la base de datos para
        borrar todas aquellas ventas asociadas a esa factura.

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where codfac = :codfac')
        query.bindValue(':codfac', int(codfac))
        if query.exec_():
            var.ui.lblstatus.setText('Factura anulada')
        else:
            print("Error anular factura en borracfac: ", query.lastError().text())

    def altaFac(dni, fecha, apel):
        """

        Módulo que da de alta una factura previa al proceso de venta

        :param dni: dni cliente
        :type dni: string
        :param fecha: fecha de alta de la factura
        :type fecha: formato fecha en string
        :param apel: apellidos del ciente
        :type apel: string
        :return: None
        :rtype: None

        Recibe datos para carga la factura en la BBDD y en la tabla Factura. Además obtiene el código de la
        factura dada de alta para cargarla en el label lblNumFac ya que al ser autonumérico no se obtiene hasta
        que previamente insertemos la factura.

        """
        query = QtSql.QSqlQuery()
        query.prepare('insert into facturas (dni, fecha, apellidos) VALUES (:dni, :fecha, :apellidos )')
        query.bindValue(':dni', str(dni))
        query.bindValue(':fecha', str(fecha))
        query.bindValue(':apellidos', str(apel))
        if query.exec_():
            var.ui.lblstatus.setText('Factura Creada')
        else:
            print("Error alta factura: ", query.lastError().text())
        query1 = QtSql.QSqlQuery()
        query1.prepare('select max(codfac) from facturas')
        if query1.exec_():
            while query1.next():
                var.ui.lblCodFact.setText(str(query1.value(0)))

    def mostrarFacturas(self):
        """

        Módulo que carga los datos de la factura por orden descendente numérico en la tabla Facturas

        :return: None
        :rtype: None

        """
        index = 0
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas order by codfac desc')
        if query.exec_():
            while query.next():
                # crea la fila
                var.ui.tableFac.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(query.value(0))))
                var.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(query.value(1))))
                index += 1
            Conexion.limpiarFac(self)
            var.ui.tableFac.selectRow(0)
            var.ui.tableFac.setFocus()
        else:
            print("Error mostrar facturas: ", query.lastError().text())
        if index == 0:
            var.ui.tableFac.clearContents()

    def mostrarFacturascli(self):
        """

        Módulo que carga los datos de las facturas del cliente selccionado
        por orden descendente numérico en la tabla Facturas

        :return: None
        :rtype: None

        """
        index = 0
        cont = 0
        dni = var.ui.ltCodCli.text()
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, fecha from facturas where dni = :dni order by codfac desc')
        query.bindValue(':dni', str(dni))
        if query.exec_():
            while query.next():
                # cojo los valores
                cont = cont + 1
                codfac = query.value(0)
                fecha = query.value(1)
                # crea la fila
                var.ui.tableFac.setRowCount(index + 1)
                # voy metiendo los datos en cada celda de la fila
                var.ui.tableFac.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codfac)))
                var.ui.tableFac.setItem(index, 1, QtWidgets.QTableWidgetItem(str(fecha)))
                index += 1
            if cont == 0:
                var.ui.tableFac.setRowCount(0)
                var.ui.lblstatus.setText('Cliente sin Facturas')
        else:
            print("Error mostrar facturas cliente: ", query.lastError().text())

    def limpiarFac(self):
        """

        Módulo que borra los datos contenidos en los widgets de gestión de facturas

        :return: None
        :rtype: None

        """
        datosfac = [var.ui.ltCodCli, var.ui.ltCalendar_2, var.ui.lblCodFact, var.ui.ltNombreCli]
        for i, data in enumerate(datosfac):
            datosfac[i].setText('')

    def cargarFac(cod):
        """

        Módulo que carga datos de un factura en los widgets al clickear sobre una fila de la tablaPro

        :param cod: código de la factura
        :type cod: int
        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('select dni, apellidos from facturas where codfac = :codfac')
        query.bindValue(':codfac', int(cod))
        if query.exec_():
            while query.next():
                var.ui.ltCodCli.setText(str(query.value(0)))
                var.ui.ltNombreCli.setText(str(query.value(1)))

    def cargarFac2(self):
        """

        Módulo que carga datos de un factura en los widgets al clickear sobre una fila de la tablaPro

        :return: None
        :rtype: None

        """
        query = QtSql.QSqlQuery()
        query.prepare('select codfac, dni, fecha, apellidos from facturas ORDER BY codfac DESC LIMIT 1')
        if query.exec_():
            while query.next():
                var.ui.lblCodFact.setText(str(query.value(0)))
                var.ui.ltCodCli.setText(str(query.value(1)))
                var.ui.ltCalendar_2.setText(str(query.value(2)))
                var.ui.ltNombreCli.setText(str(query.value(3)))

    def cargarCmbventa(cmbventa):
        """

        Módulo que carga los datos en el combobox provincias haciendo un llamada a la BBDD.

        :return: None
        :rtype: None

        """
        var.cmbventa.clear()
        query = QtSql.QSqlQuery()
        var.cmbventa.addItem('')
        query.prepare('select codigo, producto from productos order by producto')
        if query.exec_():
            while query.next():
                var.cmbventa.addItem(str(query.value(1)))
        # articulo = var.cmbventa.currentText()
        # return articulo

    def obtenCodPrec(articulo):
        """

        Módulo que devuelve el precio y código del producto que se pasa como parámetro

        :param: articulo
        :type: string
        :return: dato
        :rtype: lista que contiene código y precio del producto

        """
        dato = []
        query = QtSql.QSqlQuery()
        query.prepare('select codigo, precio from productos where producto = :articulo')
        query.bindValue(':articulo', str(articulo))
        if query.exec_():
            while query.next():
                dato = [str(query.value(0)), str(query.value(1))]
        return dato

    def altaVenta(self):
        """

        Módulo que añade líneas de venta en una factura creada

        :return: None
        :rtype: None

        Inserta en la tabla ventas una línea de venta que se va mostrando cada vez que realizamos la transacción.
        Tras realizar la venta se crea una nueva factura incluyendo el combobox de selección de artículor

        """
        query = QtSql.QSqlQuery()
        query.prepare(
            'insert into ventas (codfacventa, codarticventa, cantidad, precio) VALUES (:codfacventa, :codarticventa,'
            ' :cantidad, :precio )')
        query.bindValue(':codfacventa', int(var.venta[0]))
        query.bindValue(':codarticventa', int(var.venta[1]))
        query.bindValue(':cantidad', int(var.venta[3]))
        query.bindValue(':precio', float(var.venta[4]))
        row = var.ui.tableVenta.currentRow()
        if query.exec_():
            var.ui.lblstatus.setText('Venta Realizada')
            var.ui.tableVenta.setItem(row, 1, QtWidgets.QTableWidgetItem(str(var.venta[2])))
            var.ui.tableVenta.setItem(row, 2, QtWidgets.QTableWidgetItem(str(var.venta[3])))
            var.ui.tableVenta.setItem(row, 3, QtWidgets.QTableWidgetItem(str(var.venta[4])))
            var.ui.tableVenta.setItem(row, 4, QtWidgets.QTableWidgetItem(str(var.venta[5])))
            row = row + 1
            var.ui.tableVenta.insertRow(row)
            var.ui.tableVenta.setCellWidget(row, 1, var.cmbventa)
            var.ui.tableVenta.scrollToBottom()
            Conexion.cargarCmbventa(var.cmbventa)
        else:
            print("Error alta venta: ", query.lastError().text())

    def anulaVenta(codVenta):
        """

        Módulo que anula una linea de venta de una factura

        :param: codVenta que es el código de la venta a anlar
        :return: None
        :rtype: None

        Muestra mensaje en la barra de estado

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from ventas where codventa = :codVenta')
        query.bindValue(':codVenta', codVenta)
        if query.exec_():
            var.ui.lblstatus.setText('Venta Anulada')
        else:
            print("Error baja venta: ", query.lastError().text())

    def borraFac(self, codfac):
        """

        Módulo que borra una factura y todas las ventas asociadas a esa factura

        :param: codfac o código de la factura
        :type: int
        :return: None
        :rtype: None

        En primer lugar borra la factura y luego vuelve a realizar una llamada a la base de datos para
        borrar todas aquellas ventas asociadas a esa factura.

        """
        query = QtSql.QSqlQuery()
        query.prepare('delete from facturas where codfac = :codfac')
        query.bindValue(':codfac', int(codfac))
        if query.exec_():
            var.ui.lblstatus.setText('Factura Anulada')
            Conexion.mostrarFacturas(self)
        else:
            print("Error anular factura en borrafac: ", query.lastError().text())

        query1 = QtSql.QSqlQuery()
        query1.prepare('delete from ventas where codfacventa = :codfac')
        query1.bindValue(':codfac', int(codfac))
        if query1.exec_():
            var.ui.lblstatus.setText('Factura Anulada')

        # query1 = QtSql.QSqlQuery()
        # query1.prepare('delete from ventas where codfacventa = :codfac')
        # query1.bindValue(':codfacventa', int(codfac))
        # if query1.exec_():
        #     var.ui.lblstatus.setText('Factura Anulada')
        # else:
        #     print("Error anular factura en borrafac: ", query.lastError().text())

    def listadoVentasfac(codfac):
        """

        Módulo que lista las ventas contenidaa en una factura

        :param codfac: valor factura a la que se incluirán las líneas de venta
        :type codfac: int
        :return: None
        :rtype: None

        Recibe el código de la factura para seleccionar los datos de las ventas cargadas a esta.
        De la BB.DD toma el nombre del producto y su precio para cada línea de venta. El precio lo multiplica
        por las unidades y se obtiene el subtotal de cada línea. Después en cada línea de la tabla irá
        el código de la venta, el nombre del producto, las unidades y el subtotal.
        Finalmente, va sumando el subfact, que es la suma de todas las ventas de esa factura, le aplica el IVA y
        el importe total de la factura. Los tres valores, subfact, iva y fac los muestra en los label asignados.

        En excepciones se recoge cualquier error que se produzca en la ejecución del módulo.

        """
        try:
            var.subfac = 0.00
            var.ui.tableVenta.setRowCount(0)
            query = QtSql.QSqlQuery()
            query1 = QtSql.QSqlQuery()
            query.prepare('select codventa, codarticventa, cantidad from ventas where codfacventa = :codfac')
            query.bindValue(':codfac', int(codfac))

            if query.exec_():
                index = 0
                while query.next():
                    codventa = query.value(0)
                    codarticventa = query.value(1)
                    cantidad = query.value(2)
                    var.ui.tableVenta.setRowCount(index + 1)
                    var.ui.tableVenta.setItem(index, 0, QtWidgets.QTableWidgetItem(str(codventa)))
                    query1.prepare('select producto, precio from productos where codigo = :codarticventa')
                    query1.bindValue(':codarticventa', int(codarticventa))
                    if query1.exec_():
                        while query1.next():
                            articulo = query1.value(0)
                            precio = query1.value(1)
                            var.ui.tableVenta.setItem(index, 1, QtWidgets.QTableWidgetItem(str(articulo)))
                            var.ui.tableVenta.setItem(index, 2, QtWidgets.QTableWidgetItem(str(cantidad)))
                            subtotal = round(float(cantidad) * float(precio), 2)
                            var.ui.tableVenta.setItem(index, 3, QtWidgets.QTableWidgetItem(str(precio)))
                            var.ui.tableVenta.setItem(index, 4, QtWidgets.QTableWidgetItem(str(subtotal)))
                    index += 1
                    var.subfac = round(float(subtotal) + float(var.subfac), 2)

            if int(index) > 0:
                ventas.Ventas.prepararTablaventas(index)
            else:
                print(index)
                var.ui.tableVenta.setRowCount(index)
                ventas.Ventas.prepararTablaventas(index)
            var.ui.lblFactSubtotal.setText(str(var.subfac))
            var.iva = round(float(var.subfac) * 0.21, 2)
            var.ui.lblFactIVA.setText(str(var.iva))
            var.fac = round(float(var.iva) + float(var.subfac), 2)
            var.ui.lblFactTotal.setText(str(var.fac))
        except Exception as error:
            print('Error Listado de la tabla de ventas: %s ' % str(error))

# class Conexion():
#     HOST = 'localhost'
#     PORT = '27017'
#     URI_CONNECTION = 'mongodb://' + HOST + ':' + PORT + '/'#     var.DATABASE = 'empresa'
#     try:
#         var.client = pymongo.MongoClient(URI_CONNECTION)
#         var.client.server_info()
#         print('Conexión realizada al servidor %s'  %HOST)
#     except:
#         print('Error conexion')
