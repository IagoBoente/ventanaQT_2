from PyQt5 import  QtWidgets,QtSql

class Conexion():
    def db_connect(filename):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName(filename)
        if not db.open():
            QtWidgets.QMessageBox.critical(None,'No se puede abrir la BBDD',QtWidgets.QMessageBox.Cancel)
            return False
        else:
            print('Conexion Establecida')
        return  True

    def cargarCli(cliente):
        query = QtSql.QSqlQuery()
        query.prepare('')