import threading, time

from PyQt5 import QtSql, QtWidgets

import sys, var, clients, conexion, zipfile, os, shutil
from datetime import datetime, date


class Eventos:

    def salir(event):
        """

        Módulo para cerrar el programa

        :return: None

        Muestra ventana de aviso

        """
        try:
            var.avisoSalir.show()
            if var.avisoSalir.exec_():
                sys.exit()
            else:
                var.avisoSalir.hide()
                event.ignore()  # necesario para que ignore X de la ventana
        except Exception as error:
            print('Error: %s' % str(error))

    def avisoAccion(event):
        """

        Módulo que abre ventana de aviso

        :param: men Mensaje de aviso
        :type: string
        :return: None
        :rtype: None

        """
        try:
            var.avisoAccion.show()
            if var.avisoAccion.exec_():
                aviso = True
            else:
                aviso = False
                event.ignore()  # necesario para que ignore X de la ventana
            var.avisoAccion.hide()
            return aviso
        except Exception as error:
            print('Error: %s' % str(error))

    def avisoAbout(event):
        """

        Módulo que abre la ventana About

        :param: men Mensaje about
        :type: string
        :return: None
        :rtype: None

        """
        try:
            var.mensAbout.show()
            if var.mensAbout.exec_():
                aviso = True
            var.mensAbout.hide()
            return aviso

        except Exception as error:
            print('Error: %s' % str(error))

    def valido(self):
        """

        Modulo que según sea correcto el dni o no, muestra una imagen distinta

        :return: none

        Si es falso escribe en el label una cruz roja si es true devuelve una V verda

        """
        try:
            dni = var.ui.ltDNI.text()
            if clients.Clientes.validardni(dni):
                var.ui.lblValido.setStyleSheet('QLabel {color: green;font-family:Arial;font-size:20px;}')
                var.ui.lblValido.setText('V')
                var.ui.ltDNI.setText(dni.upper())
            else:
                var.ui.lblValido.setStyleSheet('QLabel {color: red;font-family:Arial;font-size:20px;}')
                var.ui.lblValido.setText('X')
                var.ui.ltDNI.setText(dni.upper())

        except Exception as error:
            print('Error: %s' % str(error))

    def cargarProv(self):
        """

        Módulo que se ejecuta al principio para cargar las provincias. En versión posterior cargaremos
        y municipios desde la BBDD.

        :return: None
        :rtype: None

        """
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra']
            for i in prov:
                var.ui.cbProvincia.addItem(i)
        except Exception as error:
            print('Error: %s' % str(error))

    def cargarArt(self):
        """

        Módulo que se ejecuta al principio para cargar los articulos.

        :return: None
        :rtype: None

        """
        try:
            var.cbArticulo.clear()
            query = QtSql.QSqlQuery()
            var.cbArticulo.addItem('')
            query.prepare('select nombre from articulos')
            if query.exec_():
                while query.next():
                    var.cbArticulo.addItem(str(query.value(0)))
            else:
                print("Error cargar articulos de la bd:", query.lastError().text())
        except Exception as error:
            print('Error cargar articulos: %s' % str(error))

    def AbrirDir(self):
        """

        Módulo que abre una ventana de diálogo

        :return: None
        :rtype: None

        """
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s' % str(error))

    def MostrarFecha(self):
        """

        Modulo que carga la fecha actual

        :return: none

        """
        try:
            now = datetime.now()
            today = date.today()
            current_time = now.strftime("%H:%M:%S")
            current_date = today.strftime("%d/%m/%Y")
            fecha = current_time + "\n" + current_date
            var.ui.lblstatus_2.setText(current_date)
        except Exception as error:
            print('Error abrir explorador: %s' % str(error))

    def AbrirPrinter(self):
        """

        Módulo que abre la ventana de diálogo de la impresora

        :return: None
        :rtype: None

        """
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))

    def Backup(self):
        """

        Módulo que realizar el backup de la BBDD

        :return: None
        :rtype: None

        Utiliza la librería zipfile, añade la fecha y hora de la copia al nombre de esta y tras realizar la copia
        la mueve al directorio deseado por el cliente. Para ello abre una ventana de diálogo

        """
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.filedlgabrir.getSaveFileName(None, 'Guardar Copia', var.copia, '.zip',
                                                                    options=option)
            if var.filedlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                var.ui.lblstatus.setText('COPIA DE SEGURIDAD DE BASE DE DATOS CREADA')
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error: %s' % str(error))

    def restaurarBD(self):
        """

        Módulo que restaura la BBDD

        :return: None
        :rtype: None

        Abre ventana de diálogo para buscar el directorio donde está copia de la BBDD y la restaura haciendo suo
        de la librería zipfile
        Muestra mensaje de confirmación

        """
        try:
            option = QtWidgets.QFileDialog.Options()
            filename = var.filedlgabrir.getOpenFileName(None, 'Restaurar copia de seguridad','','*.zip;;All Files',
                                                        options=option)
            if var.filedlgabrir.Accepted and filename != '':
                file = filename[0]
                with zipfile.ZipFile(str(file), 'r') as bbdd:
                    # bbdd = zipfile.ZipFile(str(filename[0]), 'r')
                    bbdd.extractall(pwd=None)
                bbdd.close()
                conexion.Conexion.db_connect(var.filebd)
                conexion.Conexion.mostrarClientes(self)
                conexion.Conexion.mostrarProductos(self)
                conexion.Conexion.mostrarFacturas(self)

        except Exception as error:
            print('Error restaurar base de datos: %s' % str(error))
