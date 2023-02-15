
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiAssegnamento(QDialog):
    def __init__(self):
        super(AggiungiAssegnamento, self).__init__()
        loadUi("assegnamento/aggiungiassegnamento.ui",self)
        self.annulla.clicked.connect(self.funz_esci)
        self.aggiungi.clicked.connect(self.funz_aggiungi)

        #fornisce uno stack di widget in cui è visibile un solo widget alla volta
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
        query = "SELECT Nome FROM `db_illuminazione_votiva`.`cimitero`;"
        self.cursore.execute(query)
        result = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.codici = []
        for x in result:
            self.codici.append(x[0])
        self.cimitero.addItems(self.codici)

        query2 = "SELECT CodDipendente FROM `db_illuminazione_votiva`.`dipendente`;"
        self.cursore.execute(query2)
        result2 = self.cursore.fetchall()
        # aggiungo i servizi aggiuntivi alla comboBox, essendo chiave esterna
        self.cod_dip = []
        for x in result2:
            self.cod_dip.append(str(x[0]))
        self.dipendente.addItems(self.cod_dip)

    def funz_aggiungi(self):
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
            cimitero = self.cimitero.currentText()

            # effettuo controllo di non nullità
            if cimitero == "" or dipendente == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                         QMessageBox.Ok, QMessageBox.Ok)

            elif  dipendente.isnumeric():
                    # Generazione del cursore
                    cursore = db.cursor()
                    query = "INSERT INTO assegnamento (Cimitero, Dipendente) VALUES ('" + cimitero + "', '" + dipendente + "');"
                    cursore.execute(query)
                    db.commit()
                    self.funz_esci()
            else:
                    QMessageBox.critical(self, 'Errore', 'Per favore, inserisci il codice Dipendente in formato numerico',
                                         QMessageBox.Ok, QMessageBox.Ok)

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from assegnamento.Assegnamento import Assegnamento
        assegnamento = Assegnamento()
        self.window().close()
        self.widget.addWidget(assegnamento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)