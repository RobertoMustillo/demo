
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaAssociazioneCimitero(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaAssociazioneCimitero, self).__init__()
        loadUi("associazionecimitero/modificaassociazionecimitero.ui",self)
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
        self.nomi = []
        for x in result2:
            self.nomi.append(str(x[0]))
        self.cimitero.addItems(self.nomi)

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

            manutenzione = self.manutenzione.currentText()
            cimitero = self.cimitero.currentText()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID  selezionato
            query = "select * from associazionecimitero"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.manutenzioni = []
            for x in result:
                self.manutenzioni.append(x[0])

            self.cimiteri = []
            for x in result:
                self.cimiteri.append(x[1])

            # prendo il codice selezionato
            codiceSel = self.cimiteri[self.elemento_selezionato]
            man_sel = self.manutenzioni[self.elemento_selezionato]

            self.query2 = "UPDATE `associazionecimitero` SET `Manutenzione` = '" + manutenzione + "', `Cimitero` = '" + cimitero + "' WHERE `Manutenzione` = '" + man_sel.__str__() + "' AND `Cimitero` = '"+ codiceSel.__str__()+ "';"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
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