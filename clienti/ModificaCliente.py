import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaCliente(QDialog):
    def __init__(self, cliente_selezionato):
        super(ModificaCliente, self).__init__()
        loadUi("clienti/modificacliente.ui", self)
        self.cliente_selezionato = cliente_selezionato  # riga del cliente selezionato (che parte da 0)!!
        # print("riga cliente sel: ")
        # print(self.cliente_selezionato)
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_cliente)

        self.widget = QtWidgets.QStackedWidget()

    def modifica_cliente(self):
        try:
            # Test di connessione a MySQL
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="db_illuminazione_votiva",
                port=8889
            )

            id = self.id.text()
            nome = self.nome.text()
            cognome = self.cognome.text()
            cf = self.cf.text()
            data = self.dateEdit.date().toString("yyyy-MM-dd")
            email = self.email.text()
            fattura = self.comboBox.currentText()
            citta = self.citta.text()
            cap = self.cap.text()
            via = self.via.text()
            numerocivico = self.numerocivico.text()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID del cliente selezionato
            query = "select * from cliente"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codiciClienti
            self.codClienti = []
            for x in result:
                self.codClienti.append(x[0])

            # prendo il codice cliente selezionato
            codiceClienteSel = self.codClienti[self.cliente_selezionato]
            # print(codiceClienteSel)
            query2 = "UPDATE `cliente` SET `CodCliente` = '" + id + "', `CodiceFiscale` = '" + cf + "', `Cognome` = '" + cognome + "', `Nome` = '" + nome + "', `RicezioneFattura` = '" + fattura + "', `DataNascita` = '" + data + "', `Email` = '" + email + "', `Citta` = '" + citta + "', `CAP` = '" + cap + "', `Via` = '" + via + "', `NumeroCivico` = '" + numerocivico + "' WHERE `cliente`.`CodCliente` = " + codiceClienteSel.__str__() + ";"
            cursore.execute(query2)
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
