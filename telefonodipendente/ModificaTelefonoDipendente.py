
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaTelefonoDipendente(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaTelefonoDipendente, self).__init__()
        loadUi("telefonodipendente/modificatelefonodipendente.ui",self)
        self.elemento_selezionato = elemento_selezionato
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_elemento)

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

    def modifica_elemento(self):
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

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID  selezionato
            query = "select * from telefonodipendente"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.telefoni = []
            for x in result:
                self.telefoni.append(x[0])

            self.codici = []
            for x in result:
                self.codici.append(x[1])

            # prendo il codice selezionato
            codiceSel = self.codici[self.elemento_selezionato]
            tel_sel = self.telefoni[self.elemento_selezionato]

            self.query2 = "UPDATE `telefonodipendente` SET `Numero` = '" + telefono + "', `Dipendente` = '" + dipendente + "' WHERE `Numero` = '" + tel_sel.__str__() + "' AND `Dipendente` = '"+ codiceSel.__str__()+ "';"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
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