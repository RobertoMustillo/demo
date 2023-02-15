from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import mysql.connector

from cimitero.AggiungiCimitero import AggiungiCimitero
from cimitero.ModificaCimitero import ModificaCimitero


class Cimitero(QDialog):
    def __init__(self):
        super(Cimitero, self).__init__()
        loadUi("cimitero/cimitero2.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["Nome", "CAP", "Via", "Canone Annuo","Capienza","Posti liberi"])
        self.tableWidget.setColumnWidth(0, 150)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 150)
        self.tableWidget.setColumnWidth(5, 150)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

       # self.image.setPixmap(QPixmap('sfondo.png'))

        #self.tableWidget.resizeColumnsToContents()
        self.loaddata()
        self.btnAggiungi.clicked.connect(self.goto_aggiungi)
        self.btnCancella.clicked.connect(self.funz_cancella)
        self.btnEsci.clicked.connect(self.funz_esci)
        self.btnModifica.clicked.connect(self.goto_modifica)
        self.aggiorna.clicked.connect(self.aggiorna_posti_liberi)

        self.widget = QtWidgets.QStackedWidget()

    def goto_aggiungi(self):
        add = AggiungiCimitero()
        self.widget.addWidget(add)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.mod = ModificaCimitero(self.selected)
            self.popola_lineEdit()
            self.window().close()
            self.widget.addWidget(self.mod)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cimitero da modificare.', QMessageBox.Ok,
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
            query = "select * from cimitero"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati selezionati
            self.mod.nome.setText(result[self.selected][0])
            self.mod.cap.setText(result[self.selected][1])
            self.mod.via.setText(result[self.selected][2])
            self.mod.canone.setText(str(result[self.selected][3]))
            self.mod.capienza.setText(str(result[self.selected][4]))
            self.mod.posti.setText(str(result[self.selected][5]))

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
        query = "select * from cimitero"
        cursore.execute(query)
        result = cursore.fetchall()

        tablerow = 0
        #results = cursore.execute(query)
        self.tableWidget.setRowCount(len(result))
        for row in result:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow += 1

    def aggiorna_posti_liberi(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

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
            query = "select * from cimitero"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            # prendo il codice selezionato
            codice_sel = self.codici[self.selected]
            upd_posti_liberi = "UPDATE cimitero SET cimitero.PostiLiberi = (SELECT (c1.Capienza - (SELECT COUNT(d.CodDefunto) FROM defunto d WHERE d.Cimitero = '" + codice_sel.__str__() + "')) " \
                               "FROM (SELECT * FROM cimitero) as c1 " \
                               "WHERE c1.Nome = '" + codice_sel.__str__() + "') " \
                               "WHERE cimitero.Nome = '" + codice_sel.__str__() + "';"
            cursore.execute(upd_posti_liberi)
            db.commit()
            self.loaddata()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cimitero da aggiornare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_cancella(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare il cimitero selezionato? <p>OPERAZIONE IRREVERSIBILE",
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
                query = "select * from cimitero"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codici
                self.codici = []
                for x in result:
                    self.codici.append(x[0])

                #prendo il codice selezionato
                codiceSel = self.codici[self.selected]
                query2 = "DELETE FROM `cimitero` WHERE `cimitero`.`Nome` ='" + codiceSel.__str__()+"';"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cimitero da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneCimiteri import GestioneCimiteri
        home = GestioneCimiteri()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)