
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaEmissioneFattura(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaEmissioneFattura, self).__init__()
        loadUi("emissionefattura/modificaemissionefattura.ui",self)
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

        query2 = "SELECT CodEvento FROM `db_illuminazione_votiva`.`evento` ORDER BY `evento`.`CodEvento` ASC;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        self.cod_eventi = []
        for x in result2:
            self.cod_eventi.append(str(x[0]))
        self.evento.addItems(self.cod_eventi)

    def modifica_elemento(self):
        try:

            fattura = self.fattura.currentText()
            evento = self.evento.currentText()
            canone = self.canone.text()
            allaccio = self.allaccio.text()

            # Generazione del cursore
            cursore = self.db.cursor()
            # cerco l'ID  selezionato
            query = "select * from emissionefattura"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            self.eventi = []
            for x in result:
                self.eventi.append(x[1])

            # prendo il codice selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            evento_sel = self.eventi[self.elemento_selezionato]

            self.query2 = "UPDATE `emissionefattura` SET `Fattura` = '" + fattura + "', `Evento` = '" + evento + "', `CanoneAnnuo` = '" + canone + "', `CostoAllaccio` = '" + allaccio + "' WHERE `Fattura` = " + codice_sel.__str__() + " AND `Evento` = '"+ evento_sel.__str__()+ "';"

            cursore.execute(self.query2)
            self.db.commit()
            self.funz_esci()
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