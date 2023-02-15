
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiAggiuntaServizio(QDialog):
    def __init__(self):
        super(AggiungiAggiuntaServizio, self).__init__()
        loadUi("aggiuntaservizio/aggiungiaggiuntaservizio.ui",self)
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
        query = "SELECT Tipo FROM `db_illuminazione_votiva`.`servizioaggiuntivo`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        #aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.codici = []
        for x in result:
            self.codici.append(x[0])
        self.servizio.addItems(self.codici)

        query2 = "SELECT CodDefunto FROM `db_illuminazione_votiva`.`defunto` ORDER BY `defunto`.`CodDefunto` ASC;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.cod_defunti = []
        for x in result2:
            self.cod_defunti.append(str(x[0]))
        self.defunto.addItems(self.cod_defunti)

    def funz_aggiungi(self):
        try:

            servizio = self.servizio.currentText()
            defunto = self.defunto.currentText()

            # effettuo controllo di non nullità
            if defunto == "" or servizio == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif  defunto.isnumeric():
                    # Generazione del cursore
                    cursore = self.db.cursor()
                    query = "INSERT INTO aggiuntaservizio (Defunto, ServizioAggiuntivo) VALUES ('" + defunto + "', '" + servizio + "');"
                    cursore.execute(query)
                    self.db.commit()
                    self.funz_esci()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci il codice Dipendente in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from aggiuntaservizio.AggiuntaServizio import AggiuntaServizio
        aggiuntaservizio = AggiuntaServizio()
        self.window().close()
        self.widget.addWidget(aggiuntaservizio)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)