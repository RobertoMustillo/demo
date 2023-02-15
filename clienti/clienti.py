# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clienti.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1300, 700)
        self.bgwidget = QtWidgets.QWidget(Dialog)
        self.bgwidget.setGeometry(QtCore.QRect(0, 0, 1500, 800))
        self.bgwidget.setStyleSheet("QWidget#bgwidget{\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(253, 153, 8, 255), stop:1 rgba(255, 255, 255, 255));\n"
"\n"
"}")
        self.bgwidget.setObjectName("bgwidget")
        self.image = QtWidgets.QLabel(self.bgwidget)
        self.image.setEnabled(True)
        self.image.setGeometry(QtCore.QRect(-200, -270, 1800, 1300))
        self.image.setStyleSheet("border-radius:50%;\n"
"image: url(:/images/1.png);\n"
"")
        self.image.setText("")
        self.image.setScaledContents(True)
        self.image.setObjectName("image")
        self.label = QtWidgets.QLabel(self.bgwidget)
        self.label.setGeometry(QtCore.QRect(450, 60, 441, 91))
        font = QtGui.QFont()
        font.setFamily("Bangla MN")
        font.setPointSize(36)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet("font: 36pt;\n"
"background: transparent;\n"
"color: rgb(255,255,255);")
        self.label.setObjectName("label")
        self.btnModifica = QtWidgets.QPushButton(self.bgwidget)
        self.btnModifica.setGeometry(QtCore.QRect(70, 320, 113, 32))
        self.btnModifica.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(16, 128, 128);")
        self.btnModifica.setObjectName("btnModifica")
        self.btnCancella = QtWidgets.QPushButton(self.bgwidget)
        self.btnCancella.setGeometry(QtCore.QRect(70, 400, 113, 32))
        self.btnCancella.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(16, 128, 128);")
        self.btnCancella.setObjectName("btnCancella")
        self.btnAggiungi = QtWidgets.QPushButton(self.bgwidget)
        self.btnAggiungi.setGeometry(QtCore.QRect(70, 250, 113, 32))
        self.btnAggiungi.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(16, 128, 128);")
        self.btnAggiungi.setObjectName("btnAggiungi")
        self.btnEsci = QtWidgets.QPushButton(self.bgwidget)
        self.btnEsci.setGeometry(QtCore.QRect(70, 490, 113, 32))
        self.btnEsci.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(16, 128, 128);")
        self.btnEsci.setObjectName("btnEsci")
        self.tableWidget = QtWidgets.QTableWidget(self.bgwidget)
        self.tableWidget.setGeometry(QtCore.QRect(260, 180, 1101, 461))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(10, item)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Elenco dei clienti"))
        self.btnModifica.setText(_translate("Dialog", "Modifica"))
        self.btnCancella.setText(_translate("Dialog", "Cancella"))
        self.btnAggiungi.setText(_translate("Dialog", "Aggiungi"))
        self.btnEsci.setText(_translate("Dialog", "Esci"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "0"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "1"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "2"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "3"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "4"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "5"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "6"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "7"))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("Dialog", "8"))
        item = self.tableWidget.horizontalHeaderItem(9)
        item.setText(_translate("Dialog", "9"))
        item = self.tableWidget.horizontalHeaderItem(10)
        item.setText(_translate("Dialog", "10"))
import source_rc