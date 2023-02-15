
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaEmissioneFatturaServizio(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaEmissioneFatturaServizio, self).__init__()
        loadUi("emissionefatturaservizio/modificaemissionefatturaservizio.ui",self)
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
        query = "SELECT NumeroFattura FROM `db_illuminazione_votiva`.`fattura`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # popolo la comboBox
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

    def modifica_elemento(self):
        try:

            fattura = self.fattura.currentText()
            servizio = self.servizio.currentText()

            # Generazione del cursore
            cursore = self.db.cursor()
            # cerco l'ID  selezionato
            query = "select * from emissionefatturaservizio"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            self.servizi = []
            for x in result:
                self.servizi.append(x[1])

            # prendo il codice selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            servizio_sel = self.servizi[self.elemento_selezionato]

            self.query2 = "UPDATE `emissionefatturaservizio` SET `Fattura` = '" + fattura + "', `ServizioAggiuntivo` = '" + servizio + "' WHERE `Fattura` = " + codice_sel.__str__() + " AND `ServizioAggiuntivo` = '"+ servizio_sel.__str__()+ "';"

            cursore.execute(self.query2)
            self.db.commit()
            self.funz_esci()
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