from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5 import QtWidgets

from PyQt5.uic import loadUi

from clienti.ClientiScreen import ClientiScreen
from emissionefattura.EmissioneFattura import EmissioneFattura
from emissionefatturaservizio.EmissioneFatturaServizio import EmissioneFatturaServizio
from eventi.Evento import Evento
from fattura.Fattura import Fattura
from telefonocliente.TelefonoCliente import TelefonoCliente


class GestioneClienti(QDialog):
    def __init__(self):
        super(GestioneClienti, self).__init__()
        loadUi("home/gestione_clienti2.ui", self)
        self.widget = QtWidgets.QStackedWidget()
        self.listWidget.itemDoubleClicked.connect(self.goto_table)
        self.apri.clicked.connect(self.goto_table)
        self.esci.clicked.connect(self.funz_esci)

        #self.image.setPixmap(QPixmap('sfondo.png'))

    def goto_clienti(self):
        clienti = ClientiScreen()
        self.window().close()
        self.widget.addWidget(clienti)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_evento(self):
        evento = Evento()
        self.window().close()
        self.widget.addWidget(evento)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_fattura(self):
        fattura = Fattura()
        self.window().close()
        self.widget.addWidget(fattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_telefonocliente(self):
        telefonocliente = TelefonoCliente()
        self.window().close()
        self.widget.addWidget(telefonocliente)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_emissionefattura(self):
        emissionefattura = EmissioneFattura()
        self.window().close()
        self.widget.addWidget(emissionefattura)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def goto_emissionefatturaservizio(self):
        emissionefatturaservizio = EmissioneFatturaServizio()
        self.window().close()
        self.widget.addWidget(emissionefatturaservizio)
        self.widget.showMaximized()
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    # apre la tabella selezionata dalla lista
    def goto_table(self):
        try:
            if self.listWidget.currentRow() == 0:
                self.goto_clienti()
            elif self.listWidget.currentRow() == 1:
                self.goto_evento()
            elif self.listWidget.currentRow() == 2:
                self.goto_fattura()
            elif self.listWidget.currentRow() == 3:
                self.goto_emissionefattura()
            elif self.listWidget.currentRow() == 4:
                self.goto_emissionefatturaservizio()
            elif self.listWidget.currentRow() == 5:
                self.goto_telefonocliente()

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
