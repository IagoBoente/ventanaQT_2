import threading, time

from PyQt5 import QtSql,QtWidgets

import sys, var, clients, conexion, zipfile, os, shutil
from datetime import datetime, date


class Eventos:

    def saludo(self):
        try:
            var.ui.lblstatus.setText('Surprise ¡¡')
        except Exception as error:
            print('Error: %s' % str(error))

    def salir(event):
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
        try:
            var.mensAbout.show()
            if var.mensAbout.exec_():
                aviso = True
            var.mensAbout.hide()
            return aviso

        except Exception as error:
            print('Error: %s' % str(error))

    def valido(self):
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
        try:
            prov = ['', 'A Coruña', 'Lugo', 'Ourense', 'Pontevedra']
            for i in prov:
                var.ui.cbProvincia.addItem(i)
        except Exception as error:
            print('Error: %s' % str(error))

    def cargarArt(self):
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
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s' % str(error))

    def MostrarFecha(self):
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
        try:
            var.dlgImprimir.setWindowTitle('Imprimir')
            var.dlgImprimir.setModal(True)
            var.dlgImprimir.show()
        except Exception as error:
            print('Error abrir imprimr: %s ' % str(error))

    def Backup(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y.%m.%d.%H.%M.%S')
            var.copia = (str(fecha) + '_backup.zip')
            option = QtWidgets.QFileDialog.Options()
            directorio, filename = var.filedlgabrir.getSaveFileName(None,'Guardar Copia',var.copia,'.zip',options=option)
            if var.filedlgabrir.Accepted and filename != '':
                fichzip = zipfile.ZipFile(var.copia, 'w')
                fichzip.write(var.filebd, os.path.basename(var.filebd), zipfile.ZIP_DEFLATED)
                fichzip.close()
                var.ui.lblstatus.setText('COPIA DE SEGURIDAD DE BASE DE DATOS CREADA')
                shutil.move(str(var.copia), str(directorio))
        except Exception as error:
            print('Error: %s' % str(error))