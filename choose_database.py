from mysql.connector import MySQLConnection
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from  PyQt5 import uic
class chooseDb(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('choose_db.ui',self)
        self.databases=self.get_databases()
        self.get_model()
        self.dbtable.clicked.connect(self.set_db_name)
        self.button_gir.clicked.connect(self.go_edit_db)
        self.show()

    def get_databases(self):
        not_get=["information_schema","performance_schema","phpmyadmin","mysql"]
        connect = MySQLConnection(
            user='root',
            password='',
            host='127.0.0.1',
        )

        cursor = connect.cursor()
        cursor.execute("show databases;")
        dbs = cursor.fetchall()
        connect.close()
        databases=[]
        for i in range(0, len(dbs)):
            databases.append(dbs[i][0])
        for a in not_get:
            databases.remove(a)
        print(databases)
        return databases

    def get_model(self):
        model=QStandardItemModel()
        model.setHorizontalHeaderLabels(["VERİTABANI İSİMLERİ"])
        for i in range(0,len(self.databases)):
            model.appendRow([QStandardItem(self.databases[i])])

        self.dbtable.horizontalHeader().setStretchLastSection(True)
        self.dbtable.setModel(model)

    def set_db_name(self):
        selected_index=self.dbtable.selectedIndexes()
        for field in selected_index:
            self.db_name=field.sibling(field.row(),field.column()).data()
        self.txt_db.setText(self.db_name)

    def go_edit_db(self):
        if self.txt_db.text() == "":
            error = QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Lütfen Bir Veritabanı Seçin")
            error.setWindowTitle("Eksik Alan")
            error.exec_()
        else:
            self.db_name=self.txt_db.text()
            sys.exit()


if __name__ == "__main__":
    app=QApplication(sys.argv)
    window=chooseDb()
    window.show()
    sys.exit(app.exec_())

