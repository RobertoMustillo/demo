from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtWidgets

from PyQt5.uic import loadUi

from assegnamento.Assegnamento import Assegnamento
from assegnamentoturno.AssegnamentoTurno import AssegnamentoTurno
from bustapaga.BustaPaga import BustaPaga
from dipendenti.Dipendenti import Dipendenti
from telefonodipendente.TelefonoDipendente import TelefonoDipendente
from turno.Turno import Turno


class GestioneDipendenti(QDialog):
    def __init__(self):
        super(GestioneDipendenti, self).__init__()
        from login.LoginScreen import LoginScreen
        if LoginScreen.autorizzazione_accesso=="Admin":
            loadUi("home/gestione_dipendenti2.ui", self)
            self.widget = QtWidgets.QStackedWidget()
            self.listWidget.itemDoubleClicked.connect(self.goto_table)
            self.apri.clicked.connect(self.goto_table)
            self.esci.clicked.connect(self.funz_esci)
            #self.image.setPixmap(QPixmap('sfondo.png'))
        elif LoginScreen.autorizzazione_accesso=="Dip":
            loadUi("home/area_dip2.ui", self)
            self.widget = QtWidgets.QStackedWidget()
            self.listWidget.itemDoubleClicked.connect(self.goto_table)
            self.apri.clicked.connect(self.goto_table)
            self.esci.clicked.connect(self.funz_esci)
            #self.image.setPixmap(QPixmap('sfondo.png'))

    def goto_dip(self):
        dip = Dipendenti()
        self.window().close()
        self.widget.addWidget(dip)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_bustapaga(self):
        bustapaga = BustaPaga()
        self.window().close()
        self.widget.addWidget(bustapaga)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_turno(self):
        turno = Turno()
        self.window().close()
        self.widget.addWidget(turno)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_assegnamentoturno(self):
        assegnamentoturno = AssegnamentoTurno()
        self.window().close()
        self.widget.addWidget(assegnamentoturno)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_assegnamento(self):
        assegnamento = Assegnamento()
        self.window().close()
        self.widget.addWidget(assegnamento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_telefonodipendente(self):
        telefonodipendente = TelefonoDipendente()
        self.window().close()
        self.widget.addWidget(telefonodipendente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # apre la tabella selezionata dalla lista
    def goto_table(self):
        try:
            if self.listWidget.currentItem().text() == "dipendente":
                self.goto_dip()
            elif self.listWidget.currentItem().text() == "busta paga":
                self.goto_bustapaga()
            elif self.listWidget.currentItem().text() == "turno":
                self.goto_turno()
            elif self.listWidget.currentItem().text() == "assegnamento cimitero":
                self.goto_assegnamento()
            elif self.listWidget.currentItem().text() == "associazione turno":
                self.goto_assegnamentoturno()
            elif self.listWidget.currentItem().text() == "telefono":
                self.goto_telefonodipendente()

        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una tabella da aprire.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def funz_esci(self):
        from home.Home import Home
        home = Home()
        self.window().close()
        self.widget.addWidget(home)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)
