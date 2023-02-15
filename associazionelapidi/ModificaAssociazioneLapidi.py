
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaAssociazioneLapidi(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaAssociazioneLapidi, self).__init__()
        loadUi("associazionelapidi/modificaassociazionelapide.ui",self)
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
        query = "SELECT CodManutenzione FROM `db_illuminazione_votiva`.`manutenzione` ORDER BY `manutenzione`.`CodManutenzione` ASC;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.manutenzione.addItems(self.codici)

        query2 = "SELECT CodEvento FROM `db_illuminazione_votiva`.`evento` ORDER BY `evento`.`CodEvento` ASC;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        self.eventi = []
        for x in result2:
            self.eventi.append(str(x[0]))
        self.evento.addItems(self.eventi)

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
            evento = self.evento.currentText()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID  selezionato
            query = "select * from associazionelapidi"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.manutenzioni = []
            for x in result:
                self.manutenzioni.append(x[0])

            self.eventi = []
            for x in result:
                self.eventi.append(x[1])

            # prendo il codice selezionato
            codiceSel = self.eventi[self.elemento_selezionato]
            man_sel = self.manutenzioni[self.elemento_selezionato]

            self.query2 = "UPDATE `associazionelapidi` SET `Manutenzione` = '" + manutenzione + "', `Evento` = '" + evento + "' WHERE `Manutenzione` = '" + man_sel.__str__() + "' AND `Evento` = '"+ codiceSel.__str__()+ "';"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from associazionelapidi.AssociazioneLapidi import AssociazioneLapidi
        associazionelapidi = AssociazioneLapidi()
        self.window().close()
        self.widget.addWidget(associazionelapidi)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)