from PyQt5 import QtWidgets

import conexion
import var
import events


class Productos:

    def altaProductos(self):
        """

        Módulo que insertar los proudctos en la tabla y en la base de datos
        en las búsquedas mostrará los datos del producto
        :return: None
        :rtype: None
        """
        if len(var.ui.ltNombrePro.text()) > 0 and len(var.ui.ltPrecioPro.text()) > 0:
            try:
                newpro = []
                tablePro = []  # sera lo que cargamos en la table
                producto = [var.ui.ltNombrePro, var.ui.ltPrecioPro, var.ui.ltStock]
                k = 0
                for i in producto:
                    newpro.append(i.text())  # cargamos los valores que hay en los editline
                    if k < 3:
                        tablePro.append(i.text())
                        k += 1
                if producto:
                    row = 0  # posicion de la fila, problema: coloca al ultimo como primero en cada click
                    column = 0  # posicion de la columna
                    var.ui.tablePro.insertRow(row)  # insertamos una fila nueva con cada click de boton
                    for registro in tablePro:
                        cell = QtWidgets.QTableWidgetItem(registro)
                        var.ui.tablePro.setItem(row, column, cell)
                        column += 1
                    conexion.Conexion.cargarPro(newpro)

                else:
                    print('Faltan datos')
                    Productos.limpiarPro(self)

            except Exception as error:
                print('Error:%s' % str(error))
        else:
            var.ui.lblstatus.setText('Faltan datos')

    def limpiarPro(self):
        """

        Módulo que limpia los datos del formulario producto

        :return: None
        :rtype: None
        """
        producto = [var.ui.ltNombrePro, var.ui.ltPrecioPro, var.ui.ltStock]
        try:
            for i in range(len(producto)):
                producto[i].setText('')

            var.ui.lblstatus.setText('')
            var.ui.lblCodPro.setText('')
            var.ui.lblStock.setText('')

            # var.ui.tablePro.removeRow(0)

        except Exception as error:
            print('Error:%s' % str(error))

    def limpiarTodo(self):
        """

        Módulo que limpia los datos del formulario producto y la tabla

        :return: None
        :rtype: None
        """
        producto = [var.ui.ltNombrePro, var.ui.ltPrecioPro, var.ui.ltStock]
        try:
            for i in range(len(producto)):
                producto[i].setText('')

            var.ui.lblstatus.setText('')
            var.ui.lblCodPro.setText('')
            var.ui.lblStock.setText('')

            var.ui.tablePro.setRowCount(0)

        except Exception as error:
            print('Error:%s' % str(error))

    def cargarproductos(self):
        """

        Módulo que carga en widgets formulario productos la fila que se clickea en la tablaPro

        :return: None
        :type: None

        """
        try:
            fila = var.ui.tablePro.selectedItems()
            if fila:
                fila = [dato.text() for dato in fila]
            print(fila)
            var.ui.ltNombrePro.setText(fila[1])
            conexion.Conexion.mostrarProductos2(self)
            var.ui.lblstatus.setText('Producto cargado')
        except Exception as error:
            print('Error:%s' % str(error))

    def bajaproductos(self):
        """

        Módulo para dar de baja un producto y recarga la tabla productos y limpia el formulario productos

        :return: None
        :type: None

        """
        nombre = var.ui.ltNombrePro.text()
        try:
            if len(nombre) > 0:
                aviso = events.Eventos.avisoAccion(self)
                if aviso:
                    conexion.Conexion.bajaPro(nombre)
                    Productos.limpiarTodo(self)
                    var.ui.lblstatus.setText('producto con nombre: ' + nombre + ' dado de baja')
                    conexion.Conexion.mostrarProductos(self)
                else:
                    var.ui.lblstatus.setText('Eliminar producto CANCELADO')
            else:
                var.ui.lblstatus.setText('Producto inexistente')
        except Exception as error:
            print('Error:%s' % str(error))

    def modifproductos(self):
        """

        Módulo para modificar datos de un producto con determinado código

        :return: None
        :rtype: None

        Además recarga la tabla de productos con los valores actualizados

        """
        try:
            newdata = []
            producto = [var.ui.ltNombrePro, var.ui.ltPrecioPro,var.ui.ltStock]
            for i in producto:
                newdata.append(i.text())
            cod = var.ui.lblCodPro.text()
            conexion.Conexion.modifPro(cod, newdata)
            conexion.Conexion.mostrarProductos(self)
        except Exception as error:
            print('Error al cargar Productos:%s' % str(error))

    def reloadPro(self):
        """

        Limpia datos formulario y recarga la tabla de productos llamando al
        módulo mostrarProductos de la clase Conexion

        :return: None

        """
        try:
            Productos.limpiarTodo(self)
            conexion.Conexion.mostrarProductos(self)
            var.ui.lblstatus.setText('Datos recargados')
        except Exception as error:
            print('Error al recargar Productos%s' % str(error))

    def buscarPro(self):
        """

        Busca un producto a partir de un nombre

        :return: None
        :rtype: None

        """
        try:
            nombre = var.ui.ltnombre.text()
            Productos.limpiarTodo(self)
            conexion.Conexion.buscaPro(nombre)
        except Exception as error:
            print('Error al buscar productos %s' % str(error))
