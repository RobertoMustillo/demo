from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import mysql.connector

from dipendenti.AggiungiDipendente import AggiungiDipendente
from dipendenti.ApriDip import ApriDip
from dipendenti.ModificaDipendente import ModificaDipendente


class Dipendenti(QDialog):
    def __init__(self):
        super(Dipendenti,self).__init__()
        loadUi("dipendenti/dipendenti2.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["ID","CodiceFiscale", "Cognome", "Nome", "DataNascita","Email","Citta"])
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 200)
        self.tableWidget.setColumnWidth(5, 250)
        self.tableWidget.setColumnWidth(6, 200)
        self.tableWidget.setColumnWidth(7, 200)
        self.tableWidget.setColumnWidth(9, 200)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
       # self.image.setPixmap(QPixmap('sfondo.png'))


        #self.tableWidget.resizeColumnsToContents()
        self.loaddata()
        self.btnApri.clicked.connect(self.goto_apri_dip)
        self.btnAggiungi.clicked.connect(self.goto_aggiungi)
        self.btnCancella.clicked.connect(self.funz_cancella)
        self.btnEsci.clicked.connect(self.funz_esci)
        self.btnModifica.clicked.connect(self.goto_modifica)

        self.widget = QtWidgets.QStackedWidget()

    def goto_apri_dip(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.apridip = ApriDip(self.selected)
            self.popola_dip()
            self.window().close()
            self.widget.addWidget(self.apridip)
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da aprire.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def goto_aggiungi(self):
        addDip = AggiungiDipendente()
        self.widget.addWidget(addDip)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.modDip = ModificaDipendente(self.selected)
            self.popola_lineEdit()
            self.window().close()
            self.widget.addWidget(self.modDip)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un dipendente da modificare.', QMessageBox.Ok,
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
            # cerco l'ID selezionato
            query = "select * from dipendente"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati del cliente selezionato
            self.modDip.id.setText(str(result[self.selected][0]))
            self.modDip.cf.setText(result[self.selected][1])
            self.modDip.cognome.setText(result[self.selected][2])
            self.modDip.nome.setText(result[self.selected][3])
            self.modDip.dateEdit.setDate(result[self.selected][4])
            self.modDip.iban.setText(result[self.selected][5])
            self.modDip.email.setText(result[self.selected][6])
            self.modDip.citta.setText(result[self.selected][7])
            self.modDip.cap.setText(result[self.selected][8])
            self.modDip.via.setText(result[self.selected][9])
            self.modDip.numerocivico.setText(result[self.selected][10])

    def popola_dip(self):
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
            # cerco l'ID selezionato
            query = "select * from dipendente"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati del cliente selezionato
            self.apridip.id.setText(str(result[self.selected][0]))
            self.apridip.cf.setText(result[self.selected][1])
            self.apridip.cognome.setText(result[self.selected][2])
            self.apridip.nome.setText(result[self.selected][3])
            self.apridip.dateEdit.setDate(result[self.selected][4])
            self.apridip.iban.setText(result[self.selected][5])
            self.apridip.email.setText(result[self.selected][6])
            self.apridip.citta.setText(result[self.selected][7])
            self.apridip.cap.setText(result[self.selected][8])
            self.apridip.via.setText(result[self.selected][9])
            self.apridip.numerocivico.setText(result[self.selected][10])

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
        query = "select * from dipendente"
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
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4].strftime('%d/%m/%Y')))
            self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[6]))
            self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[7]))
            tablerow += 1

    def funz_cancella(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            #print(self.selected)
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare il dipendente selezionato? <p>OPERAZIONE IRREVERSIBILE",
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
                query = "select * from dipendente"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codici
                self.codici = []
                for x in result:
                    self.codici.append(x[0])

                #prendo il codice selezionato
                codiceSel = self.codici[self.selected]
                query2 = "DELETE FROM dipendente WHERE CodDipendente = "+codiceSel.__str__()+";"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un dipendente da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneDipendenti import GestioneDipendenti
        home = GestioneDipendenti()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)