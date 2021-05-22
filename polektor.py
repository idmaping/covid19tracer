# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'polektor.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(401, 101)
        self.lbl_tensi = QtWidgets.QLabel(Form)
        self.lbl_tensi.setGeometry(QtCore.QRect(10, 10, 121, 17))
        self.lbl_tensi.setObjectName("lbl_tensi")
        self.lbl_suhu = QtWidgets.QLabel(Form)
        self.lbl_suhu.setGeometry(QtCore.QRect(10, 30, 121, 17))
        self.lbl_suhu.setObjectName("lbl_suhu")
        self.lbl_bpm = QtWidgets.QLabel(Form)
        self.lbl_bpm.setGeometry(QtCore.QRect(10, 50, 121, 17))
        self.lbl_bpm.setObjectName("lbl_bpm")
        self.lbl_spo2 = QtWidgets.QLabel(Form)
        self.lbl_spo2.setGeometry(QtCore.QRect(10, 70, 121, 17))
        self.lbl_spo2.setObjectName("lbl_spo2")
        self.btn_measure = QtWidgets.QPushButton(Form)
        self.btn_measure.setGeometry(QtCore.QRect(300, 40, 89, 25))
        self.btn_measure.setObjectName("btn_measure")
        self.btn_refresh = QtWidgets.QPushButton(Form)
        self.btn_refresh.setGeometry(QtCore.QRect(210, 40, 89, 25))
        self.btn_refresh.setObjectName("btn_refresh")
        self.cb_serial = QtWidgets.QComboBox(Form)
        self.cb_serial.setGeometry(QtCore.QRect(210, 10, 181, 25))
        self.cb_serial.setObjectName("cb_serial")
        self.cb_serial.addItem("")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_tensi.setText(_translate("Form", ": 0/0 mmHg"))
        self.lbl_suhu.setText(_translate("Form", ": 0 Celcius"))
        self.lbl_bpm.setText(_translate("Form", ": 0 BPM"))
        self.lbl_spo2.setText(_translate("Form", ": 0 %"))
        self.btn_measure.setText(_translate("Form", "Measure"))
        self.btn_refresh.setText(_translate("Form", "Refresh"))
        self.cb_serial.setItemText(0, _translate("Form", "None"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
