import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class FormNilai(QWidget):
    def __init__(self):
        super().__init__()
        loadUi("nilai.ui", self)  

        self.conn = sqlite3.connect("mahasiswa.db")
        self.cursor = self.conn.cursor()

        self.btn_tambah.clicked.connect(self.tambah_data)
        self.btn_ubah.clicked.connect(self.ubah_data)
        self.btn_hapus.clicked.connect(self.hapus_data)
        self.btn_batal.clicked.connect(self.batal_input)
        self.tableNilai.cellClicked.connect(self.isi_form_dari_tabel)

        self.load_mahasiswa()
        self.load_data()

    def load_mahasiswa(self):
        self.comboBox_mahasiswa.clear()
        self.cursor.execute("SELECT id, nama FROM mahasiswa")
        for id_mhs, nama in self.cursor.fetchall():
            self.comboBox_mahasiswa.addItem(nama, id_mhs)

    def load_data(self):
        self.tableNilai.setRowCount(0)
        self.cursor.execute("""
            SELECT nilai.id, mahasiswa.nama, nilai.nilai_harian, nilai.nilai_tugas, nilai.nilai_uts, nilai.nilai_uas
            FROM nilai JOIN mahasiswa ON nilai.id_mahasiswa = mahasiswa.id
        """)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tableNilai.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tableNilai.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def tambah_data(self):
        id_mhs = self.comboBox_mahasiswa.currentData()
        harian = self.lineEdit_harian.text()
        tugas = self.lineEdit_tugas.text()
        uts = self.lineEdit_uts.text()
        uas = self.lineEdit_uas.text()

        self.cursor.execute("""
            INSERT INTO nilai (id_mahasiswa, nilai_harian, nilai_tugas, nilai_uts, nilai_uas)
            VALUES (?, ?, ?, ?, ?)
        """, (id_mhs, harian, tugas, uts, uas))
        self.conn.commit()
        self.load_data()
        self.batal_input()

    def ubah_data(self):
        current_row = self.tableNilai.currentRow()
        if current_row < 0:
            return

        id_nilai = int(self.tableNilai.item(current_row, 0).text())
        id_mhs = self.comboBox_mahasiswa.currentData()
        harian = self.lineEdit_harian.text()
        tugas = self.lineEdit_tugas.text()
        uts = self.lineEdit_uts.text()
        uas = self.lineEdit_uas.text()

        self.cursor.execute("""
            UPDATE nilai SET id_mahasiswa=?, nilai_harian=?, nilai_tugas=?, nilai_uts=?, nilai_uas=?
            WHERE id=?
        """, (id_mhs, harian, tugas, uts, uas, id_nilai))
        self.conn.commit()
        self.load_data()
        self.batal_input()

    def hapus_data(self):
        current_row = self.tableNilai.currentRow()
        if current_row < 0:
            return

        id_nilai = int(self.tableNilai.item(current_row, 0).text())
        self.cursor.execute("DELETE FROM nilai WHERE id=?", (id_nilai,))
        self.conn.commit()
        self.load_data()
        self.batal_input()

    def batal_input(self):
        self.comboBox_mahasiswa.setCurrentIndex(0)
        self.lineEdit_harian.clear()
        self.lineEdit_tugas.clear()
        self.lineEdit_uts.clear()
        self.lineEdit_uas.clear()
        self.tableNilai.clearSelection()

    def isi_form_dari_tabel(self, row, _):
        nama = self.tableNilai.item(row, 1).text()
        self.comboBox_mahasiswa.setCurrentText(nama)
        self.lineEdit_harian.setText(self.tableNilai.item(row, 2).text())
        self.lineEdit_tugas.setText(self.tableNilai.item(row, 3).text())
        self.lineEdit_uts.setText(self.tableNilai.item(row, 4).text())
        self.lineEdit_uas.setText(self.tableNilai.item(row, 5).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FormNilai()
    window.show()
    sys.exit(app.exec_())
