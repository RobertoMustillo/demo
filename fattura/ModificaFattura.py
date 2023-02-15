from datetime import datetime

import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaFattura(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaFattura, self).__init__()
        loadUi("fattura/modificafattura.ui",self)
        self.elemento_selezionato = elemento_selezionato
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_elemento)

        self.widget = QtWidgets.QStackedWidget()

    def modifica_elemento(self):
        try:
            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )

            id = self.id.text()
            descrizione = self.descrizione.text()
            emissione = self.emissione.date().toString("yyyy-MM-dd")
            scadenza = self.scadenza.date().toString("yyyy-MM-dd")
            pagamento = self.pagamento.text()
            totale = self.totale.text()

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
            codice_sel = self.codici[self.elemento_selezionato]
            if pagamento == "" or pagamento == "None":
                self.query2 = "UPDATE `fattura` SET `NumeroFattura` = '" + id + "', `DataEmissione` = '" + emissione + "', `DataScadenza` = '" + scadenza + "', `DataPagamento` = NULL, `Descrizione` = '" + descrizione + "', `TotaleFattura` = '" + totale + "' WHERE `NumeroFattura` = " + codice_sel.__str__() + ";"

            elif totale == "" or totale == "None":
                self.query2 = "UPDATE `fattura` SET `NumeroFattura` = '" + id + "', `DataEmissione` = '" + emissione + "', `DataScadenza` = '" + scadenza + "', `DataPagamento` = '" + pagamento.__str__() + "' , `Descrizione` = '" + descrizione + "', `TotaleFattura` = NULL WHERE `NumeroFattura` = " + codice_sel.__str__() + ";"

          #  if (totale == "" or totale == "None") and (pagamento == "" or pagamento == "None"):
           #     self.query2 = "UPDATE `fattura` SET `NumeroFattura` = '" + id + "', `DataEmissione` = '" + emissione + "', `DataScadenza` = '" + scadenza + "', `DataPagamento` = NULL , `Descrizione` = '" + descrizione + "', `TotaleFattura` = NULL WHERE `NumeroFattura` = " + codice_sel.__str__() + ";"

            else:
                pagamento = datetime.strptime(pagamento, '%Y-%m-%d').date()
                self.query2 = "UPDATE `fattura` SET `NumeroFattura` = '" + id + "', `DataEmissione` = '" + emissione + "', `DataScadenza` = '" + scadenza + "', `DataPagamento` = '" + pagamento.__str__() + "', `Descrizione` = '" + descrizione + "', `TotaleFattura` = '" + totale + "' WHERE `NumeroFattura` = " + codice_sel.__str__() + ";"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati o inserisci una data corretta (yyyy-mm-dd).', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from fattura.Fattura import Fattura
        fattura = Fattura()
        self.window().close()
        self.widget.addWidget(fattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)