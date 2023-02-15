from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox, QHeaderView

import mysql.connector

from clienti.AggiungiCliente import AggiungiCliente
from clienti.ApriCliente import ApriCliente
from clienti.ModificaCliente import ModificaCliente


class ClientiScreen(QDialog):
    def __init__(self):
        super(ClientiScreen,self).__init__()
        loadUi("clienti/clienti3.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["ID","CodiceFiscale", "Cognome", "Nome","Email","Citta"])
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.loaddata()
        self.apri.clicked.connect(self.goto_apri_cliente)
        self.btnAggiungi.clicked.connect(self.goto_aggiungi_cliente)
        self.btnCancella.clicked.connect(self.cancella_cliente)
        self.btnEsci.clicked.connect(self.funz_esci)
        self.btnModifica.clicked.connect(self.goto_modifica_cliente)

        self.widget = QtWidgets.QStackedWidget()

    def goto_apri_cliente(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.apricliente = ApriCliente(self.selected)
            self.popola_cliente()
            self.window().close()
            self.widget.addWidget(self.apricliente)
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da aprire.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def goto_aggiungi_cliente(self):
        addcliente = AggiungiCliente()
        self.widget.addWidget(addcliente)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica_cliente(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.modcliente = ModificaCliente(self.selected)
            self.popola_lineEdit()
            self.window().close()
            self.widget.addWidget(self.modcliente)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da modificare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def popola_lineEdit(self):
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            # print(self.selected)

            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )
            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID del cliente selezionato
            query = "select * from cliente"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati del cliente selezionato
            self.modcliente.id.setText(str(result[self.selected][0]))
            self.modcliente.cf.setText(result[self.selected][1])
            self.modcliente.cognome.setText(result[self.selected][2])
            self.modcliente.nome.setText(result[self.selected][3])
            self.modcliente.dateEdit.setDate(result[self.selected][4])
            self.modcliente.comboBox.setCurrentText(result[self.selected][5])
            self.modcliente.email.setText(result[self.selected][6])
            self.modcliente.citta.setText(result[self.selected][7])
            self.modcliente.cap.setText(result[self.selected][8])
            self.modcliente.via.setText(result[self.selected][9])
            self.modcliente.numerocivico.setText(result[self.selected][10])

    def popola_cliente(self):
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            # print(self.selected)

            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )
            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID del cliente selezionato
            query = "select * from cliente"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati del cliente selezionato
            self.apricliente.id.setText(str(result[self.selected][0]))
            self.apricliente.cf.setText(result[self.selected][1])
            self.apricliente.cognome.setText(result[self.selected][2])
            self.apricliente.nome.setText(result[self.selected][3])
            self.apricliente.dateEdit.setDate(result[self.selected][4])
            self.apricliente.comboBox.setCurrentText(result[self.selected][5])
            self.apricliente.email.setText(result[self.selected][6])
            self.apricliente.citta.setText(result[self.selected][7])
            self.apricliente.cap.setText(result[self.selected][8])
            self.apricliente.via.setText(result[self.selected][9])
            self.apricliente.numerocivico.setText(result[self.selected][10])

    def loaddata(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        # Generazione del cursore
        cursore = db.cursor()
        query = "select * from cliente"
        cursore.execute(query)
        result = cursore.fetchall()

        tablerow = 0
        #results = cursore.execute(query)
        self.tableWidget.setRowCount(len(result))
        for row in result:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
            #self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4].strftime('%d/%m/%Y')))
            #self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[6]))
            self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[7]))
            #self.tableWidget.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(row[8]))
            #self.tableWidget.setItem(tablerow, 9, QtWidgets.QTableWidgetItem(row[9]))
            #self.tableWidget.setItem(tablerow, 10, QtWidgets.QTableWidgetItem(row[10]))
            tablerow += 1
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def cancella_cliente(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            #print(self.selected)
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare il cliente selezionato? <p>OPERAZIONE IRREVERSIBILE",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                # Test di connessione a MySQL
                db = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="root",
                    database="db_illuminazione_votiva",
                    port=8889
                )
                # Generazione del cursore
                cursore = db.cursor()
                #cerco l'ID del cliente selezionato
                query = "select * from cliente"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codiciClienti
                self.codClienti = []
                for x in result:
                    #print(x[0])
                    self.codClienti.append(x[0])

                #print(self.codClienti)
                #print(self.codClienti[self.selected])

                #prendo il codice cliente selezionato
                codiceClienteSel = self.codClienti[self.selected]
                #print(codiceClienteSel)
                query2 = "DELETE FROM cliente WHERE CodCliente = "+codiceClienteSel.__str__()+";"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneClienti import GestioneClienti
        home = GestioneClienti()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)