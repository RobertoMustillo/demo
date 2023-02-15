
import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaServizioAggiuntivo(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaServizioAggiuntivo, self).__init__()
        loadUi("servizioaggiuntivo/modificaservizioaggiuntivo.ui",self)
        self.elemento_selezionato = elemento_selezionato
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_elemento)

        self.widget = QtWidgets.QStackedWidget()

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

            tipo = self.tipo.text()
            prezzo = self.prezzo.text()

            # Generazione del cursore
            cursore = db.cursor()
            # cerco l'ID  selezionato
            query = "select * from servizioaggiuntivo"
            cursore.execute(query)
            result = cursore.fetchall()

            # creo un array di codici
            self.codici = []
            for x in result:
                self.codici.append(x[0])

            self.prezzi = []
            for x in result:
                self.prezzi.append(x[1])

            # prendo il codice selezionato
            codice_sel = self.codici[self.elemento_selezionato]
            prezzi_sel = self.prezzi[self.elemento_selezionato]

            self.query2 = "UPDATE `servizioaggiuntivo` SET `Tipo` = '" + tipo + "', `Prezzo` = '" + prezzo + "' WHERE `Tipo` = '" + codice_sel.__str__() + "' AND `Prezzo` = "+ prezzi_sel.__str__()+ ";"

            cursore.execute(self.query2)
            db.commit()
            self.funz_esci()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, controlla i dati inseriti, potrebbero essere già nel sistema o non sono corretti.', QMessageBox.Ok,
                                 QMessageBox.Ok)


    def funz_esci(self):
        from servizioaggiuntivo.ServizioAggiuntivo import ServizioAggiuntivo
        servizioaggiuntivo = ServizioAggiuntivo()
        self.window().close()
        self.widget.addWidget(servizioaggiuntivo)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)