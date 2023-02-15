from datetime import datetime

import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaManutenzione(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaManutenzione, self).__init__()
        loadUi("manutenzione/modificamanutenzione.ui",self)
        self.elemento_selezionato = elemento_selezionato
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_elemento)

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
            date1 = self.date1.date().toString("yyyy-MM-dd")
            date2 = self.date2.text()
            stato = self.stato.text()
            tipo = self.tipo.text()
            dipendente = self.dipendente.currentText()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID del cliente selezionato
            query = "select * from manutenzione"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            # prendo il codice selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            if (date2 == "" or date2 =="None"):
                self.query2 = "UPDATE `manutenzione` SET `CodManutenzione` = '" + id + "', `DataPianificazione` = '" + date1 + "', `DataCompletamento` = NULL, `Stato` = '" + stato + "', `Descrizione` = '" + descrizione + "', `Tipo` = '" + tipo + "', `Dipendente` = '" + dipendente + "' WHERE `CodManutenzione` = " + codice_sel.__str__() + ";"

            else:
                date2 = datetime.strptime(date2, '%Y-%m-%d').date()
                self.query2 = "UPDATE `manutenzione` SET `CodManutenzione` = '" + id + "', `DataPianificazione` = '" + date1 + "', `DataCompletamento` = '" + date2.__str__() + "', `Stato` = '" + stato + "', `Descrizione` = '" + descrizione + "', `Tipo` = '" + tipo + "', `Dipendente` = '" + dipendente + "' WHERE `CodManutenzione` = " + codice_sel.__str__() + ";"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci una data corretta (yyyy-mm-dd).', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from manutenzione.Manutenzione import Manutenzione
        manutenzione = Manutenzione()
        self.window().close()
        self.widget.addWidget(manutenzione)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)