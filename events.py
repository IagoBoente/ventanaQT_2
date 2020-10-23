import var
import sys


class Eventos:

    def saludo(self):
        try:
            var.ui.lblSaludo.setText('Surprise motherfucker ¡¡')
        except Exception as error:
            print('Error: %s' % str(error))

    def salir(self):
        try:
            sys.exit()
        except Exception as error:
            print('Error: %s' % str(error))

