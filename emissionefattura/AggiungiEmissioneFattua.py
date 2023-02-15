
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiEmissioneFattura(QDialog):
    def __init__(self):
        super(AggiungiEmissioneFattura, self).__init__()
        loadUi("emissionefattura/aggiungiemissionefattura.ui",self)
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

        query2 = "SELECT CodEvento FROM `db_illuminazione_votiva`.`evento` ORDER BY `evento`.`CodEvento` ASC;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        self.cod_eventi = []
        for x in result2:
            self.cod_eventi.append(str(x[0]))
        self.evento.addItems(self.cod_eventi)

    def funz_aggiungi(self):
        try:

            fattura = self.fattura.currentText()
            evento = self.evento.currentText()
            canone = self.canone.text()
            allaccio = self.allaccio.text()

            # effettuo controllo di non nullità
            if evento == "" or fattura == "" or canone == "" or allaccio == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif evento.isnumeric():
                    # Generazione del cursore
                    cursore = self.db.cursor()
                    query = "INSERT INTO emissionefattura (Fattura, Evento, CanoneAnnuo, CostoAllaccio) VALUES ('" + fattura + "', '" + evento + "', '" + canone + "', '" + allaccio + "');"
                    cursore.execute(query)
                    self.db.commit()
                    #self.funz_esci()

                    QMessageBox.information(self, 'Info', 'Ricorda di aggiornare il TOTALE FATTURA!',
                                         QMessageBox.Ok, QMessageBox.Ok)
                    self.goto_fattura()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci il costo in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from emissionefattura.EmissioneFattura import EmissioneFattura
        emissionefattura = EmissioneFattura()
        self.window().close()
        self.widget.addWidget(emissionefattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_fattura(self):
        from fattura.Fattura import Fattura
        fattura = Fattura()
        self.window().close()
        self.widget.addWidget(fattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)