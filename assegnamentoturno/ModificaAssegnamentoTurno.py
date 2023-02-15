
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaAssegnamentoTurno(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaAssegnamentoTurno, self).__init__()
        loadUi("assegnamentoturno/modificaassegnamentoturno.ui",self)
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
        query = "SELECT CodTurno FROM `db_illuminazione_votiva`.`turno`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.turno.addItems(self.codici)

        query2 = "SELECT CodDipendente FROM `db_illuminazione_votiva`.`dipendente`;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.cod_dip = []
        for x in result2:
            self.cod_dip.append(str(x[0]))
        self.dipendente.addItems(self.cod_dip)

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
            turno = self.turno.currentText()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID  selezionato
            query = "select * from assegnamentoturno"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[1])

            # creo un array di servizi
            self.dip = []
            for x in result:
                self.dip.append(x[0])

            # prendo il codice selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            dip_sel = self.dip[self.elemento_selezionato]

            self.query2 = "UPDATE `assegnamentoturno` SET `Turno` = '" + turno + "', `Dipendente` = '" + dipendente + "' WHERE `Turno` = '" + codice_sel.__str__() + "' AND `Dipendente` = "+ dip_sel.__str__()+ ";"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from assegnamentoturno.AssegnamentoTurno import AssegnamentoTurno
        assegnamentoturno = AssegnamentoTurno()
        self.window().close()
        self.widget.addWidget(assegnamentoturno)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)