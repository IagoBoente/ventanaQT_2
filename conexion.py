from PyQt5 import QtWidgets, QtSql

import clients
import var


class Conexion():
    def db_connect(filename):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None, 'No se puede abrir la BBDD', QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexion Establecida')
        return True

    def cargarCli(cliente):
        query = QtSql.QSqlQuery()
        query.prepare('insert into clientes (dni, apellidos, nombre ,direccion, fechalta, provincia, sexo , pago , edad)'
                      'VALUES (:dni, :apellidos, :nombre, :direccion,:fechalta, :provincia, :sexo, :pago, :edad)')
        query.bindValue(':dni', str(cliente[0]))
        query.bindValue(':apellidos', str(cliente[1]))
        query.bindValue(':nombre', str(cliente[2]))
        query.bindValue(':direccion', str(cliente[3]))
        query.bindValue(':fechalta', str(cliente[4]))
        query.bindValue(':provincia', str(cliente[5]))
        query.bindValue(':sexo', str(cliente[6]))
        query.bindValue(':pago', str(cliente[7]))
        query.bindValue(':edad', cliente[8])

        var.ui.tableCli.setRowCount(1)

        if query.exec_():
            print("Inserción Correcta")
            var.ui.lblstatus.setText('Cliente con dni ' + cliente[0] + ' dado de alta')
        else:
            print("Error: ", query.lastError().text())
            var.ui.lblstatus.setText('Inserción fallida, pruebe a introducir datos de nuevo comprobando que el DNI no sea repetido.')

        Conexion.mostrarClientes(None)
    def mostrarClientes2(self):
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
                var.ui.ltDireccion.setText(str(query.value(4)))
                var.ui.ltCalendar.setText(str(query.value(5)))
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
        query = QtSql.QSqlQuery()
        query.prepare('delete from clientes where dni = :dni')
        query.bindValue(':dni', dni)
        if query.exec_():
            print('Baja cliente')
            var.ui.lblstatus.setText('Cliente con dni ' + dni + ' dado de baja')
        else:
            print(("Error mostrar clientes:", query.lastError().text()))

    def mostrarClientes(self):
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

    def modifCli(codigo, newdata):
        query = QtSql.QSqlQuery()
        codigo = int(codigo)
        query.prepare('update clientes set dni=:dni, apellidos=:apellidos, nombre=:nombre,direccion=:direccion ,fechalta=:fechalta, provincia=:provincia , sexo=:sexo,pago=:pago ,edad=:edad where codigo =:codigo')
        query.bindValue(':codigo',int(codigo))
        query.bindValue(':dni', str(newdata[0]))
        query.bindValue(':apellidos', str(newdata[1]))
        query.bindValue(':nombre', str(newdata[2]))
        query.bindValue(':direccion', str(newdata[3]))
        query.bindValue(':fechalta', str(newdata[4]))
        query.bindValue(':provincia', str(newdata[5]))
        query.bindValue(':sexo', str(newdata[6]))
        query.bindValue(':pago', str(newdata[7]))
        query.bindValue(':edad', newdata[8])
        if query.exec_():
            print("Modificacion Correcta")
            var.ui.lblstatus.setText('Cliente con dni: ' + str(newdata[0]) + ' modificado')
        else:
            print("Error: ", query.lastError().text())

    def buscaCli(dni):
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
                var.ui.ltDireccion.setText(str(query.value(4)))
                var.ui.ltCalendar.setText(str(query.value(5)))
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
                index += 1
                var.ui.lblstatus.setText('Cliente con dni: ' + dni + ' encontrado')
        else:
            print("Error mostrar cliente:", query.lastError().text())

