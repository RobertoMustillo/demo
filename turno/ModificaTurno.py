import mysql
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ModificaTurno(QDialog):
    def __init__(self, elemento_selezionato):
        super(ModificaTurno, self).__init__()
        loadUi("turno/modificaturno.ui",self)
        self.elemento_selezionato = elemento_selezionato
        self.annulla.clicked.connect(self.funz_esci)
        self.modifica.clicked.connect(self.modifica_elemento)

        self.widget = QtWidgets.QStackedWidget()

    def modifica_elemento(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        id = self.id.text()
        data = self.data.date().toString("yyyy-MM-dd")
        oraI = self.timeEdit1.time().toString("HH:mm:ss")
        oraF = self.timeEdit2.time().toString("HH:mm:ss")

        # Generazione del cursore
        cursore = db.cursor()
        # cerco l'ID selezionato
        query = "select * from turno"
        cursore.execute(query)
        result = cursore.fetchall()

        # creo un array di codici
        self.codici = []
        for x in result:
            self.codici.append(x[0])

        # prendo il codice cliente selezionato
        codice_sel = self.codici[self.elemento_selezionato]
        query2= "UPDATE `turno` SET `CodTurno` = '"+id+"',`Data` = '"+data+"', `OraInizio` = '"+oraI+"', `OraFine` = '"+oraF+"' WHERE `CodTurno` = "+codice_sel.__str__()+";"
        cursore.execute(query2)
        db.commit()
        self.funz_esci()


    def funz_esci(self):
        from turno.Turno import Turno
        turno = Turno()
        self.window().close()
        self.widget.addWidget(turno)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)