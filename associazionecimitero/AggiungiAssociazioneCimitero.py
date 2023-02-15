
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiAssociazioneCimitero(QDialog):
    def __init__(self):
        super(AggiungiAssociazioneCimitero, self).__init__()
        loadUi("associazionecimitero/aggiungiassociazionecimitero.ui",self)
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
        query = "SELECT CodManutenzione FROM `db_illuminazione_votiva`.`manutenzione`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.manutenzione.addItems(self.codici)

        query2 = "SELECT Nome FROM `db_illuminazione_votiva`.`cimitero`;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        self.cimiteri = []
        for x in result2:
            self.cimiteri.append(str(x[0]))
        self.cimitero.addItems(self.cimiteri)

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

            manutenzione = self.manutenzione.currentText()
            cimitero = self.cimitero.currentText()

            # effettuo controllo di non nullità
            if cimitero == "" or manutenzione == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif  manutenzione.isnumeric():
                    # Generazione del cursore
                    cursore = db.cursor()
                    query = "INSERT INTO associazionecimitero (Manutenzione,Cimitero) VALUES ('" + manutenzione + "', '" + cimitero + "');"
                    cursore.execute(query)
                    db.commit()
                    self.funz_esci()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci il codice in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from associazionecimitero.AssociazioneCimitero import AssociazioneCimitero
        associazionecimitero = AssociazioneCimitero()
        self.window().close()
        self.widget.addWidget(associazionecimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)