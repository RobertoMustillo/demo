import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiCliente(QDialog):
    def __init__(self):
        super(AggiungiCliente, self).__init__()
        loadUi("clienti/aggiungicliente.ui",self)
        self.annulla.clicked.connect(self.funz_esci)
        self.aggiungi.clicked.connect(self.aggiungi_cliente)

        #fornisce uno stack di widget in cui è visibile un solo widget alla volta
        self.widget = QtWidgets.QStackedWidget()

    def aggiungi_cliente(self):
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
            fattura = self.comboBox.currentText()
            citta=self.citta.text()
            cap=self.cap.text()
            via=self.via.text()
            numerocivico=self.numerocivico.text()

            # Generazione del cursore
            cursore = db.cursor()
            query = "INSERT INTO cliente (CodiceFiscale, Cognome, Nome, DataNascita, RicezioneFattura, Email, Citta, CAP ,Via, NumeroCivico) VALUES ('"+cf+"', '"+cognome+"', '"+nome+"', '"+data+"', '"+fattura+"', '"+email+"', '"+citta+"', '"+cap+"', '"+via+"', '"+numerocivico+"');"
            cursore.execute(query)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, ricontrolla i dati.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from clienti.ClientiScreen import ClientiScreen
        clienti = ClientiScreen()
        self.window().close()
        self.widget.addWidget(clienti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)