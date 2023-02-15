from datetime import datetime

import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiManutenzione(QDialog):
    def __init__(self):
        super(AggiungiManutenzione, self).__init__()
        loadUi("manutenzione/aggiungimanutenzione.ui",self)
        self.annulla.clicked.connect(self.funz_esci)
        self.aggiungi.clicked.connect(self.funz_aggiungi)

        #fornisce uno stack di widget in cui è visibile un solo widget alla volta
        self.widget = QtWidgets.QStackedWidget()

        # Test di connessione a MySQL
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )
        self.cursore = self.db.cursor()
        query = "SELECT CodDipendente FROM `db_illuminazione_votiva`.`dipendente`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # aggiungo le chiavi esterne alla comboBox
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.dipendente.addItems(self.codici)

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
            date1 = self.date1.date().toString("yyyy-MM-dd")
            date2 = self.date2.text()
            stato = self.stato.text()
            tipo = self.tipo.text()
            dipendente = self.dipendente.currentText()

            if(date2=="" or date2 =="None"):
                self.query = "INSERT INTO manutenzione (DataPianificazione, DataCompletamento, Stato, Descrizione, Tipo, Dipendente) VALUES ('" + date1 + "', NULL, '" + stato + "', '" + descrizione + "', '" + tipo + "', '" + dipendente + "');"

            else:
                date2 = datetime.strptime(date2, '%d/%m/%Y').date()
                self.query = "INSERT INTO manutenzione (DataPianificazione, DataCompletamento, Stato, Descrizione, Tipo, Dipendente) VALUES ('" + date1 + "', '" + date2.__str__() + "', '" + stato + "', '" + descrizione + "', '" + tipo + "', '" + dipendente + "');"

            # effettuo controlloo di non nullità
            if descrizione == "" or stato == "" or tipo == "" or dipendente=="":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif  dipendente.isnumeric():
                    # Generazione del cursore
                    cursore = db.cursor()
                    cursore.execute(self.query)
                    db.commit()
                    self.funz_esci()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci il codice Dipendente in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci una data corretta (dd/mm/yyyy).', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from manutenzione.Manutenzione import Manutenzione
        manutenzione = Manutenzione()
        self.window().close()
        self.widget.addWidget(manutenzione)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)