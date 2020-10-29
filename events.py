import var
import sys
import clients


class Eventos:

    def saludo(self):
        try:
            var.ui.lblSaludo.setText('Surprise mothrfckr ¡¡')
        except Exception as error:
            print('Error: %s' % str(error))

    def salir(self):
        try:
            sys.exit()
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
