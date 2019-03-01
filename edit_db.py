from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mysql.connector import MySQLConnection
import sys
from PyQt5.uic import loadUi

class AdresDefteri(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('ekran.ui',self)
        self.rehber=self.get_data()
        self.model=self.get_model()
        self.button_ekle.clicked.connect(self.insert_data)
        self.button_sil.clicked.connect(self.delete_data)

    def db_connect(self):
        con = MySQLConnection(
            user='root',
            password='',
            host='127.0.0.1',
            database='contacts'
        )
        return con

    def execute(self,sorgu):
        con=self.db_connect()
        cursor=con.cursor(dictionary=True)
        cursor.execute(sorgu)
        con.commit()

    def get_data(self):
        sorgu=('select * from adres_defteri;')
        con=self.db_connect()
        cursor=con.cursor(dictionary=True)
        cursor.execute(sorgu)
        return cursor.fetchall()

    def get_model(self):
        model=QStandardItemModel()
        model.setHorizontalHeaderLabels(['ADI','SOYADI','TELEFON'])
        self.rehber=self.get_data()
        for kisi in self.rehber:
            model.appendRow([QStandardItem(kisi['adi']),QStandardItem(kisi['soyadi']),QStandardItem(kisi['telefon'])])
        self.tv.setModel(model)

    def insert_data(self):
        if self.txt_ad.text()=="" or self.txt_soyad.text()=="" or self.txt_telefon.text()=="":
            self.txt_ad.setStyleSheet("background-color:#ffb5b6")
            self.txt_soyad.setStyleSheet("background-color:#ffb5b6")
            self.txt_telefon.setStyleSheet("background-color:#ffb5b6")
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Ad, Soyad ve Telefon Bilgisini Giriniz")
            msgBox.setWindowTitle("Uyarı !")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()


        else:
            (self.txt_ad).setStyleSheet("background - color: rgb(239, 239, 239)")
            (self.txt_soyad).setStyleSheet("background - color: rgb(239, 239, 239)")
            (self.txt_telefon).setStyleSheet("background - color: rgb(239, 239, 239)")

            data={
                'ad':self.txt_ad.text(),
                'soyad':self.txt_soyad.text(),
                'telefon':self.txt_telefon.text()
            }
            self.execute(
                'insert into adres_defteri(adi,soyadi,telefon) values("{ad}","{soyad}","{telefon}")'.format(**data))
            self.get_model()
            self.txt_ad.clear()
            self.txt_soyad.clear()
            self.txt_telefon.clear()

    def delete_data(self):
        try:
            dict = self.get_row_and_column()
            ad = dict['adi']
            soyad = dict['soyadi']
            telefon = dict['telefon']
            sorgu = "delete from adres_defteri where adi='{}' and soyadi='{}' and telefon='{}'".format(ad, soyad, telefon)

            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Veriyi Silmek İstediğinize Eminmisiniz")
            msgBox.setWindowTitle("Uyarı !")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                self.execute(sorgu)
                self.get_model()
            else:
                pass
        except:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setText("Lütfen Bir Hücre Seçin")
            msgBox.setWindowTitle("Uyarı !")

            msgBox.exec()

    def get_row_and_column(self):
        indexes = self.tv.selectedIndexes()
        values={}
        for index in indexes:
            row = index.row()
            column = index.column()
            if column == 0:
                value_ad = index.sibling(row, column).data()
                value_soyad = index.sibling(row, (column + 1)).data()
                value_telefon = index.sibling(row, (column + 2)).data()
                values['adi'] = value_ad
                values['soyadi'] = value_soyad
                values['telefon'] = value_telefon
                return values
            elif column == 1:
                value_soyad = index.sibling(row, column).data()
                value_ad = index.sibling(row, (column - 1)).data()
                value_telefon = index.sibling(row, (column + 1)).data()
                values['adi'] = value_ad
                values['soyadi'] = value_soyad
                values['telefon'] = value_telefon
                return values
            elif column == 2:
                value_telefon = index.sibling(row, column).data()
                value_soyad = index.sibling(row, (column - 1)).data()
                value_ad = index.sibling(row, (column - 2)).data()
                values['adi'] = value_ad
                values['soyadi'] = value_soyad
                values['telefon'] = value_telefon
                return values







if __name__=="__main__":
    app=QApplication(sys.argv)
    window2=AdresDefteri()
    window2.show()
    sys.exit(app.exec_())