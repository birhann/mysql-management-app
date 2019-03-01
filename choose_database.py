from mysql.connector import MySQLConnection
import edit_db
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
        self.button_gir.clicked.connect(self.go_edit_db)
        self.dbtable.clicked.connect(self.view_db_name)

    def get_databases(self):
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
        return databases

    def get_model(self):
        model=QStandardItemModel()
        model.setHorizontalHeaderLabels(["VERİTABANI İSİMLERİ"])
        for i in range(1,len(self.databases)):
            model.appendRow([QStandardItem(self.databases[i])])

        self.dbtable.horizontalHeader().setStretchLastSection(True)
        self.dbtable.setModel(model)

    def view_db_name(self):
        selected_index=self.dbtable.selectedIndexes()
        for db_name in selected_index:
            self.db_name=db_name.sibling(db_name.row(),db_name.column()).data()
        self.txt_db.setText(self.db_name)

    def go_edit_db(self):
        try:
            edit_db.AdresDefteri.show()
            window.close()
        except:
            error=QMessageBox()
            error.setIcon(QMessageBox.Warning)
            error.setText("Lütfen Bir Veritabanı Seçin")
            error.setWindowTitle("Eksik Alan")
            error.exec_()







app=QApplication(sys.argv)
window=chooseDb()
window.show()
sys.exit(app.exec_())
