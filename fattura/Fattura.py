from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMessageBox

import mysql.connector

from fattura.AggiungiFattura import AggiungiFattura
from fattura.ModificaFattura import ModificaFattura


class Fattura(QDialog):
    def __init__(self):
        super(Fattura, self).__init__()
        loadUi("fattura/fattura2.ui",self)
        self.tableWidget.setEditTriggers(self.tableWidget.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["NumeroFattura", "Data Emissione", "Data Scadenza", "Data Pagamento","Descrizione","TotaleFattua"])
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 150)
        self.tableWidget.setColumnWidth(3, 150)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setColumnWidth(5, 100)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

       # self.image.setPixmap(QPixmap('sfondo.png'))

        #self.tableWidget.resizeColumnsToContents()
        self.loaddata()
        self.btnAggiungi.clicked.connect(self.goto_aggiungi)
        self.btnCancella.clicked.connect(self.funz_cancella)
        self.btnEsci.clicked.connect(self.funz_esci)
        self.btnModifica.clicked.connect(self.goto_modifica)
        self.aggiorna.clicked.connect(self.aggiorna_totale)

        self.widget = QtWidgets.QStackedWidget()

    def goto_aggiungi(self):
        add = AggiungiFattura()
        self.widget.addWidget(add)
        self.window().close()
        #self.widget.showMaximized()
        self.widget.show()
        self.widget.setFixedSize(700, 500)
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_modifica(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

            self.mod = ModificaFattura(self.selected)
            self.popola_lineEdit()
            self.window().close()
            self.widget.addWidget(self.mod)
            # self.widget.showMaximized()
            self.widget.show()
            self.widget.setFixedSize(700, 500)
            self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una fattura da modificare.', QMessageBox.Ok,
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
            query = "select * from fattura"
            cursore.execute(query)
            result = cursore.fetchall()

            #popolo le line Edit con i dati selezionati
            self.mod.id.setText(str(result[self.selected][0]))
            self.mod.emissione.setDate(result[self.selected][1])
            self.mod.scadenza.setDate(result[self.selected][2])
            self.mod.pagamento.setText(str(result[self.selected][3]))
            self.mod.descrizione.setText(str(result[self.selected][4]))
            self.mod.totale.setText(str(result[self.selected][5]))

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
        query = "select * from fattura"
        cursore.execute(query)
        result = cursore.fetchall()

        tablerow = 0
        #results = cursore.execute(query)
        self.tableWidget.setRowCount(len(result))
        for row in result:
            self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1].strftime('%Y-%m-%d')))
            self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2].strftime('%Y-%m-%d')))
            self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(row[4])))
            self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(row[5])))
            tablerow += 1

    def aggiorna_totale(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()

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
            query = "select * from fattura"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            # prendo il codice cliente selezionato
            codice_sel = self.codici[self.selected]
            #vedo se la fattura ha un servizio da sommare
            fattura_servizio_sql = "SELECT * FROM `emissionefatturaservizio` " \
                                   "WHERE Fattura = " + codice_sel.__str__() + ";"
            cursore.execute(fattura_servizio_sql)
            values = cursore.fetchall()
            print(values)
            #se la query è nulla la fattura è senza servizio
            if not values:
                print("senza serv")
                upd_no_servizio ="UPDATE fattura SET TotaleFattura = (SELECT sum(e.CanoneAnnuo) + sum(e.CostoAllaccio) " \
                                 "FROM emissionefattura e " \
                                 "WHERE e.Fattura = " + codice_sel.__str__() + ") " \
                                                                               "WHERE NumeroFattura = " + codice_sel.__str__() + ";"
                cursore.execute(upd_no_servizio)
                db.commit()
            elif values: #è con servizio
                print("è con servizio")

                # verifica se la fattura ha solo servizi
                fattura_solo_servizio_sql = "SELECT * FROM `emissionefattura` " \
                                            "WHERE Fattura = " + codice_sel.__str__() + ";"
                cursore.execute(fattura_solo_servizio_sql)
                # se la query è nulla la fattura ha solo servizi
                if not cursore.fetchall():
                    print("è solo servizio")
                    upd_tot = "UPDATE fattura SET TotaleFattura = (SELECT sum(s.Prezzo) FROM servizioaggiuntivo s, emissionefatturaservizio es " \
                              " WHERE es.Fattura = " + codice_sel.__str__() + " and s.Tipo = es.ServizioAggiuntivo) WHERE NumeroFattura = " + codice_sel.__str__() + ";"
                    cursore.execute(upd_tot)
                    db.commit()
                else: # la fattura ha tutti e 3

                    print("canone+allacc+serv")

                    #trovo la somma dei canoni
                    somma_canone_allacci = "SELECT  sum(e.CanoneAnnuo) + sum(e.CostoAllaccio) " \
                                           "FROM emissionefattura e " \
                                           "WHERE e.Fattura = " + codice_sel.__str__() + ";"
                    cursore.execute(somma_canone_allacci)
                    somma1 = float(cursore.fetchone()[0])

                    #trovo la somma dei servizi
                    somma_servizi = "SELECT  sum(s.Prezzo) " \
                                    "FROM emissionefatturaservizio es , servizioaggiuntivo s " \
                                    "WHERE es.Fattura = " + codice_sel.__str__() + " and s.Tipo=es.ServizioAggiuntivo;"
                    cursore.execute(somma_servizi)
                    somma2 = float(cursore.fetchone()[0])
                    somma3=somma2+somma1

                    upd_tot="UPDATE fattura SET TotaleFattura = '" +somma3.__str__()+"' WHERE NumeroFattura = " + codice_sel.__str__() + ";"
                    cursore.execute(upd_tot)
                    db.commit()



            self.loaddata()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una fattura di cui AGGIORNARE il totale automaticamente.', QMessageBox.Ok,
                                 QMessageBox.Ok)
    def funz_cancella(self):
        try:
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare la fattura selezionato? <p>OPERAZIONE IRREVERSIBILE",
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
                query = "select * from fattura"
                cursore.execute(query)
                result = cursore.fetchall()

                #creo un array di codici
                self.codici = []
                for x in result:
                    self.codici.append(x[0])

                #prendo il codice selezionato
                codiceSel = self.codici[self.selected]
                query2 = "DELETE FROM `fattura` WHERE `fattura`.`NumeroFattura` ='" + codiceSel.__str__()+"';"
                cursore.execute(query2)
                db.commit()
                self.loaddata()

            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Seleziona una fattura da eliminare o controlla che questa non sia collegata ad altri dati.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.GestioneClienti import GestioneClienti
        home = GestioneClienti()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)