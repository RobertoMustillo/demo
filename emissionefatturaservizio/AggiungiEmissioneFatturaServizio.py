
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiEmissioneFatturaServizio(QDialog):
    def __init__(self):
        super(AggiungiEmissioneFatturaServizio, self).__init__()
        loadUi("emissionefatturaservizio/aggiungiemissionefatturaservizio.ui",self)
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
        query = "SELECT NumeroFattura FROM `db_illuminazione_votiva`.`fattura`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        #popolo la comboBox
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.fattura.addItems(self.codici)

        query2 = "SELECT Tipo FROM `db_illuminazione_votiva`.`servizioaggiuntivo`;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        self.cod_servizi = []
        for x in result2:
            self.cod_servizi.append(str(x[0]))
        self.servizio.addItems(self.cod_servizi)

    def funz_aggiungi(self):
        try:

            fattura = self.fattura.currentText()
            servizio = self.servizio.currentText()

            # effettuo controllo di non nullità
            if servizio == "" or fattura == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            else:
                    # Generazione del cursore
                    cursore = self.db.cursor()
                    query = "INSERT INTO emissionefatturaservizio (Fattura, ServizioAggiuntivo) VALUES ('" + fattura + "', '" + servizio + "');"
                    cursore.execute(query)
                    self.db.commit()
                    #self.funz_esci()

                    QMessageBox.information(self, 'Info', 'Ricorda di aggiornare il TOTALE FATTURA!',
                                            QMessageBox.Ok, QMessageBox.Ok)
                    self.goto_fattura()

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from emissionefatturaservizio.EmissioneFatturaServizio import EmissioneFatturaServizio
        emissionefatturaservizio = EmissioneFatturaServizio()
        self.window().close()
        self.widget.addWidget(emissionefatturaservizio)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_fattura(self):
        from fattura.Fattura import Fattura
        fattura = Fattura()
        self.window().close()
        self.widget.addWidget(fattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)