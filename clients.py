import var

class Clientes:

    def validardni(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            dni = dni.upper()
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                return len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control
            return False
        except:
            print("error en la app")
            return None
    def selSexo(self):
        try:
            if var.ui.rbtFemenino.isChecked():
                print('has elegido femenino')
            if var.ui.rbtMasculino.isChecked():
                print('has elegido masculino')
        except Exception as error:
            print('Error:%s'% str(error))

    def selPago(self):
        try:
            if var.ui.chkEfectivo.isChecked():
                print("Pagas con efectivo")
            if var.ui.chkTarjeta.isChecked():
                print("Pagas con tarjeta")
            if var.ui.chkTransfer.isChecked():
                print("Pagas con transferecia")
        except Exception as error:
            print('Error:%s'% str(error))

    def selProv(prov):
        try:
            print('Has selccionado la provincia de ', prov)
            return prov
        except Exception as error:
            print('Error:%s' % str(error))

