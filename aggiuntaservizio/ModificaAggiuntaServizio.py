
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaAggiuntaServizio(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaAggiuntaServizio, self).__init__()
        loadUi("aggiuntaservizio/modificaaggiuntaservizio.ui",self)
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
        query = "SELECT Tipo FROM `db_illuminazione_votiva`.`servizioaggiuntivo`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.codici = []
        for x in result:
            self.codici.append(x[0])
        self.servizio.addItems(self.codici)

        query2 = "SELECT CodDefunto FROM `db_illuminazione_votiva`.`defunto` ORDER BY `defunto`.`CodDefunto` ASC;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.cod_defunti = []
        for x in result2:
            self.cod_defunti.append(str(x[0]))
        self.defunto.addItems(self.cod_defunti)

    def modifica_elemento(self):
        try:

            servizio = self.servizio.currentText()
            defunto = self.defunto.currentText()

            # Generazione del cursore
            cursore = self.db.cursor()
            # cerco l'ID  selezionato
            query = "select * from aggiuntaservizio"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            # creo un array di servizi
            self.servizi = []
            for x in result:
                self.servizi.append(x[1])

            # prendo il codice selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            servizio_sel = self.servizi[self.elemento_selezionato]

            self.query2 = "UPDATE `aggiuntaservizio` SET `Defunto` = '" + defunto + "', `ServizioAggiuntivo` = '" + servizio + "' WHERE `Defunto` = " + codice_sel.__str__() + " AND `ServizioAggiuntivo` = '"+ servizio_sel.__str__()+ "';"

            cursore.execute(self.query2)
            self.db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from aggiuntaservizio.AggiuntaServizio import AggiuntaServizio
        aggiuntaservizio = AggiuntaServizio()
        self.window().close()
        self.widget.addWidget(aggiuntaservizio)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)