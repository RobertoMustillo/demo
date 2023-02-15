from datetime import datetime

import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaEvento(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaEvento, self).__init__()
        loadUi("eventi/modificaevento.ui",self)
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
        query = "SELECT CodCliente FROM `db_illuminazione_votiva`.`cliente`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # aggiungo le chiavi esterne alla comboBox
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.cliente.addItems(self.codici)

        query2 = "SELECT CodDefunto FROM `db_illuminazione_votiva`.`defunto` ORDER BY `defunto`.`CodDefunto` ASC;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        self.cod_defunti = []
        for x in result2:
            self.cod_defunti.append(str(x[0]))
        self.defunto.addItems(self.cod_defunti)

    def modifica_elemento(self):
        try:

            id = self.id.text()
            descrizione = self.descrizione.text()
            allaccio = self.allaccio.date().toString("yyyy-MM-dd")
            #distacco = self.distacco.date().toString("yyyy-MM-dd")
            distacco = self.distacco.text()
            cliente = self.cliente.currentText()
            defunto = self.defunto.currentText()

            # Generazione del cursore
            cursore = self.db.cursor()
            # cerco l'ID del cliente selezionato
            query = "select * from evento"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            # prendo il codice cliente selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            #print(codiceClienteSel)
            if (distacco == "" or distacco=="None"):
                # distacco = None
                self.query2 = "UPDATE `evento` SET `CodEvento` = '" + id + "', `Descrizione` = '" + descrizione + "', `DataAllaccio` = '" + allaccio + "', `DataDistacco` = NULL, `Cliente` = '" + cliente + "', `Defunto` = '" + defunto + "' WHERE `CodEvento` = " + codice_sel.__str__() + ";"

            else:
                distacco = datetime.strptime(distacco, '%Y-%m-%d').date()
                self.query2 = "UPDATE `evento` SET `CodEvento` = '" + id + "', `Descrizione` = '" + descrizione + "', `DataAllaccio` = '" + allaccio + "', `DataDistacco` = '" + distacco.__str__() + "', `Cliente` = '" + cliente + "', `Defunto` = '" + defunto + "' WHERE `CodEvento` = " + codice_sel.__str__() + ";"

            cursore.execute(self.query2)
            self.db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci una data corretta (yyyy-mm-dd).', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from eventi.Evento import Evento
        evento = Evento()
        self.window().close()
        self.widget.addWidget(evento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)