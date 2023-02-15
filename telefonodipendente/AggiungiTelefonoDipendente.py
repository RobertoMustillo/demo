
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiTelefonoDipendente(QDialog):
    def __init__(self):
        super(AggiungiTelefonoDipendente, self).__init__()
        loadUi("telefonodipendente/aggiungitelefonodipendente.ui",self)
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

            telefono = self.telefono.text()
            dipendente = self.dipendente.currentText()

            # effettuo controllo di non nullità
            if dipendente == "" or telefono == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif  telefono.isnumeric():
                    # Generazione del cursore
                    cursore = db.cursor()
                    query = "INSERT INTO telefonodipendente (Numero,Dipendente) VALUES ('" + telefono + "', '" + dipendente + "');"
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
        from telefonodipendente.TelefonoDipendente import TelefonoDipendente
        telefonodipendente = TelefonoDipendente()
        self.window().close()
        self.widget.addWidget(telefonodipendente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)