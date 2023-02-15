from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import mysql.connector

from associazionecimitero.AggiungiAssociazioneCimitero import AggiungiAssociazioneCimitero
from associazionecimitero.ModificaAssociazioneCimitero import ModificaAssociazioneCimitero


class AssociazioneCimitero(QDialog):
    def __init__(self):
        super(AssociazioneCimitero, self).__init__()
        loadUi("associazionecimitero/associazionecimitero2.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["Manutenzione","Cimitero"])
        self.tableWidget.setColumnWidth(0, 250)
        self.tableWidget.setColumnWidth(1, 200)
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
        add = AggiungiAssociazioneCimitero()
        self.widget.addWidget(add)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.mod = ModificaAssociazioneCimitero(self.selected)
            self.popola_lineEdit()
            self.window().close()
            self.widget.addWidget(self.mod)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona cosa modificare.', QMessageBox.Ok,
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
            query = "select * from associazionecimitero"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati selezionati
            self.mod.manutenzione.setCurrentText(str(result[self.selected][0]))
            self.mod.cimitero.setCurrentText(str(result[self.selected][1]))

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
        query = "select * from associazionecimitero"
        cursore.execute(query)
        result = cursore.fetchall()

        tablerow = 0
        #results = cursore.execute(query)
        self.tableWidget.setRowCount(len(result))
        for row in result:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            tablerow += 1

    def funz_cancella(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare l'elemento selezionato? <p>OPERAZIONE IRREVERSIBILE",
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
                query = "select * from associazionecimitero"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codici
                self.manutenzioni = []
                for x in result:
                    self.manutenzioni.append(x[0])

                self.cimiteri = []
                for x in result:
                    self.cimiteri.append(x[1])

                #prendo il codice selezionato
                codiceSel = self.cimiteri[self.selected]
                man_sel = self.manutenzioni[self.selected]

                query2 = "DELETE FROM `associazionecimitero` WHERE `associazionecimitero`.`Manutenzione` = '" + man_sel.__str__()+ "' AND `associazionecimitero`.`Cimitero` = '"+ codiceSel.__str__()+ "';"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona cosa vuoi eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneCimiteri import GestioneCimiteri
        home = GestioneCimiteri()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)