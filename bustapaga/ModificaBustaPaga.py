
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaBustaPaga(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaBustaPaga, self).__init__()
        loadUi("bustapaga/modificabustapaga.ui",self)
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
        # aggiungo le chiavi esterne alla comboBox
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

            dipendente = self.dipendente.currentText()
            mese = self.mese.text()
            anno = self.anno.text()
            importo = self.importo.text()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID  selezionato
            query = "select * from bustapaga"
            cursore.execute(query)
            result = cursore.fetchall()

            self.mesi = []
            for x in result:
                self.mesi.append(x[1])

            self.dipendenti = []
            for x in result:
                self.dipendenti.append(x[0])

            self.anni = []
            for x in result:
                self.anni.append(x[2])

            # prendo il codice selezionato
            mesi_sel = self.mesi[self.elemento_selezionato]
            dip_sel = self.dipendenti[self.elemento_selezionato]
            anni_sel = self.anni[self.elemento_selezionato]

            self.query2 = "UPDATE `bustapaga` SET `Dipendente` = '" + dipendente + "', `Mese` = '" + mese + "', `Anno` = '" + anno + "', `Importo` = '" + importo + "' WHERE `Dipendente` = '" + dip_sel.__str__() + "' AND `Mese` = '"+ mesi_sel.__str__()+ "' AND `Anno` = '"+ anni_sel.__str__()+ "';"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from bustapaga.BustaPaga import BustaPaga
        bustapaga = BustaPaga()
        self.window().close()
        self.widget.addWidget(bustapaga)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)