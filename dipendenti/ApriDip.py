from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets


class ApriDip(QDialog):
    def __init__(self, dipendente_selezionato):
        super(ApriDip, self).__init__()
        loadUi("dipendenti/apridip.ui", self)
        self.dipendente_selezionato = dipendente_selezionato
        self.annulla.clicked.connect(self.funz_esci)

        self.widget = QtWidgets.QStackedWidget()

        self.id.setReadOnly(True)
        self.nome.setReadOnly(True)
        self.cognome.setReadOnly(True)
        self.cf.setReadOnly(True)
        self.dateEdit.setReadOnly(True)
        self.email.setReadOnly(True)
        self.iban.setReadOnly(True)
        self.citta.setReadOnly(True)
        self.cap.setReadOnly(True)
        self.via.setReadOnly(True)
        self.numerocivico.setReadOnly(True)


    def funz_esci(self):
        from dipendenti.Dipendenti import Dipendenti
        dip = Dipendenti()
        self.window().close()
        self.widget.addWidget(dip)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
