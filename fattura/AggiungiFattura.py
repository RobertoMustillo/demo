from datetime import datetime

import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiFattura(QDialog):
    def __init__(self):
        super(AggiungiFattura, self).__init__()
        loadUi("fattura/aggiungifattura.ui",self)
        self.annulla.clicked.connect(self.funz_esci)
        self.aggiungi.clicked.connect(self.funz_aggiungi)

        #fornisce uno stack di widget in cui è visibile un solo widget alla volta
        self.widget = QtWidgets.QStackedWidget()

    def funz_aggiungi(self):
        try:
            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )

            descrizione = self.descrizione.text()
            emissione = self.emissione.date().toString("yyyy-MM-dd")
            scadenza = self.scadenza.date().toString("yyyy-MM-dd")
            pagamento = self.pagamento.text()
            totale = self.totale.text()
            if pagamento== "":
                self.query = "INSERT INTO fattura (DataEmissione, DataScadenza, Descrizione, TotaleFattura) VALUES ('" + emissione + "', '" + scadenza + "', '" + descrizione + "', '" + totale + "');"

            else:
                pagamento = datetime.strptime(pagamento, '%d/%m/%Y').date()
                self.query = "INSERT INTO fattura (DataEmissione, DataScadenza, DataPagamento, Descrizione, TotaleFattura) VALUES ('" + emissione + "', '" + scadenza + "', '" + pagamento.__str__() + "', '" + descrizione + "', '" + totale + "');"


            # effettuo controlloo di non nullità
            if descrizione == "" or totale == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            # Generazione del cursore
            cursore = db.cursor()
            #query = "INSERT INTO evento (Descrizione, DataAllaccio, DataDistacco, Cliente, Defunto) VALUES ('"+descrizione+"', '"+allaccio+"', '"+distacco.__str__()+"', '"+cliente+"', '"+defunto+"');"
            cursore.execute(self.query)
            db.commit()
            self.funz_esci()

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati o inserisci una data corretta (dd/mm/yyyy).', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from fattura.Fattura import Fattura
        fattura = Fattura()
        self.window().close()
        self.widget.addWidget(fattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)