from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import mysql.connector

from defunti.AggiungiDefunto import AggiungiDefunto
from defunti.ModificaDefunto import ModificaDefunto


class DefuntiScreen(QDialog):
    def __init__(self):
        super(DefuntiScreen,self).__init__()
        loadUi("defunti/def5.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Cognome", "Nome", "Data di nascita","Data decesso","Luogo di nascita","Cimitero","Ubicazione"])
        self.tableWidget.setColumnWidth(0, 50)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 130)
        self.tableWidget.setColumnWidth(5, 130)
        self.tableWidget.setColumnWidth(6, 150)
        self.tableWidget.setColumnWidth(7, 80)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

        #self.image.setPixmap(QPixmap('sfondo.png'))
        #self.image.setGeometry(0,0,1440,1000)


        #self.tableWidget.resizeColumnsToContents()
        self.loaddata()
        self.btnAggiungi.clicked.connect(self.goto_aggiungi)
        self.btnCancella.clicked.connect(self.cancella)
        self.btnEsci.clicked.connect(self.funz_esci)
        self.btnModifica.clicked.connect(self.goto_modifica)

        self.widget = QtWidgets.QStackedWidget()

    def goto_aggiungi(self):
        addDefunto = AggiungiDefunto()
        self.widget.addWidget(addDefunto)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            self.moddefunto = ModificaDefunto(self.selected)
            self.popola_lineEdit()
    #        modcliente.nome.setText("ciao")
            self.window().close()
            self.widget.addWidget(self.moddefunto)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un defunto da modificare.', QMessageBox.Ok,
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
            query = "select * from defunto"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati del cliente selezionato
            self.moddefunto.cognome.setText(result[self.selected][1])
            self.moddefunto.nome.setText(result[self.selected][2])
            self.moddefunto.dateN.setDate(result[self.selected][3])
            self.moddefunto.dateD.setDate(result[self.selected][4])
            self.moddefunto.luogon.setText(result[self.selected][5])
            self.moddefunto.comboBox.setCurrentText(result[self.selected][6])
            self.moddefunto.ubicazione.setText(result[self.selected][7])

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
        query = "select * from defunto"
        cursore.execute(query)
        result = cursore.fetchall()

        tablerow = 0
        #results = cursore.execute(query)
        self.tableWidget.setRowCount(len(result))
        for row in result:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3].strftime('%d/%m/%Y')))
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4].strftime('%d/%m/%Y')))
            self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
            self.tableWidget.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(row[7]))
            tablerow += 1

    def cancella(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            #print(self.selected)
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
                #cerco l'ID del cliente selezionato
                query = "select * from defunto"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codici
                self.codici = []
                for x in result:
                    #print(x[0])
                    self.codici.append(x[0])

                #print(self.codClienti)
                #print(self.codClienti[self.selected])

                #prendo il codice selezionato
                codiceSel = self.codici[self.selected]
                #print(codiceSel)
                query2 = "DELETE FROM defunto WHERE CodDefunto = "+codiceSel.__str__()+";"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un defunto da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneCimiteri import GestioneCimiteri
        home = GestioneCimiteri()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)