# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'validation.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511, 278)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(200, 250, 121, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 41, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 30, 31, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 50, 101, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(10, 70, 101, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 90, 101, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(10, 110, 151, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(10, 130, 101, 17))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(10, 150, 41, 17))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(10, 170, 111, 17))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(10, 190, 111, 17))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Dialog)
        self.label_12.setGeometry(QtCore.QRect(10, 210, 111, 17))
        self.label_12.setObjectName("label_12")
        self.lbl_nama = QtWidgets.QLabel(Dialog)
        self.lbl_nama.setGeometry(QtCore.QRect(160, 10, 341, 17))
        self.lbl_nama.setObjectName("lbl_nama")
        self.lbl_nik = QtWidgets.QLabel(Dialog)
        self.lbl_nik.setGeometry(QtCore.QRect(160, 30, 341, 17))
        self.lbl_nik.setObjectName("lbl_nik")
        self.lbl_kelamin = QtWidgets.QLabel(Dialog)
        self.lbl_kelamin.setGeometry(QtCore.QRect(160, 50, 341, 17))
        self.lbl_kelamin.setObjectName("lbl_kelamin")
        self.lbl_umur = QtWidgets.QLabel(Dialog)
        self.lbl_umur.setGeometry(QtCore.QRect(160, 70, 341, 17))
        self.lbl_umur.setObjectName("lbl_umur")
        self.lbl_pw = QtWidgets.QLabel(Dialog)
        self.lbl_pw.setGeometry(QtCore.QRect(160, 90, 341, 17))
        self.lbl_pw.setObjectName("lbl_pw")
        self.lbl_time = QtWidgets.QLabel(Dialog)
        self.lbl_time.setGeometry(QtCore.QRect(160, 110, 341, 17))
        self.lbl_time.setObjectName("lbl_time")
        self.lbl_berlaku = QtWidgets.QLabel(Dialog)
        self.lbl_berlaku.setGeometry(QtCore.QRect(160, 130, 341, 17))
        self.lbl_berlaku.setObjectName("lbl_berlaku")
        self.lbl_suhu = QtWidgets.QLabel(Dialog)
        self.lbl_suhu.setGeometry(QtCore.QRect(160, 150, 341, 17))
        self.lbl_suhu.setObjectName("lbl_suhu")
        self.lbl_bpm = QtWidgets.QLabel(Dialog)
        self.lbl_bpm.setGeometry(QtCore.QRect(160, 170, 341, 17))
        self.lbl_bpm.setObjectName("lbl_bpm")
        self.lbl_spo2 = QtWidgets.QLabel(Dialog)
        self.lbl_spo2.setGeometry(QtCore.QRect(160, 190, 341, 17))
        self.lbl_spo2.setObjectName("lbl_spo2")
        self.lbl_tensi = QtWidgets.QLabel(Dialog)
        self.lbl_tensi.setGeometry(QtCore.QRect(160, 210, 341, 17))
        self.lbl_tensi.setObjectName("lbl_tensi")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Publish and print"))
        self.label_2.setText(_translate("Dialog", "Nama"))
        self.label_3.setText(_translate("Dialog", "NIK"))
        self.label_4.setText(_translate("Dialog", "Jenis Kelamin"))
        self.label_5.setText(_translate("Dialog", "Umur"))
        self.label_6.setText(_translate("Dialog", "Kode"))
        self.label_7.setText(_translate("Dialog", "Tanggal Pengambilan"))
        self.label_8.setText(_translate("Dialog", "Masa Berlaku"))
        self.label_9.setText(_translate("Dialog", "Suhu"))
        self.label_10.setText(_translate("Dialog", "Detak Jantung"))
        self.label_11.setText(_translate("Dialog", "Oximeter"))
        self.label_12.setText(_translate("Dialog", "Tensi"))
        self.lbl_nama.setText(_translate("Dialog", ":"))
        self.lbl_nik.setText(_translate("Dialog", ":"))
        self.lbl_kelamin.setText(_translate("Dialog", ":"))
        self.lbl_umur.setText(_translate("Dialog", ":"))
        self.lbl_pw.setText(_translate("Dialog", ":"))
        self.lbl_time.setText(_translate("Dialog", ":"))
        self.lbl_berlaku.setText(_translate("Dialog", ":"))
        self.lbl_suhu.setText(_translate("Dialog", ":"))
        self.lbl_bpm.setText(_translate("Dialog", ":"))
        self.lbl_spo2.setText(_translate("Dialog", ":"))
        self.lbl_tensi.setText(_translate("Dialog", ":"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
