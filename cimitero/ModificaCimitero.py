import mysql
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaCimitero(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaCimitero, self).__init__()
        loadUi("cimitero/modificacimitero.ui",self)
        self.elemento_selezionato = elemento_selezionato  #riga selezionata (che parte da 0)!!
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.funz_modifica)

        self.widget = QtWidgets.QStackedWidget()

    def funz_modifica(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        nome = self.nome.text()
        canone = self.canone.text()
        capienza = self.capienza.text()
        posti = self.posti.text()
        cap = self.cap.text()
        via = self.via.text()

        # Generazione del cursore
        cursore = db.cursor()
        # cerco l'ID selezionato
        query = "select * from cimitero"
        cursore.execute(query)
        result = cursore.fetchall()

        # creo un array di codici
        self.codici = []
        for x in result:
            self.codici.append(x[0])

        # prendo il codice selezionato
        codiceSel = self.codici[self.elemento_selezionato]
        query2= "UPDATE `cimitero` SET `Nome` = '"+nome+"', `Cap` = '"+cap+"', `Via` = '"+via+"', `CanoneAnnuo` = '"+canone+"', `Capienza` = '"+capienza+"', `PostiLiberi` = '"+posti+"' WHERE Nome = '"+codiceSel.__str__()+"';"
        cursore.execute(query2)
        db.commit()
        self.funz_esci()


    def funz_esci(self):
        from cimitero.Cimitero import Cimitero
        cimitero = Cimitero()
        self.window().close()
        self.widget.addWidget(cimitero)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)