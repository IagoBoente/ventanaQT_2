import var
import sys
import clients


class Eventos:

    def saludo(self):
        try:
            var.ui.lblstatus.setText('Surprise mothrfckr ¡¡')
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

    def AbrirDir(self):
        try:
            var.filedlgabrir.show()
        except Exception as error:
            print('Error abrir explorador: %s' %str(error))


