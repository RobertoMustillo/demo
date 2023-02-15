
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiServizioAggiuntivo(QDialog):
    def __init__(self):
        super(AggiungiServizioAggiuntivo, self).__init__()
        loadUi("servizioaggiuntivo/aggiungiservizioaggiuntivo.ui",self)
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

            tipo = self.tipo.text()
            prezzo = self.prezzo.text()

            # effettuo controllo di non nullità
            if prezzo == "" or tipo == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif  prezzo.isnumeric():
                    # Generazione del cursore
                    cursore = db.cursor()
                    query = "INSERT INTO servizioaggiuntivo (Tipo, Prezzo) VALUES ('" + tipo + "', '" + prezzo + "');"
                    cursore.execute(query)
                    db.commit()
                    self.funz_esci()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci il prezzo in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from servizioaggiuntivo.ServizioAggiuntivo import ServizioAggiuntivo
        servizioaggiuntivo = ServizioAggiuntivo()
        self.window().close()
        self.widget.addWidget(servizioaggiuntivo)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)