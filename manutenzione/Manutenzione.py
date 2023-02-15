from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import mysql.connector

from manutenzione.AggiungiManutenzione import AggiungiManutenzione
from manutenzione.ModificaManutenzione import ModificaManutenzione


class Manutenzione(QDialog):
    def __init__(self):
        super(Manutenzione, self).__init__()
        loadUi("manutenzione/manutenzione2.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["CodManutenzione", "Data Pianificazione", "Data Completamento", "Stato","Descrizione","Tipo","Dipendente"])
        self.tableWidget.setColumnWidth(0, 130)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 200)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        #self.image.setPixmap(QPixmap('sfondo.png'))

        #self.tableWidget.resizeColumnsToContents()
        self.loaddata()
        self.btnAggiungi.clicked.connect(self.goto_aggiungi)
        self.btnCancella.clicked.connect(self.funz_cancella)
        self.btnEsci.clicked.connect(self.funz_esci)
        self.btnModifica.clicked.connect(self.goto_modifica)

        self.widget = QtWidgets.QStackedWidget()

    def goto_aggiungi(self):
        add = AggiungiManutenzione()
        self.widget.addWidget(add)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.mod = ModificaManutenzione(self.selected)
            self.popola_lineEdit()
            self.window().close()
            self.widget.addWidget(self.mod)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una manutenzione da modificare.', QMessageBox.Ok,
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
            query = "select * from manutenzione"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati selezionati
            self.mod.id.setText(str(result[self.selected][0]))
            self.mod.date1.setDate(result[self.selected][1])
            self.mod.date2.setText(str(result[self.selected][2]))
            self.mod.stato.setText(str(result[self.selected][3]))
            self.mod.descrizione.setText(str(result[self.selected][4]))
            self.mod.tipo.setText(str(result[self.selected][5]))
            self.mod.dipendente.setCurrentText(str(result[self.selected][6]))

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
        query = "select * from manutenzione"
        cursore.execute(query)
        result = cursore.fetchall()

        tablerow = 0
        #results = cursore.execute(query)
        self.tableWidget.setRowCount(len(result))
        for row in result:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1].strftime('%Y-%m-%d')))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(row[6])))
            tablerow += 1

    def funz_cancella(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare la manutenzione selezionato? <p>OPERAZIONE IRREVERSIBILE",
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
                #cerco l'ID selezionato
                query = "select * from manutenzione"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codici
                self.codici = []
                for x in result:
                    self.codici.append(x[0])

                #prendo il codice selezionato
                codiceSel = self.codici[self.selected]
                query2 = "DELETE FROM `manutenzione` WHERE `manutenzione`.`CodManutenzione` ='" + codiceSel.__str__()+"';"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una manutenzione da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneCimiteri import GestioneCimiteri
        home = GestioneCimiteri()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)