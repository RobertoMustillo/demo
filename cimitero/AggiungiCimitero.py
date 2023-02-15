import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiCimitero(QDialog):
    def __init__(self):
        super(AggiungiCimitero, self).__init__()
        loadUi("cimitero/aggiungicimitero.ui",self)
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

            nome = self.nome.text()
            canone = self.canone.text()
            capienza = self.capienza.text()
            posti = self.posti.text()
            cap=self.cap.text()
            via=self.via.text()

            # Generazione del cursore
            cursore = db.cursor()
            query = "INSERT INTO cimitero (Nome, CAP ,Via, CanoneAnnuo, Capienza, PostiLiberi) VALUES ('"+nome+"', '"+cap+"','"+via+"', '"+canone+"', '"+capienza+"', '"+posti+"');"
            cursore.execute(query)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, ricontrolla i dati.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from cimitero.Cimitero import Cimitero
        cimitero = Cimitero()
        self.window().close()
        self.widget.addWidget(cimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)