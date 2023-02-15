from datetime import datetime

import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiEvento(QDialog):
    def __init__(self):
        super(AggiungiEvento, self).__init__()
        loadUi("eventi/aggiungievento.ui",self)
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

    def funz_aggiungi(self):
        try:
            descrizione = self.descrizione.text()
            allaccio = self.allaccio.date().toString("yyyy-MM-dd")
            distacco = self.distacco.text()
            cliente = self.cliente.currentText()
            defunto = self.defunto.currentText()
            if(distacco==""):
                #distacco = None
                self.query = "INSERT INTO evento (Descrizione, DataAllaccio, Cliente, Defunto) VALUES ('" + descrizione + "', '" + allaccio + "', '" + cliente + "', '" + defunto + "');"

            else:
                distacco = datetime.strptime(distacco, '%d/%m/%Y').date()
                self.query = "INSERT INTO evento (Descrizione, DataAllaccio, DataDistacco, Cliente, Defunto) VALUES ('" + descrizione + "', '" + allaccio + "', '" + distacco.__str__() + "', '" + cliente + "', '" + defunto + "');"

            # effettuo controlloo di non nullità
            if descrizione == "" or cliente == "" or defunto == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif cliente.isnumeric() and defunto.isnumeric():
                    # Generazione del cursore
                    cursore = self.db.cursor()
                    #query = "INSERT INTO evento (Descrizione, DataAllaccio, DataDistacco, Cliente, Defunto) VALUES ('"+descrizione+"', '"+allaccio+"', '"+distacco.__str__()+"', '"+cliente+"', '"+defunto+"');"
                    cursore.execute(self.query)
                    self.db.commit()
                    self.funz_esci()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci i codici in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci una data corretta (dd/mm/yyyy).', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from eventi.Evento import Evento
        evento = Evento()
        self.window().close()
        self.widget.addWidget(evento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)