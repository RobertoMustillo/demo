import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiDipendente(QDialog):
    def __init__(self):
        super(AggiungiDipendente, self).__init__()
        loadUi("dipendenti/aggiungidip.ui",self)
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
            cognome = self.cognome.text()
            cf = self.cf.text()
            data = self.dateEdit.date().toString("yyyy-MM-dd")
            email = self.email.text()
            iban = self.iban.text()
            citta=self.citta.text()
            cap=self.cap.text()
            via=self.via.text()
            numerocivico=self.numerocivico.text()

            # Generazione del cursore
            cursore = db.cursor()
            query = "INSERT INTO dipendente (CodiceFiscale, Cognome, Nome, DataNascita, IBAN, Email, Citta, CAP ,Via, NumeroCivico) VALUES ('"+cf+"', '"+cognome+"', '"+nome+"', '"+data+"', '"+iban+"', '"+email+"', '"+citta+"', '"+cap+"', '"+via+"', '"+numerocivico+"');"
            cursore.execute(query)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, ricontrolla i dati.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from dipendenti.Dipendenti import Dipendenti
        dipendente = Dipendenti()
        self.window().close()
        self.widget.addWidget(dipendente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)