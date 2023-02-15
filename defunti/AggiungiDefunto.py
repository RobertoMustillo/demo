import mysql
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiDefunto(QDialog):
    def __init__(self):
        super(AggiungiDefunto, self).__init__()
        loadUi("defunti/aggiungidefunto.ui",self)
        self.annulla.clicked.connect(self.funz_esci)
        self.aggiungi.clicked.connect(self.aggiungi_defunto)

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
        # aggiungo le chiavi esterne alla comboBox
        self.codici = []
        for x in result:
            self.codici.append(str(x[0]))
        self.comboBox.addItems(self.codici)

    def aggiungi_defunto(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        nome = self.nome.text()
        cognome = self.cognome.text()
        dataN = self.dateN.date().toString("yyyy-MM-dd")
        dataD = self.dateDecesso.date().toString("yyyy-MM-dd")
        luogon = self.luogon.text()
        cimitero = self.comboBox.currentText()
        ubicazione=self.ubicazione.text()

        # Generazione del cursore
        cursore = db.cursor()
        query = "INSERT INTO defunto (Cognome, Nome, DataNascita, DataDecesso, LuogoNascita, Cimitero, Ubicazione) VALUES ('"+cognome+"', '"+nome+"', '"+dataN+"', '"+dataD+"', '"+luogon+"', '"+cimitero+"', '"+ubicazione+"');"
        cursore.execute(query)
        db.commit()
        #self.funz_esci()

        QMessageBox.information(self, 'Info', 'Ricorda di aggiornare i POSTI LIBERI!',
                                QMessageBox.Ok, QMessageBox.Ok)
        self.goto_cimitero()

    def funz_esci(self):
        from defunti.DefuntiScreen import DefuntiScreen
        defunto = DefuntiScreen()
        self.window().close()
        self.widget.addWidget(defunto)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_cimitero(self):
        from cimitero.Cimitero import Cimitero
        cimitero = Cimitero()
        self.window().close()
        self.widget.addWidget(cimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)