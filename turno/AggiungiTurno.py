import mysql
from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class AggiungiTurno(QDialog):
    def __init__(self):
        super(AggiungiTurno, self).__init__()
        loadUi("turno/aggiungiturno.ui",self)
        self.annulla.clicked.connect(self.funz_esci)
        self.aggiungi.clicked.connect(self.aggiungi_defunto)

        #fornisce uno stack di widget in cui è visibile un solo widget alla volta
        self.widget = QtWidgets.QStackedWidget()

    def aggiungi_defunto(self):
        # Test di connessione a MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="db_illuminazione_votiva",
            port=8889
        )

        data = self.data.date().toString("yyyy-MM-dd")
        oraI = self.timeEdit1.time().toString("HH:mm:ss")
        oraF = self.timeEdit2.time().toString("HH:mm:ss")

        # Generazione del cursore
        cursore = db.cursor()
        query = "INSERT INTO turno (Data, OraInizio, OraFine) VALUES ('"+data+"', '"+oraI+"', '"+oraF+ "');"
        cursore.execute(query)
        db.commit()
        self.funz_esci()

    def funz_esci(self):
        from turno.Turno import Turno
        turno = Turno()
        self.window().close()
        self.widget.addWidget(turno)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)