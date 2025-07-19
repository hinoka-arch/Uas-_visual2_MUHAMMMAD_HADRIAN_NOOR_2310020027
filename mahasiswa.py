import sqlite3


conn = sqlite3.connect("mahasiswa.db")  
cursor = conn.cursor()

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
import sys

class FormMahasiswa(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mahasiswa.ui", self)

        self.btn_tambah.clicked.connect(self.tambah_data)
        self.btn_ubah.clicked.connect(self.ubah_data)
        self.btn_hapus.clicked.connect(self.hapus_data)
        self.btn_batal.clicked.connect(self.batal_input)
        self.tableMahasiswa.cellClicked.connect(self.isi_form_dari_tabel)

    def tambah_data(self):
        data = self.ambil_data_input()

        if not data["NIM"] or not data["Nama"]:
            QMessageBox.warning(self, "Peringatan", "NIM dan Nama harus diisi!")
            return

        row_pos = self.tableMahasiswa.rowCount()
        self.tableMahasiswa.insertRow(row_pos)

        for i, value in enumerate(data.values()):
            self.tableMahasiswa.setItem(row_pos, i, QTableWidgetItem(value))

        self.batal_input()

    def ubah_data(self):
        selected = self.tableMahasiswa.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin diubah!")
            return

        data = self.ambil_data_input()
        for i, value in enumerate(data.values()):
            self.tableMahasiswa.setItem(selected, i, QTableWidgetItem(value))

        self.batal_input()

    def hapus_data(self):
        selected = self.tableMahasiswa.currentRow()
        if selected >= 0:
            self.tableMahasiswa.removeRow(selected)
            self.batal_input()
        else:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus!")

    def batal_input(self):
        self.lineEdit_NIM.clear()
        self.lineEdit_nama.clear()
        self.lineEdit_panggilan.clear()
        self.lineEdit_telpon.clear()
        self.lineEdit_email.clear()
        self.lineEdit_kelas.clear()
        self.lineEdit_kuliah.clear()
        self.lineEdit_lokasi.clear()
        self.tableMahasiswa.clearSelection()

    def isi_form_dari_tabel(self, row, column):
        self.lineEdit_NIM.setText(self.tableMahasiswa.item(row, 0).text())
        self.lineEdit_nama.setText(self.tableMahasiswa.item(row, 1).text())
        self.lineEdit_panggilan.setText(self.tableMahasiswa.item(row, 2).text())
        self.lineEdit_telpon.setText(self.tableMahasiswa.item(row, 3).text())
        self.lineEdit_email.setText(self.tableMahasiswa.item(row, 4).text())
        self.lineEdit_kelas.setText(self.tableMahasiswa.item(row, 5).text())
        self.lineEdit_kuliah.setText(self.tableMahasiswa.item(row, 6).text())
        self.lineEdit_lokasi.setText(self.tableMahasiswa.item(row, 7).text())

    def ambil_data_input(self):
        return {
            "NIM": self.lineEdit_NIM.text().strip(),
            "Nama": self.lineEdit_nama.text().strip(),
            "Panggilan": self.lineEdit_panggilan.text().strip(),
            "Telpon": self.lineEdit_telpon.text().strip(),
            "Email": self.lineEdit_email.text().strip(),
            "Kelas": self.lineEdit_kelas.text().strip(),
            "Kuliah": self.lineEdit_kuliah.text().strip(),
            "Lokasi": self.lineEdit_lokasi.text().strip()
        }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormMahasiswa()
    window.show()
    sys.exit(app.exec_())
